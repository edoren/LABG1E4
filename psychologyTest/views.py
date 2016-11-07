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
from psychologyTest.models import (AssignTestKolb, Group, Institution,
                                   TestKolb, TestKolbAnswer, TestKolbQuestion,
                                   User)
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
    return render(request, "register.html", {})


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

    # Get all the asigned tests
    count = 0
    for assigned in request.user.assigntestkolb_set.all():
        count += 1

    print(count)

    return render(request, "home_student.html", {

    })


@login_required(login_url="/")
def account_requests(request):
    if request.user.role != "A":
        return RedirectToHome(request.user)

    return render(request, "account_requests.html", {})


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
def assign_groups(request):
    if request.user.role != "A":
        return RedirectToHome(request.user)

    groups = Group.objects.filter(is_active=True)
    psychologists = User.objects.filter(role="P")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add":
            try:
                group_id = int(request.POST.get("group"))
                psychologist_id = int(request.POST.get("psychologist"))
                group = Group.objects.get(pk=group_id)
                psychologist = User.objects.get(pk=psychologist_id)
                group.psychologist = psychologist
                group.save()
            except:
                print "Error error can not assign group"
        if action == "remove":
            try:
                group_id = int(request.POST.get("group"))
                group = Group.objects.get(pk=group_id)
                group.psychologist = None
                group.save()
            except:
                print "Error error can not remove psychologist from group"

    return render(request, "assign_groups.html", {
        "asigned_groups": groups.filter(~Q(psychologist=None)),
        "not_asigned_groups": groups.filter(Q(psychologist=None)),
        "psychologists": psychologists
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

    return render(request, "kolb_test_question.html", {"form": form})


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
