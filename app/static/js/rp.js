function select_rp(target) {
    target.off().on('click', escape_rp).addClass('down').removeClass('giveable takeable');
    board_off();
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
    $('.infect-discard').off().on('click', execute_rp).addClass('takeable');
    $('#logger').html('(Resilient Population) Choose one card in the Infection Discard pile to remove from the game.');
}

function execute_rp() {
    var card_id = $(this).attr('id').split('-')[2];
    var select = 0;
    if ( $('.card.down').length !== 0 ) {
        select  = $('.down').parent().parent().index();
    }
    $.getJSON( $SCRIPT_ROOT + '/_execute_rp', { remove: Number(card_id),
                                                index: select } ).success(
        function(data) {
            discard('52');
            $('#infect-discard-'+String(data.deleted)).off().attr('class', 'graveyard');
            ACTIONS++;
            $('.holding.down').removeClass('down').hide(200);
            board_on();
            $('.marked').off().on('click', execute_move).attr('class', 'available');
            $('.marked-t').off().on('click', treat).attr('class', 'treatable');
            if ( !body.hasClass('selecting') ) {
                infect_toggle();
            } else {
                body.removeClass('selecting');
            }
            $('#undo-action').off().on('click', undo).prop('disabled', ACTIONS === 0);
            buttons_on();
            $('html').off();
            $('#logger').html('Moved '+CARDS[data.deleted].bold()+' from the Infection discard to the graveyard.');
        }
    )
}

function escape_rp() {
    board_on();
    $('.marked').off().on('click', execute_move).attr('class', 'available');
    $('.marked-t').off().on('click', treat).attr('class', 'treatable');
    if ( !body.hasClass('selecting') ) {
        infect_toggle();
    } else {
        body.removeClass('selecting');
    }
    $('#undo-action').off().on('click', undo).prop('disabled', ACTIONS === 0);
    buttons_on();
    $('html').off();
    $('#logger').html('Cancelled <b>RESILIENT POPULATION</b>.')
}
