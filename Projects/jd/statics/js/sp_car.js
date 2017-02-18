// 购物车js

function check_sum(ths){
	var ischecked = $(ths).prop('checked');
	var sum = $(ths).parent().next().next().next().next().next().text();
	reg = /\d+.\d+/;
	sum = reg.exec(sum)[0];
	sum = parseFloat(sum);
	var orgin = $('#s4-2').text();
	orgin = reg.exec(orgin)[0];
	orgin = parseFloat(orgin);
	if(ischecked){
		orgin += sum;
	}else{
		orgin -= sum;
	}
	$('#s4-2').text("总价为：" + orgin + "元");

}

// 选择商品加入购物车
function Goods_add(ths){
	var good_name = $(ths).find('p').text();
	var price = $(ths).find('a').text();
	var image = $(ths).attr("picture");
	var temp = $('#template').clone();
	$('#body-topic').append(temp);
	// alert(good_name);
	// alert(price);
	// alert(image);


	$('#d2').find('img').attr("src", image);
	$('#d3').text(good_name);
	$('#d4').text(price);
	$('#d6').text(price);
	$('#template').removeClass('hide');
	// 给商品div添加一个isgood属性 为了使用jquery找出所有商品并统计总价格
	$('#template').find(':checkbox').attr('isgood', 'true');
}

// 商品数量输入框取消激活时检查数字有效性并计算总价格
function Blur(ths){
	var n = $(ths).val();
	var price = $(ths).parent().parent().prev().text();
	reg = /\d+.\d+/;
	price = reg.exec(price)[0];
	n = parseInt(n);
	if(isNaN(n)||n<1){
		alert('非法数值，商品数量不能小于1...');
		$(ths).val(1);
	}else{
		n = $(ths).val();
		// n = parseInt(n);
		$(ths).parent().parent().next().text(price*n);
	}
	// alert(n);
	// price = 
}

function Reduce_num(ths){
	var n = $(ths).next().val();
	var price = $(ths).parent().parent().prev().text();
	reg = /\d+.\d+/;
	price = reg.exec(price)[0];
	n = parseInt(n);
	if(n<=1){
		alert('商品数量不能小于1...');
	}else{
		$(ths).next().val(n-1);
		n = $(ths).next().val();
		// n = parseInt(n);
		$(ths).parent().parent().next().text(price*n);
		var ischecked = $(ths).parent().parent().parent().first().find(':checkbox').prop('checked');
		// alert(ischecked);
		if(ischecked){
		var orgin = $('#s4-2').text();
		price = parseFloat(price);
		orgin = reg.exec(orgin)[0];
		orgin = parseFloat(orgin);
		orgin -= price;
		$('#s4-2').text("总价为：" + orgin + "元");
	}
	}
}

function Add_num(ths){
	var n = $(ths).prev().val();
	var price = $(ths).parent().parent().prev().text();
	reg = /\d+.\d+/;
	price = reg.exec(price)[0];
	n = parseInt(n);
	$(ths).prev().val(n+1);
	n = $(ths).prev().val();
	$(ths).parent().parent().next().text(price*n);
	var ischecked = $(ths).parent().parent().parent().first().find(':checkbox').prop('checked');
	// alert(ischecked);
	if(ischecked){
		var orgin = $('#s4-2').text();
		price = parseFloat(price);
		orgin = reg.exec(orgin)[0];
		orgin = parseFloat(orgin);
		orgin += price;
		$('#s4-2').text("总价为：" + orgin + "元");
	}
}

function Check_all(ths){
	var ischecked=$(ths).prop('checked');
	reg = /\d+.\d+/;
	var sum = 0;
	// alert(ischecked);
	if(ischecked){
		$('#c1').parent().parent().parent().children().find("input[type='checkbox']").prop('checked', true);
		$('#c1').parent().parent().parent().children().find("input[type='checkbox']").each(function(){
			var isgoods = $(this).attr('isgood');
			if(isgoods){
				unit = $(this).parent().next().next().next().next().next().text();
				unit = reg.exec(unit);
				unit = parseFloat(unit);
				sum += unit;
				$('#s4-2').text("总价为：" + sum + "元");
			}
		});
	}else{
		$('#c1').parent().parent().parent().children().find("input[type='checkbox']").prop('checked', false);
		$('#s4-2').text("总价为：" + 0 + "元");
	}
}

function delete_unit(ths){
	$(ths).parent().parent().parent().addClass('hide');
	var ret = $(ths).parent().parent().parent().children().find(':checkbox').prop('checked');
	var sum = $(ths).parent().parent().prev().text();
	reg = /\d+.\d+/;
	sum = reg.exec(sum)[0];
	sum = parseFloat(sum);
	var orgin = $('#s4-2').text();
	orgin = reg.exec(orgin)[0];
	orgin = parseFloat(orgin);
	if(ret){
		orgin -= sum;
		$('#s4-2').text("总价为：" + orgin + "元");
	}else{
	}
}