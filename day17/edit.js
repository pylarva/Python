STATUS = [
    {'id': 1, 'text': "在线"},
    {'id': 2, 'text': "下线"}
];

BUSINESS = [
    {'id': 1, 'text': "车商会"},
    {'id': 2, 'text': "二手车"},
];

function CheckAll(mode,tb){
    //1、选中checkbox
    //2、如果已经进入编辑模式，让选中行进入编辑状态
    //tb = #tb1
    //$(tb) = $('#tb1')
    $(tb).children().each(function(){
        //$(this)表示循环过程中，每一个tr，每一行数据
        var tr=$(this);
        var isChecked = $(this).find(':checkbox').prop('checked');
        if(isChecked===true){
        }else{
            $(this).find(':checkbox').prop('checked',true);
            //如果已经进入编辑模式，让选中行进入编辑状态；
            var isEditMode = $(mode).hasClass('editing');
            if(isEditMode){
                RowEditInMode(tr);
            }
        }
    });
}

function CheckCancel(mode,tb){
    //1、取消选中checkbox
    //2、如果已经进入编辑模式，行退出编辑状态；
    $(tb).children().each(function(){
        var tr=$(this);
        if(tr.find(':checkbox').prop('checked')){
            //移除选中
            tr.find(':checkbox').prop('checked',false);
            var isEditing=$(mode).hasClass('editing');
            if(isEditing === true){
                //当前行，退出编辑状态；
                RowEditOutMode(tr);
            }
        }
    });
}

function CheckReverse(mode,tb){
    if($(mode).hasClass('editing')){
        $(tb).children().each(function(){
            var tr = $(this);
            var check_box = tr.children().first().find(':checkbox');
            if(check_box.prop('checked')){
                check_box.prop('checked',false);
                //##################相似代码################
                RowEditOutMode(tr);
                //##########################################
            }else{
                check_box.prop('checked',true);
                //##################相似代码################
                RowEditInMode(tr);
                //##########################################
            }
        });
    }else{
        $(tb).children().each(function(){
            var tr = $(this);
            var check_box = tr.children().first().find(':checkbox');
            if(check_box.prop('checked')){
                check_box.prop('checked',false);
            }else{
                check_box.prop('checked',true);
            }
        });
    }
}

function EditMode(ths,tb){
    var isEditing  = $(ths).hasClass('editing');
    if (isEditing){
        //当前为编辑模式，点击触发了此函数，退出编辑模式；把……
        $(ths).text("进入编辑模式");
        $(ths).removeClass('editing');
        $(tb).children().each(function(){
            var tr=$(this);
            if(tr.find(':checkbox').prop('checked')){
                RowEditOutMode(tr);
            }
        });
    }else{
        $(ths).text("退出编辑模式");
        $(ths).addClass('editing');
        $(tb).children().each(function(){
            //$(this)表示循环过程中，每一个tr，每一行数据
            var tr=$(this);
            var isChecked = $(this).find(':checkbox').prop('checked');
            if(isChecked===true){
                RowEditInMode(tr);
            }
        });
    }
}

function RowEditInMode(tr){
    tr.children().each(function(){
        var td=$(this);
        if(td.attr('edit')=='true'){
            if(td.attr('edit-type')=="select"){
                var all_values = window[td.attr('global-key')];
                var select_val = td.attr('select-val');
                select_val = parseInt(select_val);  //字符串转数字
                var options = "";
                $.each(all_values,function(index,value){
                    if(select_val == value.id){
                        options += "<option selected='selected'>"+value.text+"</option>";
                    }else{
                        options += "<option>"+value.text+"</option>";
                    }
                });
                var temp = "<select onchange='MultiChange(this);'>"+options+"</select>";
            }else{
                var text=td.text();
                var temp = "<input type='text' value='"+text+"' />";
            }
            td.html(temp);
        }
    });
}

function RowEditOutMode(tr){
    tr.children().each(function(){
        var td=$(this);
        if(td.attr('edit')=='true'){
            var inp = td.children(":first");
            var input_value = inp.val();
            td.text(input_value);
        }
    });
}
/*************************编辑模式中选择一个进行编辑***************************/
$(function(){
    $("#tb1").find(':checkbox').click(function(){
        var tr = $(this).parent().parent();
        if($("#edit_mode").hasClass('editing')){
            if($(this).prop("checked")){
                //当前行进入编辑状态
                RowEditInMode(tr);
            }else{
                //当前行退出编辑状态
                RowEditOutMode(tr);
            }
        }
    });
});

/*************************multi_select_change_ctrl***************************/
globalCtrlKeyPress = false;
//如果按下键盘的任意键，执行function
window.onkeydown = function(event){
    //console.log(event.keyCode);
    if(event && event.keyCode == 17){
        window.globalCtrlKeyPress = true;
    }else{
        window.globalCtrlKeyPress = false;
    }
};

function MultiChange(ths){
    //检测是否按下ctrl建
    if(window.globalCtrlKeyPress === true){
        //td所在的tr中的索引位置
        var index = $(ths).parent().index();
        var value = $(ths).val();
        $(ths).parent().parent().nextAll().find("td input[type='checkbox']:checked").each(function(){
        $(this).parent().parent().children().eq(index).children().val(value);
        });
    }
}