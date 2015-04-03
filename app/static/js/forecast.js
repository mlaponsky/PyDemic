function select_forecast(target) {
    target.off().addClass('down').removeClass('giveable takeable');
    $('.giveable').off().switchClass('giveable', 'holding');
    $('.takeable').off().switchClass('takeable', 'holding');
    buttons_off();
    $('.available').off().attr('class', 'unavailable');
    $('.treatable').off().attr('class', 'unavailable');
    $('.role.choosable').off().switchClass('choosable', 'marked');
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

    $.getJSON( $SCRIPT_ROOT + '/_execute_forecast', { card0: Number(card0),
                                                      card1: Number(card1),
                                                      card2: Number(card2),
                                                      card3: Number(card3),
                                                      card4: Number(card4),
                                                      card5: Number(card5) }).success(
        function(data) {
            discard('49');
            $('#forecast').hide(200);
            $('#logger').html('Played <b>FORECAST</b>.');
            $('.pl-card.holding').off().on('click', give_card).switchClass('holding', 'giveable');
            $('.card.holding').off().on('click', take_card).switchClass('holding', 'takeable');
            $('.role.marked').off().on('click', select_player).switchClass('marked', 'choosable');
            buttons_on()
            set_cities(data.available);
            set_treatable(data.position);
        }).error( function(error) {console.log(error) });
}
