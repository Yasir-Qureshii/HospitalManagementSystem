$(document).ready(function () {
	$(".btn_approve").click(function(){
    $(".hide_this").css('opacity', 0);
    $(".patient_msg").hide();
    $(".more_info").hide();
    $(".disapprove").hide();
    $(".approve").fadeIn(700);

}); 
	$(".btn_disapprove").click(function(){
    $(".approve").hide();
    $(".patient_msg").hide();
    $(".more_info").hide();
    $(".disapprove").fadeIn(700);

});
	$(".btn_more_info").click(function(){
    $(".approve").hide();
    $(".patient_msg").hide();
    $(".disapprove").hide();
    $(".more_info").fadeIn(700);
});
	$(".btn-close").click(function(){
    $(".tr-close").hide();
});
	$(".btn-close1").click(function(){
    $(".tr-close1").hide();
});
	$(".btn-close2").click(function(){
    $(".tr-close2").hide();
});
	$(".btn-new").click(function(){
    $("#past").hide();
    $("#default").hide();
    $("#new").fadeIn(600);
});

	$(".btn-default").click(function(){
    $("#new").hide();
    $("#past").hide();
    $("#default").fadeIn(600);
});
	$(".btn-past").click(function(){
    $("#new").hide();
    $("#default").hide();
    $("#past").fadeIn(600);
});
    $(".btn-accounts").click(function(){
    $(".login").hide();
    $(".accounts").removeClass("invisible");
});
    $(".btn-login").click(function(){
    $(".accounts").addClass("invisible");
    $(".login").fadeIn(600);
});
    setTimeout(function(){
        $('#paint').addClass("invisible");
    }, 8000);

$('.chatbox').scrollTop($('.chatbox')[0].scrollHeight);

})
