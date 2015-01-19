$(document).ready( function() {
	$('#likes').click(function(){
		var planid;
		var username;
		var msgstr;
		planid = $(this).attr("data-planid");
		username = $(this).attr("data-username");
		$.get('/plan/like_plan/', {plan_id: planid, user_name: username}, function(data){
			$('#likes').hide();
			$('#favorite_string').html(data);
		});
	});
});