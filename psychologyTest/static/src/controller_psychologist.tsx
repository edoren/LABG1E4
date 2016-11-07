var csrftoken = getCookie("csrftoken");

////////////////////////////////////////////////////////////////////////////////
// Test Management

var test_id = null;
var question_id = null;

function select_test(id) {
    test_id = id;
}

function select_question(id) {
    question_id = id;
    console.log("HOLA")
}

function remove_test() {
    if (test_id == null) return;
    window.location.href = "remove/?id=" + test_id;
}

function remove_question() {
    console.log("HOLA")
    if (question_id == null) return;
    window.location.href = "question/remove/?id=" + question_id;
}

////////////////////////////////////////////////////////////////////////////////
// Asignar Estudiantes

$("#group-select").change((eventData, handler) => {
    var selected_group = $("#group-select").val();
    var selected_student = $("#student-select").val();
    $("#student-select option").each((index, value) => {
        var user_group = $(value).attr("groupid");
        if (user_group == null) return;
        if (user_group == selected_group) {
            $(value).show();
        } else {
            $(value).hide();
        }
    })
})

////////////////////////////////////////////////////////////////////////////////
