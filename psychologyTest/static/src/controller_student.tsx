$(document).ready(() => {
    $("select.option").each((index, value) => {
        var $value = $(value);
        var selected = $value.attr("data-selected");
        $value.val(selected);
    });
});
