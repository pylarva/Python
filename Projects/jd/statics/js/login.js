(function (jq) {
    jq.extend({
       valid:function (form) {
           jq(form).find(':submit').click(function () {
               var user_name = $('#i1').val();
               if(user_name.length === 0){
                  $('#t1').text('用户名为空...');
                  $('#t1').addClass('error_color');
                  return false;
               }
               if(user_name.length < 6){
                  $('#t1').text('用户名不小于6位...');
                  $('#t1').addClass('error_color');
                  return false;
               }
               var user_pwd = $('#i2').val();
               if(user_pwd.length === 0){
                   $('#t2').text('密码为空...');
                   $('#t2').addClass('error_color');
                   return false;
               }
               if(user_pwd.length < 6){
                   $('#t2').text('密码不小于6位...');
                   $('#t2').addClass('error_color');
                   return false;
               }
           });
       }
    });
})(jQuery);
