function check_phase() {
    PHASE++;
    if (PHASE < 4 || PHASE > 7) {
        board_off();
        $('.available').off().attr('class', 'unavailable');
        $('.treatable').off().attr('class', 'unavailable');
        buttons_off();
        $('#next-phase').prop('disabled', false).off().on('click', end_turn);
    }
}

function end_turn() {
    PHASE++;
    var EPIDEMIC = 0;
    board_off();
    $('.available').off().attr('class', 'unavailable');
    $('.treatable').off().attr('class', 'unavailable');
    buttons_off();
    $.getJSON( $SCRIPT_ROOT + '/_end_turn').success(
        function(data) {
            $('#draw-0').show().children('div').css('background', "url(static/img/player_cards/pl-"+String(data.draw_0)+".svg) no-repeat center center");
            $('#draw-1').show().children('div').css('background', "url(static/img/player_cards/pl-"+String(data.draw_1)+".svg) no-repeat center center");
            $('#stage-name').html("DRAW STAGE");
            $('#mask').fadeIn(500);
            setTimeout( function() {
                $('#card-'+String(data.draw_0)).show(400);
                $('#card-'+String(data.draw_1)).show(400);
                var cards_left = document.getElementById("cards-cnt").getElementsByTagName('tspan')[0].textContent
                document.getElementById("cards-cnt").getElementsByTagName('tspan')[0].textContent = String(Number(cards_left) - 2);

                if ( data.draw_0 === 53 ) {
                    EPIDEMIC++;
                }
                if ( data.draw_1 === 53 ) {
                    EPIDEMIC++;
                }
                if (data.num_cards > 7) {
                    TRASHING = 1;
                }
                setTimeout( function () {
                    $('#mask').fadeOut(300);
                }, 1000);
                if ( EPIDEMIC > 0 ) {
                    epidemic();
                } else if (TRASHING === 1) {
                    set_active_trash();
                }
            }, 1000);
        }).error(function(errors){console.log(error);});
}

function epidemic() {
    $.getJSON($SCRIPT_ROOT + '/_epidemic').success(
        function(data) {
            setTimeout( function() {
                $('.draw-card').hide();
                $('#draw-0').show().children('div').css('background', 'url(/static/img/infect_cards/inf-'+String(data.card)+'.svg) no-repeat center center');
                EPIDEMIC--;
                $('#stage-name').html('EPIDEMIC');
                $('#mask').fadeIn(500);
                setTimeout( function() {
                    $('#mask').fadeOut(300);
                    for ( var city in data.infected ) {
                        if ( data.infected.hasOwnProperty(city) ) {
                            var city_obj = document.getElementById(String(city));
                            var dims = city_obj.getBoundingClientRect();
                            add_cubes(String(city), dims, String(data.color), data.row, data.added);
                        }
                    }
                    if (data.infected.length != 0) {
                        $('#logger').html('(EPIDEMIC)'.bold()+' Infected '+CARDS[data.card].bold()+' with 3 '+COLORS[data.color].bold()+' cubes.');
                    } else if ( data.cure === 2 ) {
                        $('#logger').html('(EPIDEMIC)'.bold()+' Drew '+CARDS[data.card].bold()+' , but '+COLOR(data.color).bold()+' has been eradicated.');
                    } else {
                        $('#logger').html('(EPIDEMIC)'.bold()+' Drew '+CARDS[data.card].bold()+' , but the city is quarantined.');
                    }
                    if (data.infected.length > 1) {
                        $('#logger').html($('#logger').html() + ' OUTBREAK.'.bold())
                    }

                    if ( EPIDEMIC > 0 ) {
                        epidemic();
                    } else if ( TRASHING === 1 ) {
                        set_active_trash();
                    }
                }, 2000);
            }, 1000)
        }).error(function(errors){console.log(error);});
}
