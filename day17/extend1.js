// js插件扩展方式优势： 自执行 + 闭包（变量封装在自己函数里面）
(function(jq){
	jq.extend({
		'dalong':function(arg){
			console.log(arg);
		}
	});

	function f1(){

	}
})(jQuery);