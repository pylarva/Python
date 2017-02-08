(function(jq){

	function ErrorMessage(inp, message){
        var tag = document.createElement('span');
        tag.innerText = message;
        inp.after(tag);
	}

	jq.extend({
		valid:function(form){
		// #form1 $('#form1')
		jq(form).find(':submit').click(function(){
			jq(form).find('.item span').remove();
			var flag = true;

			jq(form).find(':text, :password').each(function(){

				var require = $(this).attr('require');
				if(require){
					var val = $(this).val();
    				var label = $(this).attr('label');

    				if(val.length<=0){
						ErrorMessage($(this), label + "不能为空");
	    				flag = false;
	    				return false;
    				}

    				var minLen = $(this).attr('min-len');
    				if(minLen){
    					var minLenInt = parseInt(minLen);
    					if(val.length<minLenInt){
    						ErrorMessage($(this), label + "最小长度为" + minLen);
		    				flag = false;
		    				return false;
    					}
    				}

    				var phone = $(this).attr('phone');
    				if(phone){
    					console.log(111);
    					var phoneReg = /^1[3|5|8]\d{9}$/;
    					if(!phoneReg.test(val)){
    						ErrorMessage($(this), label + "格式错误");
		    				flag = false;
		    				return false;
    					}
    				}
				}

			});
			return flag;
		});
		}
	});
})(jQuery);