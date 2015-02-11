/**
 * @author max
 */
function sizeGame() {
	var raw_image_w = 4378;
	var raw_image_h = 2185;
	var image_ratio = raw_image_w / raw_image_h;
	
	var screen_w = $(window).width();
	var screen_h = $(window).height();
	var screen_ratio = screen_w / screen_h;
	
	if (image_ratio >= screen_ratio) {
		$("#map").width(screen_w).height(screen_w*(1/image_ratio));
	} else {
		$("#map").width(screen_h*image_ratio).height(screen_h);
	}
};

$( window ).load(sizeGame);
$( window ).resize(sizeGame);
