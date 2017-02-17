(function(jq){
	jq.extend({
		valid:function(form){
			jq(form).find(':submit').click(function(){
				var ret_1 = Blur_1('#i1');
				if(ret_1 === false){
					return false;
				}
				var ret_2 = Blur_2('#i2');
				if(ret_2 === false){
					return false;
				}
				var ret_3 = Blur_3('#i3');
				if(ret_3 === false){
					return false;
				}
				var ret_4 = Blur_4('#i4');
				if(ret_4 === false){
					return false;
				}

				var ischecked = jq(form).find(':checkbox').prop('checked');
				if(ischecked === false){
				alert('请阅读并勾选用户协议...');
				return false;
				}

				// 不知道为什么不能用for循环 会出现ret 返回值 undefined
				// for (var a=1;a<5;i++){
				// 	var idd = "'" + "#i" + a + "'";
				// 	console.log(idd);
				// 	alert(idd);
				// 	var ret = Blur_i(idd);
				// 	// var ret = Blur_1('#i1');
				// 	alert(ret);
				// 	if(ret === false){
				// 		break;
				// 	}
				// }
				// return false;
			});
		}
	});
})(jQuery);

// 全局变量 设置初始密码空值
var pwd = '';

function Focus_1(ths){
	$('#t1').removeClass('error-color');
	$('#t1').text('支持中文、字母、数字、-、_组合 4-20个字符');
}

function Blur_1(ths){
	// $('#t1').text("");
	var user_name = $(ths).val();
	// alert(user_name.length);
	if(user_name.length === 0){
		$('#i1').next().addClass('display_no');
		$('#t1').text("用户名不能为空");
		$('#t1').addClass('error-color');
		return false;
	}
	if(user_name.length<4 || user_name.length>20){
		$('#i1').next().addClass('display_no');
		$('#t1').text('用户名长度为 4-20');
		$('#t1').addClass('error-color');
		return false;
	}else{
		$('#t1').text('');
		$('#i1').next().removeClass('display_no');
	}
}

function Focus_2(ths){
	$('#t2').removeClass('error-color');
	$('#t2').text('密码最小长度为6 建议至少使用2种字符');
}

function Blur_2(ths){
	// $('#t1').text("");
	var user_pwd = $(ths).val();
	// alert(user_name.length);
	if(user_pwd.length === 0){
		$('#i2').next().addClass('display_no');
		$('#t2').text("密码不能为空");
		$('#t2').addClass('error-color');
		return false;
	}
	if(user_pwd.length<6){
		$('#i2').next().addClass('display_no');
		$('#t2').text('密码长度不足6位');
		$('#t2').addClass('error-color');
		return false;
	}else{
		// 设置密码为全局变量 用来第二次确认密码
		pwd = user_pwd;
		$('#t2').text('');
		$('#i2').next().removeClass('display_no');
	}
}

function Focus_3(ths){
	$('#t3').removeClass('error-color');
	$('#t3').text('请再次输入密码');
}

function Blur_3(ths){
	// $('#t1').text("");
	var user_pwd = $(ths).val();
	// alert(user_name.length);
	if(user_pwd.length === 0){
		$('#i3').next().addClass('display_no');
		$('#t3').text("请再次输入密码");
		$('#t3').addClass('error-color');
		return false;
	}
	if(user_pwd != pwd){
		$('#i3').next().addClass('display_no');
		$('#t3').text('两次输入的密码不一致');
		$('#t3').addClass('error-color');
		return false;
	}else{
		$('#t3').text('');
		$('#i3').next().removeClass('display_no');
	}
}

function Focus_4(ths){
	$('#t4').removeClass('error-color');
	$('#t4').text('请输入手机号');
}

function Blur_4(ths){
	// $('#t1').text("");
	var user_phone = $(ths).val();
	// alert(user_name.length);
	if(user_phone.length === 0){
		$('#i4').next().addClass('display_no');
		$('#t4').text("手机号不能为空");
		$('#t4').addClass('error-color');
		return false;
	}
	var phoneReg = /^1[3|5|8]\d{9}$/;
	if(!phoneReg.test(user_phone)){
		$('#i4').next().addClass('display_no');
		$('#t4').text('手机号格式错误');
		$('#t4').addClass('error-color');
		return false;
	}else{
		$('#t4').text('');
		$('#i4').next().removeClass('display_no');
	}
}