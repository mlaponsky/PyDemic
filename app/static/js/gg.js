function select_gg() {
    $(this).off().on('click', escape_gg).attr('class', 'pl-card down');
    $('.giveable').off().attr('class', 'pl-card holding');
    $('.takeable').off().attr('class', 'card marked');
    buttons_off();
    for (var i=0; i<48; i++) {
        if ( $('#station-'+String(i)).attr('class') === 'built' ) {
            if ( $('#'+String(i)).attr('class') === 'available' ) {
                $('#'+String(i)).off().attr('class', 'unavailable marked');
                console.log('Available');
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
                $('.holding').attr('class', 'pl-card giveable');
                $('.giveable').off().on('click', give_card);
                $('.card.holding').off().on('click', take_card).attr('class', 'card takeable');
                $('.down').attr('class', 'pl-card giveable');
                $('#card-48').off().on('click', select_airlift);
                $('#card-50').off().on('click', select_gg);
                $('.marked').off().on('click', execute_move).attr('class', 'available');
                $('.selectable').off().attr('class', 'unavailable');
                set_treatable(String(data.position));
                buttons_on();
                $('html').off();
            }
        }
    ).error(function(error){console.log(error)});
}
