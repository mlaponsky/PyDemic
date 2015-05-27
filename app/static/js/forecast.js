function select_forecast(target) {
    target.off().addClass('down').removeClass('giveable takeable');
    buttons_off();
    board_off();
    $('.available').off().attr('class', 'unavailable');
    $('#forecast').show(200);
    $('#next-phase').off().on('click', execute_forecast).prop('disabled', false);
    $('#logger').html("Rearrange the top six cards of the Infection Deck (top card drawn first). Click 'NEXT' when finished.");
}

function execute_forecast() {
    var card0 = $('#forecast li:nth-child(1)').attr('id').split('-')[1];
    var card1 = $('#forecast li:nth-child(2)').attr('id').split('-')[1];
    var card2 = $('#forecast li:nth-child(3)').attr('id').split('-')[1];
    var card3 = $('#forecast li:nth-child(4)').attr('id').split('-')[1];
    var card4 = $('#forecast li:nth-child(5)').attr('id').split('-')[1];
    var card5 = $('#forecast li:nth-child(6)').attr('id').split('-')[1];
    var select = 0;
    if ( $('.card.down').length !== 0 ) {
        select  = $('.down').parent().parent().index();
    }

    $.getJSON( $SCRIPT_ROOT + '/_execute_forecast', { card0: Number(card0),
                                                      card1: Number(card1),
                                                      card2: Number(card2),
                                                      card3: Number(card3),
                                                      card4: Number(card4),
                                                      card5: Number(card5),
                                                      index: select }).success(
        function(data) {
            discard('49');
            $('#logger').html('Played <b>FORECAST</b>.');
            $('#next-phase').off().prop('disabled', true);
            $('#forecast').hide(200);
            buttons_on();
            board_on();
            set_cities(data.available);
            set_treatable(data.position);
            $('.holding.down').removeClass('down').hide(200);
            if (data.num_cards <= 7) {
                TRASHING = 0;
                if (data.phase === 4) {
                    infect_phase();
                }
            } else {
                set_active_trash();
            }
        }).error( function(error) {console.log(error) });
}
