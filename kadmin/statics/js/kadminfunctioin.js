function MoveSelectedOption(ele, target_id) {

    var new_target_id = $(ele).parent().attr('id');
    var option = "<option value='" + $(ele).val() + "'ondblclick=MoveSelectedOption(this,'" + new_target_id + "') >" + $(ele).text() + "</option>";
    $("#" + target_id).append(option);
    $(ele).remove();

}

function MoveAllElements(from_id, to_id) {

    console.log($("#" + from_id).children())
    $("#" + from_id).children().each(function () {
        MoveSelectedOption(this, to_id);
    })
}

function FuzzSearch(ele) {

    console.log($(ele).val())
    var search_text = $(ele).val().toUpperCase();
    $(ele).next().children().each(function () {
        if ($(this).text().toUpperCase().search(search_text) != -1) {
            $(this).show();
        } else {
            $(this).hide();
        }
    })

}

function VerificationBeforeFormSubmit() {


    $("select[tag] option").prop('selected', true);

}

function SelectAllObjs(ele) {

    if ($(ele).prop('checked')){
        $('input[row-select]').prop('checked',true)

    }else {
        $('input[row-select]').prop('checked',false)
    }


}


function ActionCheck(ele){
    var selected_action = $("select[name='action']").val();
    var selected_objs = $("input[row-select]").filter(":checked");
    console.log($("select[name='action']").val())
    if (!selected_action){
        alert("no action selected!")
        return false
    }
    if (selected_objs.length == 0 ){
        alert("no object selected!")
        return false
    }else {
        //生成一个标签,放到form里

        var selected_ids = [];
        $.each(selected_objs,function () {
            console.log($(this) );
            selected_ids.push($(this).val())
        })
        console.log(selected_ids)
        var input_ele = "<input type='hidden' name='selected_ids' value=" + JSON.stringify(selected_ids) + ">"

        $(ele).append(input_ele);
    }
    //return false



}