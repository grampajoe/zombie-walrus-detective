(function(){
	var share_button = $('#share_button');
	var share_box = $('#share');

	$(share_button).click(function(){
		var pos = $(share_button).position();
		$(share_box).css('left', pos.left + 'px');
		$(share_box).css('top', (pos.top + 20) + 'px');
		$(share_box).toggle();
		return false;
	});

	$(document.body).click(function(){
		$(share_box).hide();
	});

	$(share_box).click(function(){ return false; });
})();
