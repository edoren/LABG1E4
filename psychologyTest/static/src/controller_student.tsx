$(document).ready(() => {
    $("select.answer-option").each(function() {
        var $this = $(this);
        var selected = $this.data("selected");
        $this.val(selected);
    });
});

$("select.answer-option").click(function() {
    $(this).data("oldval", $(this).val());
});

$("select.answer-option").change(function() {
    var select_changed = $(this);
    var curr_val = $(this).val();
    var old_val = $(this).data("oldval");

    var answer_id = $(this).data("answer");
    $(".answer").find(`select[data-answer="${answer_id}"]`).each(function () {
        var select_in_check = $(this);
        if (select_changed.is(select_in_check)) return;
        if (select_in_check.val() == select_changed.val()) {
            select_in_check.val(old_val);
        }
    });
});
