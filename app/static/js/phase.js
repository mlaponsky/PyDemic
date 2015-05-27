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

function set_outbreaks(outbreaks) {
    var num_outbreaks = outbreaks.length;
    for ( var i=0; i<9; i++ ) {
        if ( $('#outbreak-'+String(i)).attr('class') === 'on') {
            $('#outbreak-'+String(i)).attr('class', 'off');
            $('#outbreak-'+String(i+num_outbreaks)).attr('class', 'on');
            break;
        };
    }
}

function set_infect_rate() {
    for ( var i=0; i<7; i++ ) {
        if ( $('#rate-'+String(i)).attr('class') === 'on') {
            $('#rate-'+String(i)).attr('class', 'off');
            $('#rate-'+String(i+1)).attr('class', 'on');
            break;
        };
    }
}

function infect_cities(data) {
    var cities = Object.keys(data.infected);
    for ( var i=0; i<cities.length; i++) {
        var city_obj = document.getElementById('city-'+String(cities[i]));
        var dims = city_obj.getBoundingClientRect();
        for ( var j=0; j<4; j++ ) {
            if ( data.infected[cities[i]][j] !== 0 ) {
                add_cubes(String(cities[i]), dims, String(j), data.rows[cities[i]][j], data.infected[cities[i]][j], data.at_risk);
            }
        }
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
            $('#draw-0').attr('src', "static/img/player_cards/pl-"+String(data.draw_0)+".svg");
            $('#draw-1').attr('src', "static/img/player_cards/pl-"+String(data.draw_1)+".svg");
            $('#stage-name').html("DRAW STAGE");
            $('#stage-name').fadeIn(300).delay(1000).fadeOut(300).delay(300);
            setTimeout( function() {
                $('#logger').html('Drew '+CARDS[data.draw_0].bold()+' and '+CARDS[data.draw_1].bold()+'.');
                $('#draw-0').delay(500).show(400);
                $('#draw-1').delay(500).show(400);
                events_on();
                var cards_left = document.getElementById("cards-cnt").getElementsByTagName('tspan')[0].textContent
                document.getElementById("cards-cnt").getElementsByTagName('tspan')[0].textContent = String(Number(cards_left) - 2);

                if ( data.draw_0 === 53 ) {
                    EPIDEMIC++;
                } else {
                    $('#card-'+String(data.draw_0)).delay(800).show(200);
                }
                if ( data.draw_1 === 53 ) {
                    EPIDEMIC++;
                } else {
                    $('#card-'+String(data.draw_1)).delay(800).show(200);
                }
                if (data.num_cards > 7) {
                    TRASHING = 1;
                }
                setTimeout( function() {
                    if ( EPIDEMIC > 0 ) {
                        epidemic();
                    } else if (TRASHING === 1) {
                        set_active_trash();
                    } else {
                        $('#next-phase').off().on('click', infect).prop('disabled', false);
                    }
                }, 3000);
            }, 1000);
        }).error(function(errors){console.log(error);});
}

function epidemic() {
    $('#logger-box').stop(true);
    $('#logger-box').css({"border-color": "#fffff0"});
    $.getJSON($SCRIPT_ROOT + '/_epidemic').success(
        function(data) {
            $('.draw-card').delay(100).hide(400);
            $('#infect').delay(100).hide(400);
            $('#epidemic-'+String(data.drawn)).show();
            EPIDEMIC--;
            $('#infect-discard-'+String(data.card)).show();
            $('#stage-name').html('EPIDEMIC').delay(500).fadeIn(300).delay(1000).fadeOut(300).delay(300);;
            setTimeout( function() {
                $('#infect').attr('src', '/static/img/infect_cards/inf-'+String(data.card)+'.svg');
                $('#infect').delay(1000).show(400);
                setTimeout( function() {
                    infect_cities(data);

                    set_infect_rate();
                    set_outbreaks(data.outbreaks);

                    if (Object.keys(data.infected).length !== 0) {
                        $('#logger').html('(EPIDEMIC)'.bold()+' Infected '+CARDS[data.card].bold()+' with 3 '+COLORS[data.color].bold()+' cubes.');
                    } else if ( data.cure === 2 ) {
                        $('#logger').html('(EPIDEMIC)'.bold()+' Drew '+CARDS[data.card].bold()+' , but '+COLOR(data.color).bold()+' has been eradicated.');
                    } else {
                        $('#logger').html('(EPIDEMIC)'.bold()+' Drew '+CARDS[data.card].bold()+' , but the city is quarantined.');
                    }
                    if (data.outbreaks.length !== 0) {
                        var outbreaks = [];
                        for ( var i=0; i<outbreaks.length; i++ ) {
                            outbreaks.push(CARDS[data.outbreaks[i]]);
                        }
                        $('#logger').html( $('#logger').html()+" OUTBREAK(S) in "+outbreaks.join(", ").bold()+'.');
                    }
                    if (data.has_rp !== false) {
                        $('#logger').html($('#logger').html()+' Would you like to play Resilient Population?');
                        pulse_log();
                        $('#accept').show(200).off().on('click', set_rp);
                        $('#decline').show(200).off().on('click', finish_epidemic);
                    } else {
                        setTimeout( function() {
                            $('#infect').hide(300).delay(300)
                            if ( EPIDEMIC > 0 ) {
                                epidemic();
                            } else if ( TRASHING === 1 ) {
                                set_active_trash();
                            } else {
                                PHASE = 5;
                                $('.infect-discard').hide();
                                for (var i=0; i<data.at_risk.length; i++) {
                                    pulse_svg(data.at_risk[i]);
                                }
                                $('#next-phase').off().on('click', infect).prop('disabled', false);
                            }
                        }, 500);
                    }
                }, 1000)
            }, 1000);
        }).error(function(errors){console.log(error);});
    }

function finish_epidemic() {
    $('#logger-box').stop(true);
    $('#logger-box').css({"border-color": "#fffff0"});
    $.getJSON( $SCRIPT_ROOT + '/_finish_ep').success(
        function(data) {
            if (data.has_rp) {
                $('#logger').html('');
            }
            $('#logger').html($('#logger').html()+ ' Shuffled discard pile and placed it on top of deck.');
            for ( var i=0; i<data.at_risk.length; i++ ) {
                pulse_svg(data.at_risk[i]);
            }
            $('.choice').hide();
            $('.infect-discard').hide();
            if ( EPIDEMIC > 0 ) {
                epidemic();
            } else {
                $('#next-phase').off().on('click', infect).prop('disabled', false);
            }
        }
    )
}

function infect() {
    buttons_off();
    events_on();
    $('#logger-box').stop(true);
    $('#logger-box').attr("border-color", "#fffff0");
    $('.choice').hide();
    $('.draw-card').delay(100).hide(400);
    $('#infect').delay(100).hide(400);
    $.getJSON( $SCRIPT_ROOT + '/_infect' ).success( function(data) {
        $('#stage-name').html('INFECT STAGE '+String(data.counter)).delay(500).fadeIn(300).delay(1000).fadeOut(300).delay(300);
        setTimeout( function() {
            $('#infect').delay(1000).show(400);
            $('#infect').attr('src', '/static/img/infect_cards/inf-'+String(data.card)+'.svg');
            $('#infect-discard-'+String(data.card)).show(200);
            setTimeout( function() {
                stop_svg(data.card);
                infect_cities(data);

                set_outbreaks(data.outbreaks);

                if ( Object.keys(data.infected).length !== 0 ) {
                    $('#logger').html('Infected '+CARDS[data.card].bold()+' with 1 '+COLORS[data.color].bold()+' cube.');
                } else if (data.cure === 2) {
                    $('#logger').html('Drew '+CARDS[data.card].bold()+', but the disease is eradicated.');
                } else {
                    $('#logger').html('Drew '+CARDS[data.card].bold()+', the city is quarantined.');
                }
                if (data.outbreaks.length !== 0) {
                    var outbreaks = [];
                    for ( var i=0; i<data.outbreaks.length; i++ ) {
                        outbreaks.push(CARDS[data.outbreaks[i]]);
                    }
                    $('#logger').html( $('#logger').html()+" OUTBREAK(S) in "+outbreaks.join(", ").bold()+'.');
                }
            }, 1000)
        }, 2000);
        PHASE++;
        if (data.counter < data.total) {
            $('#next-phase').off().on('click', infect).prop('disabled', false);
        } else {
            $('#next-phase').off().on('click', next_turn).prop('disabled', false);
        }
    }).error(function(errors){console.log(error);});
}

function events_on() {
    $('#cp-store').addClass('giveable').off().on('click', select_store);
    for ( var i=48; i<53; i++ ) {
        $('#card-'+String(i)).addClass('giveable').off().on('click', give_card);
        var roles = $('.role');
        for (var j=0; j<roles.length; j++) {
            var id= $(roles[j]).attr('id');
            $('#'+id+'-card-'+String(i)).addClass('takeable').off().on('click', take_card);
        }
    }
}

function set_rp() {
    if (!body.hasClass('menu-push-toright')) {
        infect_toggle();
    } else {
        body.addClass('selecting');
    }
    $('.infect-discard').addClass('takeable').off().on('click', epidemic_rp);
}

function epidemic_rp() {
    var card = $(this).attr('id').split('-')[2]
    $.getJSON( $SCRIPT_ROOT + '/_ep_rp', { card: Number(card) }).success(
        function(data) {
            if ( !data.is_stored ) {
                $('#'+data.owner+'-card-52').hide(200);
                $('#card-52').hide(200);
                $('#pl-discard-52').show(200);
            } else {
                $('#cp-store').hide(200);
                $('#pl-discard-52').off().show(200).attr('class', 'graveyard');
            }
            $('#infect-discard-'+card).off().attr('class', 'graveyard');
            $('.choice').hide(200);
            $('.infect-discard').hide();
            $('#logger').html('Moved '+CARDS[Number(card)].bold()+' from the Infection discard to the graveyard, and shuffled the infection discard pile back into the deck.');
            if ( !body.hasClass('selecting') ) {
                infect_toggle();
            } else {
                body.removeClass('selecting');
            }
            $('.choice').hide();
            finish_epidemic();
        }
    ).error(function(errors){console.log(error);});
}

function next_turn() {
    $.getJSON( $SCRIPT_ROOT + '/_next_turn' ).success( function(data) {
        ACTIONS = 0;
        PHASE = 0;
        ACTIVE = data.roles[0];
        $('#stage-name').html(ROLES[data.roles[0]]+"'s TURN").delay(100).fadeIn(300).delay(1000).fadeOut(300);
        set_cities(data.available);
        set_treatable(data.positions[0])
        set_selectable_players(data.roles[0]);
        $('.pl-name').css('background', "url("+data.role_img+") no-repeat center center");
        $('#player-color').attr('src', data.icon);
        $('#forecast>li').hide();
        for (var n=0; n<data.forecast.length; n++) {
            $('#forecast-'+String(data.forecast[n])).show();
        }

        var first = $('#'+data.roles[0]).parent().parent();
        var last = $('#'+data.roles[data.roles.length-1]).parent().parent();
        last.parent().append(last);
        last.show();
        last.children('li').show()
        first.hide();

        $('.pl-card').hide(200);
        set_giveable(data.hand, data.can_give);
        set_takeable(data.team_hands, data.can_take);

        for (var j=0; j<data.pieces.length; j++) {
            var city = document.getElementById('city-'+data.positions[j]);
            var city_dims = city.getBoundingClientRect();
            animate_position(j, data.roles, data.positions[j], city_dims);
        }
        buttons_on();
        $('#build-station').prop('disabled', !data.can_build);
        $('#make-cure').prop('disabled', !data.can_cure);
        $('#undo-action').prop('disabled', ACTIONS === 0)
    }).error(function(errors){console.log(error);});
}
