// 保存选中的数据
var selectData;

//为模态对话框添加拖拽
$("#modalDialog").draggable({cursor: "move",handle: '.modal-header'});
	
/**
 * 使用递归遍历json字符串，生成树结构
 * @param  {[type]} tData json字符串
 * @return {[type]}       返回树结构
 */
function loadTree(tData){
	var ul = $('<ul>');
	for(var i=0; i<tData.length; i++){
		var li = $('<li>').appendTo(ul);
		var node = $('<a>').appendTo(li);
		var icon = $('<i>').css('margin-right','5').appendTo(node);
		var aTree = $('<span>').html(tData[i].title).css({'cursor': 'pointer'}).appendTo(node);
		var aStr = 'checkFile(' + tData[i].field + ')';
		aTree.attr('onclick', aStr);
		var input = $('<input>').addClass('field').val(tData[i].field).css({'display':'none'}).appendTo(node);

		// 处理有子节点的
		if(tData[i].children != undefined){
			// 添加图标样式
			icon.addClass('fa fa-minus-square-o');
			var ic = $('<i>').addClass('fa fa-folder-open-o');
			icon.after(ic).addClass('status');
			node.addClass('tree-node');
			
			// 添加标记节点是否打开
			$('<input>').addClass('open').val(tData[i].open).css('display','none').appendTo(node);

			// 递归遍历子节点
			loadTree(tData[i].children).appendTo(li);
		} else{
			icon.addClass('fa fa-file-text-o');
			// 叶子节点新增是否可选
			$('<input>').addClass('candidate').val(tData[i].candidate).css('display','none').appendTo(li);
		}
	}
	return ul;
}

/**
 * 节点点击事件
 * @param  {[type]} box 存在菜单树的盒子
 */
function nodeClick(box){
	box.find('.tree-node').click(function(){
		// 判断该节点是否开启
		if($.trim($(this).find('.open').val()) == 'true'){
			// 已开启，则关闭节点
			$(this).next().slideUp(500);
			$(this).find('.open').val('false');
			$(this).find('.status').removeClass('fa-minus-square-o').addClass('fa-plus-square-o');
		} else{
			// 开启前关闭节点下的所有节点
			$(this).next().find('.tree-node').each(function(){
				$(this).next().css('display','none');
				$(this).find('.open').val('false');
				$(this).find('.status').removeClass('fa-minus-square-o').addClass('fa-plus-square-o');
			})

			// 已关闭，则开启节点
			$(this).find('.open').val('true');
			$(this).find('.status').removeClass('fa-plus-square-o').addClass('fa-minus-square-o');
			// 开启节点下的节点
			
			$(this).next().slideDown(500);
		}
	})
}

/**
 * 将数据转换成表格
 * @param  {[type]} tData json类型数组: 
 *                        [{title:'title', field:'field', candidate: true/false},
 *                         {title:'title', open:true/false, children:[{}...{}]} ]
 * @return {[type]}       返回由数据转换出来的table
 */
function loadTreeTable(tData){
	var outCol = tData.length;
	var treeTable = $('<table cellspacing="0" cellpadding="0" border="1">').css('border-collapse','collapse').addClass('tree-table');
	var trTitle = $('<tr>').addClass('tr-title').appendTo(treeTable);
	var trContent = $('<tr>').addClass('tr-content').appendTo(treeTable);

	// 遍历叶子节点
	for(var i=0; i<tData.length; i++){
		var childTable = undefined;
		if(tData[i].children != undefined && tData[i].children.length > 0){
			// 递归遍历子节点
			childTable = loadTreeTable(tData[i].children);
			// 去除内联表格的边框效果
			childTable.css({'border-width':'0px', 'border-style':'hidden'})

			// 获取子表的节点行
			var childTrTitle = childTable.find('.tr-title').first();
			$('<td>').addClass('td-title').attr('colspan',tData[i].children.length).html(tData[i].title).appendTo(childTrTitle);

			// 将子表加入
			$('<td>').addClass('t-node-table').html(childTable).appendTo(trContent);
		} else{
			var td = $('<td>').appendTo(trContent);
			$('<span>').html(tData[i].title).appendTo(td);
			if(tData[i].candidate != undefined && (tData[i].candidate == false || tData[i].candidate == 'false')){
				td.addClass('t-select t-default');
			}

			// 存在节点信息
			$('<input>').addClass('candidate').css('display','none').val(tData[i].candidate).appendTo(td);
			$('<input>').addClass('field').css('display','none').val(tData[i].field).appendTo(td);
			td.addClass('t-leaf');
		}
	}

	return treeTable;
}

/**
 * 递归取消选中
 * @param  {[type]} td 点击的元素
 * @return {[type]}    [description]
 */
function cancelSelect(td){
	var isAllSelect = true;
	// 判断同级的叶子节点状态
	td.parent().find('.t-leaf').each(function(){
		if($(this).find('.candidate').val() == false || $.trim($(this).find('.candidate').val()) == 'false'){
			isAllSelect = false;
			return isAllSelect;
		}
	})

	// 获取表格标题行
	var trTitle = td.parent().prev();
	var parentTd = trTitle.parent().parent();

	if(isAllSelect != false){
		trTitle.find('.td-title').removeClass('t-select');
		cancelSelect(parentTd);
	}
}

/**
 * 组装选中的表格数据
 * @return {[type]} 返回json类型数组: 
 *                        [{title:'title', field:'field', candidate: true/false},
 *                         {title:'title', open:true/false, children:[{}...{}]} ]
 */
function packDataNode(table){
	var parentData;
	var childData = [];

	var titleContent = table.find('.tr-title').first().children('.t-select').html();

	// 遍历叶子节点
	table.find('.tr-content').first().children('.t-select').each(function(){
		childData.push({title:$.trim($(this).find('span').html()), 
			field:$(this).find('.field').val(),
			candidate:$(this).hasClass('t-default')?false:true}); // 处理默认编码不可选
	})

	// 递归节点下的数据
	table.find('.tr-content').first().children('.t-node-table').each(function(){
		if($(this).find('table').first().find('.td-title').first().hasClass('t-select')){
			childData.push(packDataNode($(this).find('table').first()));
		}
	})

	// 处理标题,并将子节点附加到父节点
	if(titleContent!=undefined && $.trim(titleContent) != '' && childData.length > 0){
		parentData = {title:titleContent, open:true, children:childData};
	} else{
		return childData;
	}

	return parentData;
}

/**
 * 表格点击事件
 */
function tableClick(){
	// 保存选中的数据
	var newData = [{title:'编码', field: "code",candidate: false}];
	// 点击某个叶子点
	$('.t-leaf').click(function(){
		if($.trim($(this).find('.candidate').val()) == 'true' || $(this).find('.candidate').val() == true){
			// 选中该项
			$(this).addClass('t-select');
			$(this).find('.candidate').val('false');

			// 该项对应的标题节点样式改变
			$(this).parents('.tr-content').prev().find('.td-title').addClass('t-select');
		} else{
			// 取消选中
			$(this).removeClass('t-select');
			$(this).find('.candidate').val('true');
			
			cancelSelect($(this));
		}

		// 绘制新表格
		$('#select_tree_table').empty();
		selectData = packDataNode($('#tree_table>.tree-table'));
		$('#select_tree_table').append(loadTreeTable(selectData));
	})

	// 点击节点选中节点下所有数据
	$('.td-title').click(function(){
		// 判断节点下的是否全部选中
		var isAllSelect = true;
		$(this).parent().next().find('.t-leaf').each(function(){
			if($.trim($(this).find('.candidate').val()) == 'true'){
				isAllSelect = false;
				return isAllSelect;
			}
		})

		if(isAllSelect == false){
			// 点击节点-节点下的全选
			$(this).parent().parent().find('.t-leaf,.td-title').addClass('t-select');
			$(this).parent().parent().find('.t-leaf').each(function(){
				$(this).find('.candidate').val('false');
			})
			$(this).parents('.tr-content').prev().find('.td-title').addClass('t-select');
		} else{
			// 点击节点-节点下的全部取消
			$(this).parent().parent().find('.t-leaf,.td-title').removeClass('t-select');
			$(this).parent().parent().find('.t-leaf').each(function(){
				// alert()
				$(this).find('.candidate').val('true');
			})
			cancelSelect($(this).parent().parent().parent());
		}

		// 绘制新表格
		$('#select_tree_table').empty();
		selectData = packDataNode($('#tree_table>.tree-table'));
		$('#select_tree_table').append(loadTreeTable(selectData));
	})
}

/**
 * 选中节点的结果集
 * @param  {[type]} data 
 * @return {[type]} 返回 feild数组
 */
function result(selData){
	var datas = new Array();

	for(var i=0; i<selData.length; i++){
		if(selData[i].children != undefined && selData[i].children.length > 0){
			var child = result(selData[i].children);
			// 递归遍历子节点
			for(var j=0; j<child.length; j++){
				datas.push(child[j]);
			}
		} else{
			if(selData[i].field != 'code'){
				datas.push('\"' + selData[i].field + '\"');
			}
		}
	}

	return datas;
}