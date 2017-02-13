// 自执行函数 对checkbox绑定事件 在编辑模式下选中复选框直接将该行设置成编辑模式
$(function(){
    $('#tb').find(':checkbox').click(function(){
        var $tr = $(this).parent().parent();
        if($('#edit_mode').hasClass('editing')){
            if($(this).prop('checked')){
                RowIntoEdit($tr);
            }else{
                RowOutEdit($tr);
            }
        }
    });
});

globalEventContext = false;
// 监控是否按下Ctrl键 触发选择标签进行多选事件
window.onkeydown = function(event){
    if(event && event.keyCode == 17){
        globalCtrlKeyPress = true;
    }else{
        globalCtrlKeyPress = false;
    }
};

STATUS = [
  {'id':1, 'value':'在线'},
  {'id':2, 'value':'下线'}
];

SERVER = [
    {'id':1, 'value':'db数据库'},
    {'id':2, 'value':'zabbix监控'},
    {'id':3, 'value':'web负载均衡'}
];

// 全选函数 在编辑模式下全选会将剩余行也置于编辑模式
function CheckAll(mode, tb){
    // $('#tb input[type="checkbox"]').prop('checked',true);
    $(tb).children().each(function(){
        var ischecked=$(this).find(':checkbox').prop('checked');
        if(ischecked){
        }else{
            $(this).find(':checkbox').prop('checked', true);
            var isEditing=$(mode).hasClass('editing');
            if(isEditing){
                RowIntoEdit($(this));
            }
        }
    });
    }

// 取消函数 在编辑模式下取消会将该行从编辑模式设置为不可编辑
function CancleAll(mode, tb){
    // $('#tb input[type="checkbox"]').prop('checked',false);
    $(tb).children().each(function(){
        var ischecked=$(this).find(':checkbox').prop('checked');
        if(ischecked){
            $(this).find(':checkbox').prop('checked', false);
            var isEditing=$(mode).hasClass('editing');
            if(isEditing){
                RowOutEdit($(this));
            }
        }
    });
    }

// 反选函数 在编辑模式下反选：选中的行变为不可编辑 未选中的行变为可编辑
function ReverseAll(mode ,tb){
    $(tb).children().each(function(){
        var ischecked=$(this).find(':checkbox').prop('checked');
        if(ischecked){
            $(this).find(':checkbox').prop('checked', false);
            var isEditing=$(mode).hasClass('editing');
            if(isEditing){
                RowOutEdit($(this));
                }
            }else{
                $(this).find(':checkbox').prop('checked', true);
                var isEditing=$(mode).hasClass('editing');
                if(isEditing){
                    RowIntoEdit($(this));
                }
            }
    });
    }

// 编辑模式
function RowIntoEdit($tr){
    $tr.children().each(function(){
        if($(this).attr('edit')==='true'){
            if($(this).attr('edit-type')==='select'){
                var all_values = window[$(this).attr('global-key')];
                var select_val = $(this).attr('sle-val'); 
                select_val = parseInt(select_val);
                select_option = "";
                // 开始循环全局变量 STATUS 向select标签中添加option
                $.each(all_values, function(index, obj){
                    if(select_val == obj.id){
                        select_option += "<option select='selected'>"+obj.value+"</option>";
                    }else{
                        select_option += "<option>"+obj.value+"</option>";
                    }
                });
                // 添加event onchange事件 监控是否按下Ctrl键 进行多选
                var temp = "<select onchange='MultiSelect(this);'>"+select_option+"</select>";
            }else{
                var orgin_value = $(this).text();
                var temp = "<input value='"+orgin_value+"' />";
            }
            $(this).html(temp);
        }
    });
}

// 保存编辑
function RowOutEdit($tr){
    $tr.children().each(function(){
        if($(this).attr('edit')==='true'){
            var inp = $(this).children(':first');
            var inp_value = inp.val();
            $(this).text(inp_value);
        }
    });
}

// 编辑按钮
function edit_mode(ths,tb){
    var isediting =  $(ths).hasClass('editing');
    if(isediting){
        $(ths).text('进入编辑模式');
        $(ths).removeClass('editing');
        $(tb).children().each(function(){
            var $tr = $(this);
            if($(this).find(':checkbox').prop('checked')){
                RowOutEdit($tr);
            }
        });
    }else{
        $(ths).text('退出编辑模式');
        $(ths).addClass('editing');
        $(tb).children().each(function(){
            var $tr = $(this);
            var ischecked = $(this).find(':checkbox').prop('checked');
            if(ischecked){
                RowIntoEdit($tr);
        }
    });
    }
}

// 按住Ctrl键多选函数
function MultiSelect(ths){
    if(globalCtrlKeyPress === true){
        // 查找该元素在该行的索引 为了方便下面查找到同元素 即同一行tr中第几个td
        var index = $(ths).parent().index();
        // 该元素值 将查找到的同元素设置为该值
        var value = $(ths).val();
        $(ths).parent().parent().nextAll().find("td input[type='checkbox']:checked").each(function(){
        // eq取得对应索引位置的jquery对象 并设置值
        $(this).parent().parent().children().eq(index).children().val(value);
        });
    }
}
