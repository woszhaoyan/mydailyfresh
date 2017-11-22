/**
 * Created by zhaoyan on 2017/11/7.
 */

$(function () {

    var user_name_error = false;
    var passwd_error = false;
    var passwd_again_error = false;
    var email_error = false;
    var allow_error = false;


    //使用js对用户名进行失焦后，实时校验
    $('#user_name').blur(function () {
        user_name_check()
    })

    $('#user_passwd').blur(function () {
        passwd_check()
    })

    $('#user_passwd_again').blur(function () {
        passwd_again_check()
    })

    $('#user_email').blur(function () {
        email_check()
    })

    //两种实现方式:区别是什么，第一种只能触发一次
    $('#allow').click(function () {
        // allow_check()
        if($(this).is(':checked')){
            $(this).siblings('span').hide();
        }
        else {
            $(this).siblings('span').html("请您同意协议，否则无法注册")
            $(this).siblings('span').show()
        }
    })


    function user_name_check() {
        var len = $('#user_name').val().length;

        if(len < 5 || len > 20){
            $('#user_name').next().html('请输入5-20个字符的用户名');
            $('#user_name').next().show();
            user_name_error = true
        }
        else{
            $.get("/user/user_check/?user_name=" + $('#user_name').val(), function (data) {
                if (data.count == 1){
                    $('#user_name').next().html('您的用户名已经被使用');
                    $('#user_name').next().show();
                    user_name_error = true
                }
                else{
                    $('#user_name').next().hide();
                    user_name_error = false
                }
            })
        }
    }

    function passwd_check() {

        var len = $('#user_passwd').val().length;
        if(len < 6){
            $('#user_passwd').next().html('请输入大于5位的密码')
            $('#user_passwd').next().html();
            passwd_error = true;
        }else{
            $('#user_passwd').next().hide();
            passwd_error = false
        }
    }
    
    function passwd_again_check() {

        var u_passwd = $('#user_passwd')
        var u_passwd_again = $('#user_passwd_again')

        if(u_passwd.val() != u_passwd_again.val()){
            u_passwd_again.next().html('您两次输入的密码不一致');
            u_passwd_again.next().show();
            passwd_again_error = true
        }
        else{
            u_passwd_again.next().hide();
            passwd_again_error = false;
        }
    }

    function email_check() {
        //前端匹配邮箱的正则表达式
        var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
        var email = $('#user_email')

        if(re.test(email.val())){
            email.next().hide()
            email_error = false;
        }
        else{
            email.next().html('您输入的邮箱格式不正确')
            email.next().show()
            email_error = true;
        }
    }

    //保留仅仅是为了了解两种实现的区别
    function allow_check() {
        var allow = $('#allow')
        if(allow.is('checked')){
            allow.siblings('span').hide()
            allow_error = false;
        }else {
            allow.siblings('span').html("请您同意协议，否则无法注册")
            allow.siblings('span').show()
            allow_error = true;
        }
    }

    // 如果发生错误就不能提交
    $('#reg_form').submit(function () {
        user_name_check()
        passwd_check()
        passwd_again_check()
        email_check()

        if (user_name_error || passwd_again_error || passwd_error ||email_error || allow_error){
            return false;
        }else{
            return true;
        }
    })

})
