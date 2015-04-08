function check_phase() {
    if (PHASE < 4 || PHASE > 7) {
        board_off();
        $('.available').off().attr('class', 'unavailable');
        $('.treatable').off().attr('class', 'unavailable');
        buttons_off();
    }
}

function end_turn() {
    PHASE++;
    board_off();
    $('.available').off().attr('class', 'unavailable');
    $('.treatable').off().attr('class', 'unavailable');
    buttons_off();
    $.getJSON( $SCRIPT_ROOT + '/_end_turn').success(
        function(data) {
            $('#draw-0').show().css('background', "url(static/img/player_cards/pl-"+String(data.draw_0)+".svg) no-repeat center center");
            $('#draw-1').show().css('background', "url(static/img/player_cards/pl-"+String(data.draw_1)+".svg) no-repeat center center");
            if (data.num_cards > 7) {
                $('.pl-card').off().on('click', trash).addClass('giveable');
            }
            $('.forecast-card').hide();
            for (var i=0; i<data.forecast.length; i++) {
                $('#forecast-'+String(data.forecast[i])).show();
            }
        }
    )
}
