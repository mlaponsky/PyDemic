function select_store(event) {
    var card = $('#cp-store');
    card.removeClass('giveable');
    var card_id = card.attr('class').split('-')[1];
    card.addClass('down');
    if ( card_id === '48' ) {
        select_airlift(card);
    } else if ( card_id === '49' ) {
        select_forecast(card);
    } else if ( card_id === '50' ) {
        select_gg(card);
    } else if ( card_id === '51' ) {
        select_oqn(card);
    } else if ( card_id === '52' ) {
        select_rp(card);
    }
}

function store_on_cp(event) {
    var card = $(event.target).parent();
    var card_id = card.attr('id').split('-')[2]
    $.getJSON( $SCRIPT_ROOT + '/_store_on_cp', { card: card_id }).success(
        function(data) {
            card.off().hide(200);
            $('#cp-store').off().on('click', select_store).attr('src', 'static/img/player_cards/pl-'+card_id+'.svg');
            $('#cp-store').attr('class', '.store-'+card_id).addClass('giveable').show(200);
            ACTIONS++;
            STORE = 1;
            PHASE = data.phase;
            $('#actions-'+String(PHASE)).attr('class', 'on');
            if (PHASE === 4) {
                actions_off();
            }
            $('#undo-action').prop('disabled', ACTIONS === 0);
        }
    ).error(function(error) {console.log(errors)} )
}
