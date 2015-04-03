function select_gg(target) {
    target.off().on('click', escape_gg).addClass('down').removeClass('giveable takeable');
    $('.giveable').off().removeClass('giveable').addClass('holding');
    $('.takeable').off().removeClass('takeable').addClass('holding');
    $('.role.choosable').off().removeClass('choosable').addClass('holding')
    buttons_off();
    for (var i=0; i<48; i++) {
        if ( $('#station-'+String(i)).attr('class') === 'built' ) {
            if ( $('#'+String(i)).attr('class') === 'available' ) {
                $('#'+String(i)).off().attr('class', 'unavailable marked');
            } else {
                $('#'+String(i)).off().attr('class', 'unavailable');
            }
        } else {
            if ( $('#'+String(i)).attr('class') === 'available' ) {
                $('#'+String(i)).off().on('click', build_station).attr('class', 'selectable marked');
            } else {
                $('#'+String(i)).off().on('click', build_station).attr('class', 'selectable');
            }
        }
    }
    $('html').keyup( function( e ) {
        if (e.keyCode === 27) { escape_gg() };
    });
}

function escape_gg() {
    $.getJSON( $SCRIPT_ROOT + '/_escape_gg').success(
        function(data) {
            if ($('.down').length !== 0 ) {
                $('.marked').off().on('click', execute_move).attr('class', 'available');
                $('.selectable').off().attr('class', 'unavailable');
                set_treatable(String(data.position));
                buttons_on();
                $('html').off();
                escape_cards();
                reset_cards();
                console.log($('#scientist-card-50').attr('class'));
            }
        }
    ).error(function(error){console.log(error)});
}
