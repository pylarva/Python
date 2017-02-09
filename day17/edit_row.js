function CheckAll(){
            /*
            var tb = document.getElementById('tb');
            var trs = tb.children;
            for(var i=0;i<trs.length;i++){
                var current_tr = trs[i];
                var ck = current_tr.firstElementChild.firstElementChild;
                ck.setAttribute('checked','checked');
            }
            */
            $('#tb input[type="checkbox"]').prop('checked',true);
        }
        function CancleAll(){
            /*
            var tb = document.getElementById('tb');
            var trs = tb.children;
            for(var i=0;i<trs.length;i++){
                var current_tr = trs[i];
                var ck = current_tr.firstElementChild.firstElementChild;
                ck.removeAttribute('checked');
            }
            */
            $('#tb input[type="checkbox"]').prop('checked',false);
        }
        function ReverseAll(){
            /*
            var tb = document.getElementById('tb');
            var trs = tb.children;
            for(var i=0;i<trs.length;i++){
                var current_tr = trs[i];
                var ck = current_tr.firstElementChild.firstElementChild;
                if(ck.checked){
                    ck.checked = false;
                    ck.removeAttribute('checked');
                }else{
                    ck.checked = true;
                    ck.setAttribute('checked', 'checked');
                }
            }
            */
            $('#tb input[type="checkbox"]').each(function(i){
                // this  当前标签
                // $(this)当前标签的jQuery对象
                if($(this).prop('checked')){
                    $(this).prop('checked', false);
                }else{
                    $(this).prop('checked', true);
                }
            });
        }