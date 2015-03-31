/**
 * @author max
 */
var left_offset;
var top_offset;
var menu_shift;

function sizeGame() {
	var raw_image_w = 4378;
	var raw_image_h = 2185;
	var image_ratio = raw_image_w / raw_image_h;

	var screen_w = $(window).width();
	var screen_h = $(window).height();
	var screen_ratio = screen_w / screen_h;

	menu_shift = screen_w*0.06;

	if (image_ratio >= screen_ratio) {
		$("#map").width(screen_w).height(screen_w*(1/image_ratio));
	} else {
		$("#map").width(screen_h*image_ratio).height(screen_h);
	}
};

function fit() {
	$('#map').css({
        position:'absolute',
        left: ($(window).width() - $('#map').outerWidth())/2,
        top: ($(window).height() - $('#map').outerHeight())/2
    });
	left_offset = ($(window).width() - $('#map').outerWidth())/2;
	top_offset = ($(window).height() - $('#map').outerHeight())/2;
	console.log(top_offset);
	console.log(left_offset);
}

$(window).load(function() {	sizeGame();
							fit();
							initial_load();
							});
$(window).resize(function() {
	 						sizeGame();
							});
