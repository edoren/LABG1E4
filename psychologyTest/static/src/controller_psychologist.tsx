$("#modify_user_btn").prop("disabled", true);
$("#remove_user_btn").prop("disabled", true);

$("#create_user").click(function () {
    var childs = $("#table-select tbody > tr.selected");
    console.log(childs);
    var cont = 0;
    $.each(childs, function() {
        console.log(`${$(this).text()} - ${cont++}`);
    });
});

$("#table-select tbody > tr").click(function () {
    var is_selected = $(this).hasClass("selected");

    // Enable Modify and Remove Buttons
    $("#modify_user_btn").prop("disabled", false);
    $("#remove_user_btn").prop("disabled", false);

    if (!is_selected) {
        $(this).addClass("selected").siblings().removeClass("selected");
        // selected_row = $(this);
    }
});
