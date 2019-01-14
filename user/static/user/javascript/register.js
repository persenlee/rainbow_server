var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".next").click(function(e){
    btn_id =  e.target.id;
    if(!validate(btn_id)) {
        return false;
    }
	if(animating) return false;
	animating = true;

	current_fs = $(this).parent();
	next_fs = $(this).parent().next();

	//activate next step on progressbar using the index of next_fs
	$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({
        'transform': 'scale('+scale+')',
        'position': 'absolute'
      });
			next_fs.css({'left': left, 'opacity': opacity});
		},
		duration: 800,
		complete: function(){
			current_fs.hide();
			animating = false;
			//show the next fieldset
			next_fs.show();
		},
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(".previous").click(function(){
	if(animating) return false;
	animating = true;

	current_fs = $(this).parent();
	previous_fs = $(this).parent().prev();

	//de-activate current step on progressbar
	$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");


	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale previous_fs from 80% to 100%
			scale = 0.8 + (1 - now) * 0.2;
			//2. take current_fs to the right(50%) - from 0%
			left = ((1-now) * 50)+"%";
			//3. increase opacity of previous_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({'left': left});
			previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
		},
		duration: 800,
		complete: function(){
			current_fs.hide();
			animating = false;
			//show the previous fieldset
			previous_fs.show();
		},
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});


$("#send_mail").click(function(e){
    e.preventDefault(); // cancel the link itself
    var email =$("#email").val();
    $.ajax({
        type: "POST", // 使用post方式
        url: "send_mail",
        data: {"email":email}, // 参数列表，stringify()方法用于将JS对象序列化为json字符串
        success: function(result){
        // 请求成功后的操作
            alert('邮件发送成功');
        },
        error: function(result){
        // 请求失败后的操作
            alert('邮件发送失败')
        }
    });
})

function validate(btn_id){
    if(btn_id == 'step1_next'){
        return validate_step1_next()
    }
    return true;
}


function validate_step1_next(){
    var email =$("#email").val();
    var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
    if (!reg.test(email)) {
        showValidate($("#email"));
//        alert('邮箱格式不正确，请重新填写!');
        return false;
    }

    var password = $("#password").val();
    if (password.length < 6) {
        showValidate($("#password"));
        return false;
    }
    var confirm_password = $("#confirm_password").val();
    if (confirm_password.length < 6) {
        showValidate($("#confirm_password"));
        return false;
    }

    if (password != confirm_password) {
        alert('密码不一致，请重新填写!');
        return false;
    }

    return true;
}




