var selected_row = null;

$("#create_user").click(function () {
    if (selected_row == null) return;
    var childs = selected_row.children();
    var cont = 0;
    $.each(childs, function() {
        console.log(`${$(this).text()} - ${cont++}`);
    });
});

$("#table-select tbody > tr").click(function () {
    var is_selected = $(this).hasClass("selected");
    if (!is_selected) {
        $(this).addClass("selected").siblings().removeClass('selected');
        selected_row = $(this);
    }
});
