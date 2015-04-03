function select_rp(target) {
    target.off().on('click', escape_rp).addClass('down').removeClass('giveable takeable');
    $('.giveable').off().removeClass('giveable').addClass('holding');
    $('.takeable').off().removeClass('takeable').addClass('holding');
    buttons_off();
    $('.available').off().attr('class', 'unavailable marked');
    $('.treatable').off().attr('class', 'unavailable marked-t');
    if (!body.hasClass('menu-push-to-right')) {
        infect_toggle();
    } else {
        body.addClass('selecting');
    }

    $('html').keyup( function( e ) {
        if (e.keyCode === 27) { escape_rp() };
    });
    $('#infect-discard li.card').off().on('click', execute_rp).attr('class', 'card takeable');
}

function execute_rp() {
    var card_id = $(this).attr('id').split('-')[2];
    $.getJSON( $SCRIPT_ROOT + '/_execute_rp', { remove: Number(card_id) } ).success(
        function(data) {
            discard('52')
            $('#infect-discard-'+String(data.deleted)).off().attr('class', 'graveyard');
            ACTIONS++;
            escape_rp();
        }
    )
}

function escape_rp() {
    escape_cards();
    $('.marked').off().on('click', execute_move).attr('class', 'available');
    $('.marked-t').off().on('click', treat).attr('class', 'treatable');
    if ( !body.hasClass('selecting') ) {
        infect_toggle();
    } else {
        body.removeClass('selecting');
    }
    buttons_on();
    $('html').off();
}
