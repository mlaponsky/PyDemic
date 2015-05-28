function pulse_svg(city) {
    var map = Snap.select('#cities');
    var icon = map.select('#city-'+String(city));
    icon.stop().attr({'fill': COLOR_CODES[Math.floor(city/12)],
               'stroke-width': 2})
               .animate({'stroke-width': 10}, 800, function() {
                    icon.animate({'stroke-width': 2}, 800, function() {
                        pulse_svg(city);
                    });
               });
}

function flash_svg(city, loop) {
    var map = Snap.select('#cities');
    var icon = map.select('#city-'+String(city));
    icon.stop().attr({'fill': COLOR_CODES[Math.floor(city/12)],
               'stroke-width': 2})
               .animate({'fill': '#fffff0'}, 800, function() {
                   icon.animate({'fill': COLOR_CODES[Math.floor(city/12)]}, 800, function() {
                       if (loop) {
                           flash_svg(city, true);
                       }
                   });
               });
}

function stop_svg(city) {
    var map = Snap.select('#cities');
    var icon = map.select('#city-'+String(city));
    icon.stop().attr({'fill': COLOR_CODES[Math.floor(city/12)],
                      'stroke-width': 2});
}

function set_cities(cities) {
	var map = Snap.select('#cities');

	map.selectAll('.available').forEach( function(el) {
		el.unavailable();
	});
	map.selectAll('.selectable').forEach( function(el) {
		el.unavailable();
	});
	map.selectAll('.selected').forEach( function(el) {
		el.unavailable();
	});
    for (var i=0; i<cities.length; i++) {
        map.select('#city-'+String(cities[i])).available();
    }
}

function set_treatable(position) {
	var map = Snap.select('#cities');
    if ( $(".city-"+position).length !== 0 ) {
        map.select("#city-"+position).treatable();
    } else {
        map.select("#city-"+position).unavailable();
    }
}
