(function(){
	var share_button = document.getElementById('share_button');
	var share_box = document.getElementById('share');
	
	function getPos(obj)
	{
		var pos = [0,0];
		if (obj.offsetParent)
		{
			do {
				pos = [pos[0] + obj.offsetLeft, pos[1] + obj.offsetTop];
			} while (obj = obj.offsetParent);
		}
		return pos;
	}

	share_button.onclick = function(){
		var pos = getPos(share_button);
		share_box.style.left = pos[0] + 'px';
		share_box.style.top = (pos[1] + 20) + 'px';
		share_box.style.display = (share_box.style.display == 'block') ? 'none' : 'block';
		return false;
	};
})();
