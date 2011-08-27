(function(){
	var comments = $('#comments ul.comments li');
	
	function update_active()
	{
		comments.removeClass('active');
		if (document.location.hash.match(/^#comment_[\d]+$/))
			$(document.location.hash).addClass('active');
	}

	$(window).bind('hashchange', update_active);

	update_active();
})();
