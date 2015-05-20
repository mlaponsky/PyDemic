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
    ACTIONS = 0;
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
                    setTimeout( function() {
                        if ( EPIDEMIC > 0 ) {
                            epidemic();
                        } else if (TRASHING === 1) {
                            set_active_trash();
                        } else {
                            infect_phase();
                        }
                    }, 500);
                }, 1000);
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
                    $('.infect-discard').off().hide();
                    var cities = Object.keys(data.infected);
                    for ( var i=0; i<cities.length; i++) {
                        var city_obj = document.getElementById(String(data.card));
                        var dims = city_obj.getBoundingClientRect();
                        for ( var j=0; j<4; j++ ) {
                            if ( data.infected[cities[i]][j] !== 0 ) {
                                add_cubes(String(cities[i]), dims, String(j), data.rows[cities[i]][j], data.infected[cities[i]][j], data.at_risk);
                            }
                        }
                    }
                    for ( var i=0; i<7; i++ ) {
                        if ( $('#rate-'+String(i)).attr('class') === 'on') {
                            $('#rate-'+String(i)).attr('class', 'off');
                            $('#rate-'+String(i+1)).attr('class', 'on');
                            break;
                        };
                    }

                    if (data.infected.length !== 0) {
                        $('#logger').html('(EPIDEMIC)'.bold()+' Infected '+CARDS[data.card].bold()+' with 3 '+COLORS[data.color].bold()+' cubes.');
                    } else if ( data.cure === 2 ) {
                        $('#logger').html('(EPIDEMIC)'.bold()+' Drew '+CARDS[data.card].bold()+' , but '+COLOR(data.color).bold()+' has been eradicated.');
                    } else {
                        $('#logger').html('(EPIDEMIC)'.bold()+' Drew '+CARDS[data.card].bold()+' , but the city is quarantined.');
                    }
                    if (data.infected.length > 1) {
                        $('#logger').html($('#logger').html() + ' OUTBREAK.'.bold())
                    }
                    setTimeout( function() {
                        if ( EPIDEMIC > 0 ) {
                            epidemic();
                        } else if ( TRASHING === 1 ) {
                            set_active_trash();
                        } else {
                            infect_phase();
                        }
                    }, 500);
                }, 1000);
            }, 1000);
        }).error(function(errors){console.log(error);});
    }

function infect_phase() {
    $.getJSON( $SCRIPT_ROOT + '/_infect' ).success( function(data) {
        var cities = Object.keys(data.infected);
        for (var i=0; i<4; i++) {
            if (i<data.cards.length) {
                $('#draw-'+String(i)).show().children('div').css('background', 'url(/static/img/infect_cards/inf-'+String(data.cards[i])+'.svg) no-repeat center center');
                $('#infect-discard-'+String(data.cards[i])).off().show();
            } else {
                $('#draw-'+String(i)).hide();
            }
        }
        setTimeout( function() {
            $('#mask').fadeIn(500);
            setTimeout( function() {
                $('#mask').fadeOut(300);
                for ( var i=0; i<cities.length; i++ ) {
                    var city_obj = document.getElementById(String(cities[i]));
                    var dims = city_obj.getBoundingClientRect();
                    for (var j=0; j<4; j++) {
                        if (data.infected[cities[i]][j] !== 0) {
                            add_cubes(String(cities[i]), dims, String(j), data.rows[cities[i]][j], data.infected[cities[i]][j], data.at_risk);
                        }
                    }
                }
            }, 2000);
        }, 1000);
        PHASE = 4;
    }).error(function(errors){console.log(error);});
}

function events_on() {
    $('#cp-store').addClass('giveable').off().on('click', select_store);
    for ( var i=48; i<53; i++ ) {
        $('#card-'+String(i)).addClass('giveable').off().on('click', give_card);
        for (var j=0; j<$('.role').length; j++) {
            var id= $('.role')[j].attr('id');
            $('#'+id+'-card-'+String(i)).addClass('takeable').off().on('click', take_card);
        }
    }
}

function has_rp() {
    $.getJSON( $SCRIPT_ROOT + '/_has_rp').success(
        function(data) {
            if (data.has_rp) {
                $('#logger').html('Would you like to play the Resilient Population event?');
                $('.choice').show(200);
            }
        }
    )
}
