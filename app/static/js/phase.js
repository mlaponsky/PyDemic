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
            if (i+num_outbreaks <= 8) {
                $('#outbreak-'+String(i+num_outbreaks)).attr('class', 'on');
            } else {
                $('#outbreak-8').attr('class', 'on');
            }
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
    var map = Snap.select('#cities');
    ACTIONS = 0;
    EPIDEMIC = 0;
    board_off();
    map.selectAll('.available').forEach( function(el) {
		el.unavailable();
	});
    map.selectAll('.treatable').forEach( function(el) {
		el.unavailable();
	});
    buttons_off();
    $.getJSON( $SCRIPT_ROOT + '/_end_turn').success(
        function(data) {
            PHASE = 5;
            $('#draw-phase').attr('class', 'on');
            $('#next-turn').prop('disabled', true);
            if (data.lose) {
                $('#stage-name').html("YOU LOSE");
                $('#stage-name').fadeIn(300);
                board_off();
                buttons_off();
            } else {
                $('#draw-0').attr('src', "static/img/player_cards/pl-"+String(data.draw_0)+".svg");
                $('#draw-1').attr('src', "static/img/player_cards/pl-"+String(data.draw_1)+".svg");
                $('#stage-name').html("DRAW STAGE");
                $('#stage-name').fadeIn(300).delay(1000).fadeOut(300).delay(300);
                $('#next-phase').prop('disabled', true);
                setTimeout( function() {
                    $('#logger').html('Drew '+CARDS[data.draw_0].bold()+' and '+CARDS[data.draw_1].bold()+'.');
                    $('#draw-0').delay(500).show(400);
                    $('#draw-1').delay(500).show(400);
                    document.getElementById("cards-cnt").getElementsByTagName('tspan')[0].textContent = String(data.cards_left);

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
                    if ( EPIDEMIC > 0 ) {
                        setTimeout( function() {
                            epidemic()
                        }, 3000);
                    } else if (TRASHING === 1) {
                        setTimeout( function() {
                            set_active_trash()
                        }, 3000);
                    } else if (data.oqn) {
                        $('#logger').html($('#logger').html()+ '. Played One Quiet Night; will skip infection stage.');
                        set_next_button();
                    } else {
                        events_on();
                        set_next_button();
                    }
                }, 1000);
            }
        }).error(function(errors){console.log(error);});
}

function epidemic() {
    $('#logger-box').stop(true);
    $('#logger-box').css({"border-color": "#fffff0"});
    $.getJSON($SCRIPT_ROOT + '/_epidemic').success(
        function(data) {
            if (data.lose) {
                $('#stage-name').html("YOU LOSE");
                $('#stage-name').fadeIn(300);
                board_off();
                buttons_off();
                $('#epidemic-'+String(data.drawn)).show();
                $('#infect').attr('src', '/static/img/infect_cards/inf-'+String(data.card)+'.svg');
                $('#infect').delay(1000).show(400);
            } else {
                $('.draw-card').delay(100).hide(400);
                $('#epidemic-'+String(data.drawn)).show(200);
                EPIDEMIC--;
                $('#infect-discard-'+String(data.card)).show();
                $('#stage-name').html('EPIDEMIC').delay(500).fadeIn(300).delay(1000).fadeOut(300).delay(300);;

                $('#forecast>li').hide();
                for (var n=data.forecast.length-1; n >= 0; n--) {
                    $('#forecast').prepend($('#forecast-'+String(data.forecast[n])));
                    $('#forecast-'+String(data.forecast[n])).show();
                }
                setTimeout( function() {
                    $('#infect').attr('src', '/static/img/infect_cards/inf-'+String(data.card)+'.svg');
                    $('#infect').delay(1000).show(400);
                    setTimeout( function() {
                        infect_cities(data);

                        set_infect_rate();
                        set_outbreaks(data.outbreaks);

                        if (Object.keys(data.infected).length !== 0) {
                            $('#logger').html('(EPIDEMIC)'.bold()+' Infected '+CARDS[data.card].bold()+' with 3 '+COLORS[data.color].bold()+' cubes.');
                        } else if ( data.cured === 2 ) {
                            $('#logger').html('(EPIDEMIC)'.bold()+' Drew '+CARDS[data.card].bold()+' , but '+COLORS(data.color).bold()+' has been eradicated.');
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
                                if ( EPIDEMIC > 0 ) {
                                    epidemic();
                                } else if ( TRASHING === 1 ) {
                                    set_active_trash();
                                } else if (data.oqn) {
                                    events_on();
                                    $('#logger').html($('#logger').html()+ '. Played One Quiet Night; will skip infection stage.');
                                    set_next_button();
                                } else {
                                    PHASE = 6;
                                    events_on();
                                    for (var i=0; i<data.at_risk.length; i++) {
                                        pulse_svg(data.at_risk[i]);
                                    }
                                    $('.infect-discard').hide();
                                    set_next_button();
                                }
                                events_on();
                            }, 500);
                        }
                    }, 1000)
                }, 1000);
            }
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
            $('#forecast>li').hide();
            for (var n=data.forecast.length-1; n >= 0; n--) {
                $('#forecast').prepend($('#forecast-'+String(data.forecast[n])));
                $('#forecast-'+String(data.forecast[n])).show();
            }
            if ( EPIDEMIC > 0 ) {
                epidemic();
            } else if (TRASHING === 1) {
                set_active_trash();
            } else if (data.oqn) {
                events_on();
                $('#logger').html($('#logger').html()+ '. Played One Quiet Night; will skip infection stage.');
                set_next_button();
            } else {
                events_on();
                PHASE = 6;
                set_next_button();
            }
        }
    )
}

function infect() {
    buttons_off();
    $('#next-phase').prop('disabled', true);
    $('#logger-box').stop(true);
    $('#logger-box').attr("border-color", "#fffff0");
    $('.choice').hide();
    $('.draw-card').delay(100).hide(400);
    $('#infect').delay(100).hide(400);
    $.getJSON( $SCRIPT_ROOT + '/_infect' ).success( function(data) {
        if (data.lose) {
            $('#stage-name').html("YOU LOSE");
            $('#stage-name').fadeIn(300);
            board_off();
            buttons_off();
            $('#infect').delay(500).show(400);
            $('#infect').attr('src', '/static/img/infect_cards/inf-'+String(data.card)+'.svg');
            $('#infect-discard-'+String(data.card)).show(200);
            infect_cities(data);
            if (data.outbreaks.length !== 0) {
                var outbreaks = [];
                for ( var i=0; i<data.outbreaks.length; i++ ) {
                    outbreaks.push(CARDS[data.outbreaks[i]]);
                }
                $('#logger').html('Infected '+CARDS[data.card].bold()+' with 1 '+COLORS[data.color].bold()+' cube. OUTBREAK(S) in '+outbreaks.join(", ").bold()+'.');
            }
        } else {
            PHASE = data.phase;
            COUNTER = data.total;
            $('#forecast>li').hide();
            for (var n=data.forecast.length-1; n >= 0; n--) {
                $('#forecast').prepend($('#forecast-'+String(data.forecast[n])));
                $('#forecast-'+String(data.forecast[n])).show();
            }
            $('#stage-name').html('INFECT STAGE '+String(data.counter)).delay(500).fadeIn(300).delay(1000).fadeOut(300);
            setTimeout( function() {
                $('#inf-phase-'+String(data.counter)).attr('class', 'on');
                $('#infect').delay(500).show(400);
                $('#infect').attr('src', '/static/img/infect_cards/inf-'+String(data.card)+'.svg');
                $('#infect-discard-'+String(data.card)).show(200);
                setTimeout( function() {
                    events_on();
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
                    set_next_button();
                }, 500)
            }, 2000);
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
            $('#logger').html('Moved '+CARDS[Number(card)].bold()+' from the Infection discard to the graveyard.');
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
        TRASHING = 0;
        ACTIVE = data.roles[0];
        set_selectable_players(ACTIVE);

        $('#stage-name').html(ROLES[data.roles[0]]+"'s TURN").delay(100).fadeIn(300).delay(1000).fadeOut(300);
        for ( var i=1; i<=4; i++ ) {
            $('#actions-'+String(i)).attr('class', 'off');
            $('#inf-phase-'+String(i)).attr('class', 'off');
        }
        $('#draw-phase').attr('class', 'off');
        for ( var i=0; i<48; i++ ) {
            stop_svg(i);
        }
        for ( var i=0; i<data.at_risk.length; i++ ) {
            pulse_svg(data.at_risk[i]);
        }
        buttons_on();
        board_on();
        $('.pl-name').css('background', "url("+data.role_img+") no-repeat center center");
        $('#player-color').attr('src', data.icon);
        $('#forecast>li').hide();
        for (var n=data.forecast.length-1; n >= 0; n--) {
            $('#forecast').prepend($('#forecast-'+String(data.forecast[n])));
            $('#forecast-'+String(data.forecast[n])).show();
        }

        var first = $('#'+data.roles[0]).parent().parent();
        var last = $('#'+data.roles[data.roles.length-1]).parent().parent();
        last.parent().append(last);
        last.show();
        first.hide();

        $('.pl-card').hide(200);
        set_giveable(data.hand, data.can_give);
        set_takeable(data.team_hands, data.can_take);

        for (var j=0; j<data.pieces.length; j++) {
            var city = document.getElementById('city-'+data.positions[j]);
            var city_dims = city.getBoundingClientRect();
            animate_position(j, data.roles, data.positions[j], city_dims);
        }
        set_cities(data.available);
        set_treatable(data.positions[0])
        set_selectable_players(data.roles[0]);
        events_on();
        if (ACTIVE === 'cp') {
            for (var l=48; l<53; l++) {
                if ( !$('#pl-discard-'+String(l)).hasClass('graveyard') ) {
                    $('#pl-discard-'+String(l)).off().on('click', store_on_cp).addClass('takeable');
                }
            }
        }
        $('#infect').hide(200);
        $('.draw-card').hide(200);
        $('#logger').html(ROLES[ACTIVE].bold()+"'s turn.")
        $('#build-station').prop('disabled', !data.can_build);
        $('#make-cure').prop('disabled', !data.can_cure);
        $('#undo-action').prop('disabled', ACTIONS === 0)
    }).error(function(errors){console.log(error);});
}
