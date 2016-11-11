# -*- coding:utf-8 -*-
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import Http404
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)
from psychologyTest.forms import (AddGroupForm, AddInstitutionForm,
                                  AddUserForm, CreateAssignTestKolb,
                                  CreateTestKolb, CreateTestKolbQuestion,
                                  EditUserProfileForm)
from psychologyTest.models import (AccountRequest, AssignTestKolb, Group,
                                   Institution, StudentGroup, TestKolb,
                                   TestKolbAnswer, TestKolbQuestion, User)
from psychologyTest.util import RedirectToHome, try_cast_int


def login_page(request):
    data = {}

    if request.user.is_authenticated():
        return RedirectToHome(request.user)

    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            data["error"] = "Nombre de usuario o contraseña incorrectos."
            return render(request, "login.html", data)

        if user.is_active:
            login(request, user)
            data["success"] = "Login correcto"
            return RedirectToHome(user)
        else:
            data["error"] = "El usuario no esta activo o fué eliminado."

    return render(request, "login.html", data)


def register(request):
    data = request.POST.dict()
    data.update({"is_active": False})
    form = AddUserForm(request.POST)
    message_success = None
    message_error = None

    if request.method == "POST":
        if form.is_valid():
            usuario = form.save()
            AccountRequest(user=usuario).save()
            if usuario.role == "S":
                StudentGroup(student=usuario, group=None).save()
            form = AddUserForm(None)
            message_success = ("Registro exitoso. Por favor espere a que un "
                               "administrador active su cuenta")
        else:
            message_error = form.errors

    return render(request, "register.html", {
        "form": form,
        "message_success": message_success,
        "message_error": message_error
    })


def restore_password(request):
    if request.POST:
        from_email = EMAIL_HOST_USER
        to_email = request.POST.get("email")
        try:
            user = User.objects.get(email=to_email)
        except User.DoesNotExist:
            user = None
        if user is not None:
            password = user.password
            subject = ("Alguien solicito reestablecer la contrasena para "
                       "tu cuenta en PTTI")
            message = ("Hola, alguien solicito recientemente que se "
                       "restablezca tu contrasena de PTTI. "
                       "Esta es tu contrasena: {}".format(password))
            mail = EmailMessage(subject, message, from_email, [to_email])
            mail.send()
        return redirect("login_page")
    else:
        return render(request, "restore_password.html", {})


@login_required(login_url="/")
def logout_page(request):
    logout(request)
    return redirect("login_page")


@login_required(login_url="/")
def home_admin(request):
    if request.user.role != "A":
        return RedirectToHome(request.user)

    user_profile = User.objects.filter(
        is_active=True).exclude(role="R").exclude(role="A")
    groups = Group.objects.filter(is_active=True)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            form = AddUserForm(request.POST, initial={"is_active": True})
            if form.is_valid():
                usuario = form.save(commit=False)
                usuario.is_active = True
                usuario.save()
                if usuario.role == "S":
                    StudentGroup(student=usuario, group=None).save()
            else:
                print form.errors
        elif action == "modify":
            id_obj = request.POST.get("id")
            if id_obj is not None:
                user = User.objects.get(pk=id_obj)
                form = AddUserForm(request.POST, instance=user,
                                   initial={"is_active": True})
                if form.is_valid():
                    usuario = form.save(commit=False)
                    usuario.is_active = True
                    usuario.save()
                else:
                    print form.errors
        elif action == "remove":
            id_obj = request.POST.get("id")
            if id_obj is not None:
                obj = User.objects.get(pk=id_obj)
                obj.is_active = False
                obj.save()

    return render(request, "home_admin.html",
                  {"user_profile": user_profile, "groups": groups})


@login_required(login_url="/")
def home_psychologist(request):
    if request.user.role != "P":
        return RedirectToHome(request.user)

    groups = Group.objects.filter(psychologist=request.user)

    return render(request, "home_psychologist.html", {
        "groups": groups.filter(is_active=True)
    })


@login_required(login_url="/")
def home_student(request):
    if request.user.role != "S":
        return RedirectToHome(request.user)

    return render(request, "home_student.html", {})


@login_required(login_url="/")
def account_requests(request):
    if request.user.role != "A":
        return RedirectToHome(request.user)

    requested_accounts = AccountRequest.objects.all()

    if request.method == "GET":
        accept = request.GET.get("accept")
        deny = request.GET.get("deny")
        user_id = accept or deny
        if (user_id is not None):
            try:
                acc = AccountRequest.objects.get(user=user_id)
                if accept:
                    acc.user.is_active = True
                    acc.user.save()
                elif deny:
                    acc.user.delete()
                acc.delete()
            except:
                pass

    return render(request, "account_requests.html", {
        "requested_accounts": requested_accounts
    })


@login_required(login_url="/")
def manage_groups(request):
    if request.user.role != "A":
        return RedirectToHome(request.user)

    groups = Group.objects.filter(is_active=True)
    institutions = Institution.objects.filter(is_active=True)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            form = AddGroupForm(request.POST)
            if form.is_valid():
                gr = form.save(commit=False)
                gr.is_active = True
                gr.save()
            else:
                print form.errors
        elif action == "modify":
            id_obj = request.POST.get("id")
            if id_obj is not None:
                user = Group.objects.get(pk=id_obj)
                form = AddGroupForm(request.POST, instance=user)
                if form.is_valid():
                    gr = form.save(commit=False)
                    gr.is_active = True
                    gr.save()
                else:
                    print form.errors
        elif action == "remove":
            id_obj = request.POST.get("id")
            if id_obj is not None:
                obj = Group.objects.get(pk=id_obj)
                obj.is_active = False
                obj.save()

    return render(request, "manage_groups.html", {
        "groups": groups,
        "institutions": institutions
    })


@login_required(login_url="/")
def manage_institutions(request):
    if request.user.role != "A":
        return RedirectToHome(request.user)

    institutions = Institution.objects.filter(is_active=True)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            form = AddInstitutionForm(request.POST)
            if form.is_valid():
                inst = form.save(commit=False)
                inst.is_active = True
                inst.save()
            else:
                print form.errors
        elif action == "modify":
            id_obj = request.POST.get("id")
            if id_obj is not None:
                obj = Institution.objects.get(pk=id_obj)
                form = AddInstitutionForm(request.POST, instance=obj)
                if form.is_valid():
                    inst = form.save(commit=False)
                    inst.is_active = True
                    inst.save()
                else:
                    print form.errors
        elif action == "remove":
            id_obj = request.POST.get("id")
            if id_obj is not None:
                obj = Institution.objects.get(pk=id_obj)
                obj.is_active = False
                obj.save()

    return render(request, "manage_institutions.html", {
        "institutions": institutions
    })


@login_required(login_url="/")
def assign_workloads(request):
    if request.user.role != "A":
        return RedirectToHome(request.user)

    groups = Group.objects.filter(is_active=True)
    psychologists = User.objects.filter(role="P")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add":
            try:
                group_id = request.POST.get("group")
                psychologist_id = request.POST.get("psychologist")
                group = Group.objects.get(pk=group_id)
                psychologist = User.objects.get(pk=psychologist_id)
                group.psychologist = psychologist
                group.save()
            except:
                print "Error error can not assign group"
        elif action == "remove":
            try:
                group_id = request.POST.get("group")
                group = Group.objects.get(pk=group_id)
                group.psychologist = None
                group.save()
            except:
                print "Error error can not remove psychologist from group"

    return render(request, "assign_workloads.html", {
        "asigned_groups": groups.filter(~Q(psychologist=None)),
        "not_asigned_groups": groups.filter(Q(psychologist=None)),
        "psychologists": psychologists
    })


@login_required(login_url="/")
def assign_group_student(request, group_id=None):
    if request.user.role != "A":
        return RedirectToHome(request.user)

    group = get_object_or_404(Group, pk=group_id)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add":
            try:
                student_id = request.POST.get("student")
                assign = StudentGroup.objects.get(student=student_id)
                assign.group = group
                assign.save()
            except:
                print "Error assigning user"
        elif action == "remove":
            try:
                assign_id = request.POST.get("assignation")
                assign = StudentGroup.objects.get(pk=assign_id)
                assign.group = None
                assign.save()
            except:
                print "Error error can not remove psychologist from group"

    assignations = StudentGroup.objects.filter(group=group)

    not_assigned = StudentGroup.objects.filter(group=None)

    return render(request, "assign_group_student.html", {
        "assignations": assignations,
        "not_assigned": not_assigned
    })


@login_required(login_url="/")
def edit_profile(request):
    if request.user.role == "R":
        return RedirectToHome(request.user)

    groups = Group.objects.filter(is_active=True)

    if request.method == "POST":
        form = EditUserProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            print form.errors

    BASE = {
        "A": "base_admin.html",
        "P": "base_psychologist.html",
        "S": "base_student.html"
    }

    return render(request, "edit_profile.html", {
        "base": BASE[request.user.role],
        "groups": groups
    })


@login_required(login_url="/")
def manage_tests(request, action=None):
    if request.user.role != "P":
        return RedirectToHome(request.user)

    tests = TestKolb.objects.filter(psychologist=request.user.id)

    if action is None:
        return render(request, "manage_tests.html", {"tests": tests})
    elif action == "create":
        new_test = CreateTestKolb({
            "name": "Untitled Test",
            "psychologist": request.user.id
        })
        if new_test.is_valid():
            test = new_test.save()
            test_id = test.id
            return redirect("kolb_test", action="edit", test_id=test_id)
    elif action == "assign":
        test_id = request.GET.get("id")
        return redirect("kolb_test", action="assign", test_id=test_id)
    elif action == "edit":
        test_id = request.GET.get("id")
        return redirect("kolb_test", action="edit", test_id=test_id)
    elif action == "remove":
        test_id = request.GET.get("id")
        get_object_or_404(TestKolb, pk=test_id).delete()
        return redirect("manage_tests")

    raise Http404


@login_required(login_url="/")
def kolb_test(request, action=None, test_id=None):
    if request.user.role != "P":
        return RedirectToHome(request.user)

    if action is None or test_id is None:
        raise Http404

    test = get_object_or_404(TestKolb, pk=test_id,
                             psychologist=request.user.id)

    if action == "assign":
        data = request.POST.dict()
        data.update({"test": test.id})

        if request.method == "POST":
            action = request.POST.get("action")
            student_id = request.POST.get("student")
            if action == "add" and student_id != "None":
                form = CreateAssignTestKolb(data)
                if form.is_valid():
                    form.save()
                else:
                    print form.errors
            elif action == "remove":
                assignation_id = request.POST.get("assignation_id")
                try:
                    assignation = AssignTestKolb.objects.get(pk=assignation_id)
                    assignation.delete()
                except:
                    pass

        # Get the users not asigned to this test
        not_assigned = []
        for group in request.user.group_set.all():
            for t in group.studentgroup_set.all():
                student = AssignTestKolb.objects.filter(student=t.student.id,
                                                        test=test_id)
                if student.count() == 0:
                    not_assigned.append((t.student, t.group))

        return render(request, "assign_test_student.html", {
            "test": test,
            "not_assigned": not_assigned
        })
    if action == "edit":
        form = CreateTestKolb(None, instance=test)

        if request.method == "POST":
            data = request.POST.dict()
            data.update({"psychologist": request.user.id})
            form = CreateTestKolb(data, instance=test)
            if form.is_valid():
                form.save()
                return redirect("manage_tests")
            else:
                print "Error guardando test"
                print form.errors

        return render(request, "kolb_test.html", {"form": form, "test": test})
    else:
        raise Http404


@login_required(login_url="/")
def kolb_test_question(request, test_id=None, action=None):
    if request.user.role != "P":
        return RedirectToHome(request.user)

    if action is None or test_id is None:
        raise Http404

    test = get_object_or_404(TestKolb, pk=test_id,
                             psychologist=request.user.id)

    if action == "add":
        question = None
    elif action == "edit":
        question_id = request.GET.get("id")
        question = get_object_or_404(TestKolbQuestion, pk=question_id)
    elif action == "remove":
        question_id = request.GET.get("id")
        question = get_object_or_404(TestKolbQuestion, pk=question_id)
        question.delete()
        return redirect("kolb_test", action="edit", test_id=test_id)
    else:
        raise Http404

    form = CreateTestKolbQuestion(None, instance=question)

    if request.method == "POST":
        data = request.POST.dict()
        data.update({
            "test": test.id,
            "psychologist": request.user.id
        })
        form = CreateTestKolbQuestion(data, instance=question)
        if form.is_valid():
            form.save()
            return redirect("kolb_test", action="edit", test_id=test_id)
        else:
            print "Error ingresando pregunta"
            print form.errors

    return render(request, "kolb_test_question.html", {
        "test_id": test.id,
        "form": form
    })


@login_required(login_url="/")
def kolb_test_solve(request, test_id=None):
    if request.user.role != "S":
        return RedirectToHome(request.user)

    # Check that the test is assigned to the user
    assignation = get_object_or_404(AssignTestKolb, test=test_id,
                                    student=request.user.id)
    test = assignation.test

    # Retreive all the answers for each question is does not exist
    # it creates one
    questions = test.testkolbquestion_set.all()
    answers = []
    for question in questions:
        query = question.testkolbanswer_set.filter(assignation=assignation)
        if query.count() == 0:
            answer = TestKolbAnswer(question=question,
                                    assignation=assignation).save()
        else:
            answer = query.first()
        answers.append(answer)

    if request.method == "POST":
        data = request.POST
        option1 = [try_cast_int(x) for x in data.getlist("option1")]
        option2 = [try_cast_int(x) for x in data.getlist("option2")]
        option3 = [try_cast_int(x) for x in data.getlist("option3")]
        option4 = [try_cast_int(x) for x in data.getlist("option4")]
        rcv_answers = zip(option1, option2, option3, option4)
        if len(answers) == len(rcv_answers):
            for answer, rcv_answer in zip(answers, rcv_answers):
                answer.option1 = rcv_answer[0]
                answer.option2 = rcv_answer[1]
                answer.option3 = rcv_answer[2]
                answer.option4 = rcv_answer[3]
                answer.save()
            finished = (True not in [None in x for x in rcv_answers])
            assignation.is_finished = finished
            assignation.save()
        return redirect("home_student")

    q_and_a = zip(questions, answers)

    return render(request, "kolb_test_solve.html", {
        "test": test,
        "q_and_a": q_and_a
    })


@login_required(login_url="/")
def kolb_test_result(request, test_id=None):
    if request.user.role != "S":
        return RedirectToHome(request.user)

    # Check that the test is assigned to the user
    assignation = get_object_or_404(AssignTestKolb, test=test_id,
                                    student=request.user.id)
    test = assignation.test

    if not assignation.is_finished:
        raise Http404

    default_num_questions = 9
    max_calification = 9 * 4

    answers = assignation.testkolbanswer_set.all()

    learning_styles = {
        "convergent": {
            "name": "Convergente",
            "description": "Su punto más fuerte reside en la aplicación práctica de las ideas. Esta persona se desempeña mejor en las pruebas que requieren una sola respuesta o solución concreta para una pregunta o problema. Organiza sus conocimientos de manera que se pueda concretar en resolver problemas usando razonamiento hipotético deductivo. Estas personas se orientan más a las cosas que a las personas. Tienden a tener menos intereses por la materia física y se orientan a la especialización científica.",
            "caracteristics": ["Pragmático", "Racional", "Analítico", "Organizado",
                       "Buen discriminador", "Orientado a la tarea",
                       "Disfruta aspectos técnicos", "Insensible", "Deductivo",
                       "Gusta de la experimentación", "Es poco empático",
                       "Hermético", "Poco imaginativo", "Buen líder"]
        },
        "divergent": {
            "name": "Divergente",
            "description": "Se desempeña mejor en cosas concretas (EC) y la observación reflexiva (OR). Su punto más fuerte es la capacidad imaginativa. Se destaca porque tiende a considerar situaciones concretas desde muchas perspectivas. Se califica este estilo como “divergente” porque es una persona que funciona bien en situaciones que exigen producción de ideas (como en la “lluvia de ideas”).",
            "caracteristics": ["Sociable", "Sintetiza bien", "Genera ideas", "Soñador", "Valora la comprensión", "Orientado a las personas", "Espontáneo", "Disfruta el descubrimiento", "Empático", "Abierto", "Muy imaginativo", "Emocional", "Flexible", "Intuitivo"]
        },
        "assimilative": {
            "name": "Asimilador",
            "description": "Predomina en esta persona la conceptualización abstracta (CA) y la observación reflexiva (OR). Su punto más fuerte lo tiene en la capacidad de crear modelos teóricos. Se caracteriza por un razonamiento inductivo y poder juntar observaciones dispares en una explicación integral. Se interesa menos por las personas que por los conceptos abstractos, y dentro de éstos prefiere lo teórico a la aplicación práctica. Suele ser un científico o un investigador.",
            "caracteristics": ["Poco sociable", "Sintetiza bien", "Genera modelos", "Reflexivo", "Pensador abstracto", "Poco sensible", "Orientado a la reflexión", "Disfruta la teoría", "Disfruta hacer teoría", "Poco empático", "Hermético", "Disfruta el diseño", "Planificador", "Investigador"]
        },
        "accommodative": {
            "name": "Acomodador",
            "description": "Se desempeña mejor en la experiencia concreta (EC) y la experimentación activa (EA). Su punto más fuerte reside en hacer cosas e involucrarse en experiencias nuevas. Suele arriesgarse más que las personas de los otros tres estilos de aprendizaje. Se lo llama “acomodador” porque se destaca en situaciones donde hay que adaptarse a circunstancias inmediatas específicas. Es pragmático, en el sentido de descartar una teoría sobre lo que hay que hacer, si ésta no se aviene con los “hechos”. El acomodador se siente cómodo con las personas, aunque a veces se impacienta y es “atropellador”. Este tipo suele encontrarse dedicado a la política, a la docencia, a actividades técnicas o prácticas, como los negocios.",
            "caracteristics": ["Sociable", "Organizado", "Acepta retos", "Flexible", "Impulsivo", "Busca objetivos", "Comprometido", "Orientado a la acción", "Dependiente de los demás", "Poca habilidad analítica", "Empático", "Abierto", "Asistemático", "Espontáneo"]
        }
    }

    scores = {"EC": 0, "OR": 0, "CA": 0, "EA": 0}
    for answer in answers:
        scores["EC"] += answer.option1
        scores["OR"] += answer.option2
        scores["CA"] += answer.option3
        scores["EA"] += answer.option4

    max_area = (answers.count() * 4) * 2

    scores = {
        "convergent": (scores["CA"] * scores["EA"]) / 2,
        "divergent": (scores["EC"] * scores["OR"]) / 2,
        "assimilative": (scores["CA"] * scores["OR"]) / 2,
        "accommodative": (scores["EC"] * scores["EA"]) / 2
    }

    greatest_learning_style = max(scores, key=scores.get)

    return render(request, "kolb_test_result.html", {
        "test": test,
        "learning_type": learning_styles[greatest_learning_style]
    })
