function fit() {
	$('#map').css({
        position:'absolute',
        left: ($(window).width() - $('#map').outerWidth())/2,
        top: ($(window).height() - $('#map').outerHeight())/2
    });
}

$(window).load(fit);
$(window).resize(fit);
