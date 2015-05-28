function select_gg(target) {
    var map = Snap.select('#cities');
    target.off().on('click', escape_gg).addClass('down').removeClass('giveable takeable trashable');
    board_off();

    buttons_off();
    for (var i=0; i<48; i++) {
        if ( $('#station-'+String(i)).attr('class') === 'built' ) {
            if ( map.select('#city-'+String(i)).hasClass('available') ) {
                map.select('#city-'+String(i)).unavailable();
                map.select('#city-'+String(i)).addClass('marked');
            } else {
                map.select('#city-'+String(i)).unavailable();
            }
        } else {
            if ( map.select('#city-'+String(i)).hasClass('available') ) {
                map.select('#city-'+String(i)).selectable();
                map.select('#city-'+String(i)).addClass('marked')
            } else {
                map.select('#city-'+String(i)).selectable();
            }
        }
    }
    $('html').keyup( function( e ) {
        if (e.keyCode === 27) { escape_gg() };
    });
}

function escape_gg() {
    var map = Snap.select('#cities');
    $.getJSON( $SCRIPT_ROOT + '/_escape_gg').success(
        function(data) {
            if ( $('.down').length !== 0 && TRASHING === 0 ) {
                map.selectAll('.marked').forEach( function(el) {
            		el.available();
            	});
                map.selectAll('.selectable').forEach( function(el) {
            		el.unavailable();
            	});
                set_treatable(String(data.position));
                $('html').off();
                board_on();
                buttons_on();
            } else if ( TRASHING === 1 ) {
                $('.down').off().on('click', trash).addClass('trashable').removeClass('down');
                $('.holding-t').off().on('click', trash).addClass('trashable').removeClass('holding-t');
                map.selectAll('.selectable').forEach( function(el) {
            		el.unavailable();
            	});
                $('html').off();
            }
        }
    ).error(function(error){console.log(error)});
}
