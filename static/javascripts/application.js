$(document).ready(function(){$(".scroll").on("click touchstart",function(o){o.preventDefault();var i=0;i=$(this.hash).offset().top>$(document).height()-$(window).height()?$(document).height()-$(window).height():$(this.hash).offset().top,$("html,body").animate({scrollTop:i},1e3,"swing")}),$(".modal-close svg").click(function(){$(".join").removeClass("overlay-visible")}),$("#join-yazlo form").submit(function(){return email=$("#join-yazlo form input[type=email]").val(),email&&""!=email.trim()?($("#join-yazlo form input[type=email]").css("border-color","white"),$(".join").addClass("overlay-visible")):$("#join-yazlo form input[type=email]").css("border-color","#ff4c4c"),!1}),$("#modal-row button[type=submit]").click(function(){captcha_response=$(".g-recaptcha-response").val(),$("#modal-row img").css("display","inline"),$.get("/verifycaptcha",{response:captcha_response,email:$("#join-yazlo form input[type=email]").val()},function(o){$(".join-result").addClass("join-result-show"),$("#modal-row img").css("display","none"),1==o.success?($(".join-result").css("color","#00b200"),$(".join-result").html("<span class='glyphicon glyphicon-ok'></span> Email sent. Check your inbox to activate your account.")):($(".join-result").css("color","rgba(255, 0, 0, 0.8)"),$(".join-result").html("<span class='glyphicon glyphicon-alert'></span> Error encountered in registering email."))})})});