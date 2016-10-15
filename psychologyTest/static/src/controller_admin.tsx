function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie("csrftoken");

// Disable the modify and remove buttons if no row is selected
$("#modify-btn").prop("disabled", true);
$("#remove-btn").prop("disabled", true);

$("#create-btn").click(function() {
    $("form").trigger("reset");
    $("#formd-action").val("create");
    $("form .submit-button").text("Crear");
});

$("#modify-btn").click(function() {
    $("#formd-action").val("modify");
    $("form .submit-button").text("Editar");
});

$("#modify-btn.manage-users").click(function() {
    var selected_row = $("#table-select tbody > tr.selected");
    $("#formd-id").val(selected_row.attr("data-pk"));
    $("#formd-type-doc").val(selected_row.attr("data-type-doc"));
    $("#formd-no-doc").val(selected_row.attr("data-no-doc"));
    $("#formd-first-name").val(selected_row.attr("data-first-name"));
    $("#formd-second-name").val(selected_row.attr("data-second-name"));
    $("#formd-first-surname").val(selected_row.attr("data-last-name"));
    $("#formd-second-surname").val(selected_row.attr("data-second-surname"));
    $("#formd-born-date").val(selected_row.attr("data-born-date"));
    $("#formd-born-date-alt").val(selected_row.attr("data-born-date-alt"));
    $("#formd-gender").val(selected_row.attr("data-gender"));
    $("#formd-address").val(selected_row.attr("data-address"));
    $("#formd-phone").val(selected_row.attr("data-phone"));
    $("#formd-email").val(selected_row.attr("data-email"));
    $("#formd-password").val(selected_row.attr("data-password"));
    $("#formd-password-repeat").val(selected_row.attr("data-password"));
    $("#formd-role").val(selected_row.attr("data-role"));
    $("#formd-group").val(selected_row.attr("data-group"));
});

$("#modify-btn.manage-institutions").click(function() {
    var selected_row = $("#table-select tbody > tr.selected");
    $("#formd-id").val(selected_row.attr("data-pk"));
    $("#formd-nit").val(selected_row.attr("data-nit"));
    $("#formd-name").val(selected_row.attr("data-name"));
    $("#formd-address").val(selected_row.attr("data-address"));
    $("#formd-city").val(selected_row.attr("data-city"));
    $("#formd-phone").val(selected_row.attr("data-phone"));
    $("#formd-web-site").val(selected_row.attr("data-web-site"));
});

$("#modify-btn.manage-groups").click(function() {
    var selected_row = $("#table-select tbody > tr.selected");
    $("#formd-id").val(selected_row.attr("data-pk"));
    $("#formd-name").val(selected_row.attr("data-name"));
    $("#formd-institution").val(selected_row.attr("data-institution"));
    $("#formd-grade").val(selected_row.attr("data-grade"));
    $("#formd-schedule").val(selected_row.attr("data-schedule"));
});

$("form").on("submit", function() {
    if($("#formd-password").val() != $("#formd-password-repeat").val()){
        $("#form-alert").show();
        $("#error-text").text("Las contraseñas no son iguales.");
        return false;
    }
    window.location.replace(window.location.href);
    return true;
});

$("#dismiss-alert").click(function() {
    $("#form-alert").hide();
});

$("#confirm .remove").click(function() {
    var id = $("#table-select tbody > tr.selected").attr("data-pk");
    var postdata = {
        "action": "remove",
        "id": id,
        "csrfmiddlewaretoken": csrftoken
    }
    $("#confirm").modal("hide");
    $.post("", postdata); // POST request to the same view I am now
    window.location.replace(window.location.href);
});

$("#table-select tbody > tr").click(function() {
    var is_selected = $(this).hasClass("selected");

    // Enable Modify and Remove Buttons
    $("#modify-btn").prop("disabled", false);
    $("#remove-btn").prop("disabled", false);

    if (!is_selected) {
        $(this).addClass("selected").siblings().removeClass("selected");
    }

    var row_id = $("#table-select tbody > tr.selected").attr("data-pk");
});
