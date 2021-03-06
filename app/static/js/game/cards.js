function select_card(event) {
    var image = $(event.target);
    if ( image.attr('class') === 'up' ) {
        image.attr('class', 'down');
    } else {
        image.attr('class', 'up');
    }
}

function create_card(city, data) {
    var card = $('<li class="pl-card"></li>');
    card.attr( 'id', "card-"+String(city) );
    var image = $('<div></div>');
    image.attr('title', data['name'] + '\n' + data['description'] );
    image.on('click', select_card);
    image.css('background', "url("+data['player_card']+") no-repeat center center");
    image.css('background-size', 'contain');
    image.appendTo(card);
    var hand = $("#player");
    $(".pl-card").each( function(index) {
        var id = $(this).attr('id');
        if ( Number(id.split('-')[1]) > city ) {
            $(this).before(card);
            return false;
        }
    });
}

function set_team_trash(owner) {
    var map = Snap.select('#cities');
    TRASHING = 1;
    $('.can-give').off().removeClass('can-give');
    map.selectAll('.available').forEach( function(el) {
		el.unavailable();
        el.addClass('marked');
	});
    map.selectAll('.treatable').forEach( function(el) {
		el.unavailable();
        el.addClass('marked');
	});
    $('.role').off().attr('class', 'role');
    buttons_off();
    board_off();
    $('#'+owner).parent().parent().attr('class', 'team-trashing');
    $('#'+owner+"-box li.card").off().on('click', trash).addClass('trashable');
    $('#logger').html( $('#logger').html() + ' Over the hand limit; please choose discard a card.');
}

function set_active_trash() {
    var map = Snap.select('#cities');
    TRASHING = 1;
    map.selectAll(".available").forEach( function(el) {
		el.unavailable();
	});
    map.selectAll(".selectable").forEach( function(el) {
		el.unavailable();
	});
    map.selectAll(".selected").forEach( function(el) {
		el.unavailable();
	});
    map.selectAll('.treatable').forEach( function(el) {
		el.unavailable();
        el.addClass('marked-t');
	});
    buttons_off();
    board_off();
    $('.pl-card').off().on('click', trash).addClass('trashable');
    $('#logger').html( $('#logger').html() + ' You are over the hand limit. Discard down to 7 cards.');
}

function discard(card) {
    if ( $('.event-card.down').length !== 0 ) {
        $('.down').removeClass('.down').hide(200);
    } else {
        $("#card-"+card).attr('class', 'pl-card').hide(200);
    }
    $("#pl-discard-"+card).show(200);
    $('#logger').html($('#logger').html()+' Discarded '+CARDS[Number(card)].bold()+'.');
}

function board_off() {
    $('.trashable').off().removeClass('trashable').addClass('holding-t');
    $('.giveable').off().removeClass('giveable').addClass('holding');
    $('.takeable').off().removeClass('takeable').addClass('holding');
    $('.role.choosable').off().removeClass('choosable').addClass('holding')
    $('.self-chooseable').off().removeClass('self-chooseable').addClass('holding');
}

function board_on() {
    $('.trashable').off().removeClass('trashable');
    $('.giveable').off().removeClass('giveable');
    $('.takeable').off().removeClass('takeable');
    $('.down.curing').off().removeClass('down curing');
    $('.pl-card.down').off().removeClass('down').addClass('giveable');
    $('.card.down').off().removeClass('down').addClass('takeable');
    $('.pl-card.holding').removeClass('holding').addClass('giveable');
    $('.pl-discard.holding').removeClass('holding').addClass('takeable').off().on('click', store_on_cp);
    $('.card.holding').removeClass('holding').addClass('takeable');
    $('.giveable').off().on('click', give_card);
    $('.card.takeable').off().on('click', take_card);
    $('.role.holding').off().on('click', select_player).removeClass('holding').addClass('choosable');
    $('#name.holding').off().removeClass('holding').addClass('self-chooseable');
    $('.can-give').removeClass('can-give');
    $('.can-take').removeClass('can-take');
    $('.team-trashing').removeClass('team-trashing');
}

function trash(event) {
    var card = $(event.target).parent();
    card.removeClass('giveable').addClass('down');
    var card_id_bits = card.attr('id').split('-');
    var card_id = card_id_bits[card_id_bits.length - 1];
    if (card_id === '48') {
        select_airlift(card);
    } else if (card_id === '49') {
        select_forecast(card);
    } else if (card_id === '50') {
        select_gg(card);
    } else if (card_id === '51') {
        select_oqn(card);
    } else if (card_id === '52') {
        select_rp(card);
    } else {
        $.getJSON( $SCRIPT_ROOT + '/_trash', { card: Number(card_id),
                                               action: 1 }).success(
            function(data) {
                PHASE = data.phase;
                $('#logger').html('');
                if ( card.hasClass('pl-card') ) {
                    discard(String(data.card));
                } else {
                    card.off().removeClass('takeable trashable down').hide(200);
                    $('#logger').html('Discarded '+CARDS[Number(data.card)].bold()+'.');
                }
                board_on();
                buttons_on();
                if ( data.num_cards <= 7 ) {
                    TRASHING = 0;
                    if (PHASE >= 4) {
                        actions_off();
                    } else {
                        set_cities(data.available);
                        set_treatable(data.origin);
                    }
                } else {
                    if ( ACTIVE === data.owner ) {
                        set_active_trash();
                    } else {
                        set_team_trash(data.owner)
                    }
                }
                if ( !body.hasClass('selecting') && data.phase <= 4 ) {
                    team_toggle();
                } else {
                    body.removeClass('selecting');
                }
                set_next_button();
            }
        ).error(function(error){console.log(error)});
    }
}

function give(card, data) {
    card.off().attr('class', 'pl-card').hide(200);
    $('#'+data.recipient+'-card-'+data.card).on('click', take_card).addClass('takeable').show(200);
    set_cities(data.available);
    $('#logger').html('You gave '+CARDS[Number(data.card)].bold()+' to the '+ROLES[data.recipient].bold()+'.');
    ACTIONS++;
    PHASE = data.phase;
    $('#actions-'+String(PHASE)).attr('class', 'on');
    $('#undo-action').prop('disabled', ACTIONS===0);
    if (PHASE >= 4) {
        actions_off();
        $('#next-phase').off().on('click', end_turn).prop('disabled', false);
    } else {
        set_cities(data.available);
        set_treatable(data.origin);
    }
}

function give_card(event) {
    var card = $(event.target).parent();
    var card_id = card.attr('id').split('-')[1];
    var sel = ACTIVE;
    if ( $('.role.chosen').length !== 0 ) {
        sel = $('.chosen').parent().parent().index();
    }
    if (card_id === '48') {
        select_airlift(card);
    } else if (card_id === '49') {
        select_forecast(card);
    } else if (card_id === '50') {
        select_gg(card);
    } else if (card_id === '51') {
        select_oqn(card);
    } else if (card_id === '52') {
        select_rp(card);
    } else {
        $.getJSON( $SCRIPT_ROOT + '/_give_card', { card: Number(card_id),
                                                   recip: sel }).success(
            function(data) {
                var map = Snap.select('#cities');
                if (typeof data.available !== 'undefined') {
                    map.selectAll('.available').forEach( function(el) {
                        el.unavailable();
                    });
                    buttons_off();
                    if (!body.hasClass('menu-push-toleft')) {
                        team_toggle();
                        setTimeout( function() {
                            give(card, data);
                            if ( data.num_cards > 7 ) {
                                $('#'+data.recipient).parent().parent().addClass('can_give');
                                set_team_trash(data.recipient);
                            } else {
                                setTimeout( function() {
                                    team_toggle();
                                    buttons_on();
                                }, 1200);
                            }
                        }, 200);
                    } else {
                        give(card, data);
                        if ( data.num_cards > 7 ) {
                            $('#'+data.recipient).parent().parent().addClass('can_give');
                            set_team_trash(data.recipient);
                        }
                        buttons_on();
                    }
                    $('#build-station').prop('disabled', !data.can_build);
                    $('#make-cure').prop('disabled', !data.can_cure);
                    set_next_button();
                } else {
                    var map = Snap.select('#cities');
                    map.selectAll('.available').forEach(function(el) {
                        el.unavailable();
                        el.addClass('marked');
                    });
                    map.selectAll('.treatable').forEach( function(el) {
                        el.unavailable();
                        el.addClass('marked-t');
                    });
                    buttons_off();
                    card.off().attr('class', 'pl-card down');
                    board_off();
                    if (!body.hasClass('menu-push-toleft')) {
                        team_toggle();
                    } else {
                        body.addClass('selecting');
                    }
                    for (var i=0; i<data.recipients.length; i++) {
                        $("#"+data.recipients[i]).parent().parent().attr('class', 'can-give');
                        $("#"+data.recipients[i]).off().on('click', select_recipient);
                    }
                    $('html').off().on( 'click', function(e) {
                        if ( $(e.target).hasClass('down') ) {
                            escape_give_select(card, data);
                        }
                    });
                    $('html').keyup( function( e ) {
                        if (e.keyCode === 27) { escape_give_select(card, data) };
                    });
                    $('#logger').html('Choose a recipient of the card.');
                }
            }).error(function(error) {console.log(errors)} );

    }
}

function select_recipient(event) {
    var recip = $(event.target).parent().parent().index();
    var card_id = $('.down').attr('id').split('-')[1];
    $.getJSON( $SCRIPT_ROOT + '/_select_recipient', { card: card_id,
                                                      selected: recip }).success(
        function(data) {
            var card = $('#card-'+data.card);
            if ( data.num_cards <= 7) {
                escape_give_select(card, data);
            }
            card.off();
            give(card, data);
            if (data.num_cards > 7) {
                set_team_trash(data.recipient);
            }
            events_on();
            set_selectable_players(ACTIVE);
            set_next_button();
        }).error(function(error) {console.log(errors)} );
}

function take_card(event) {
    var card = $(event.target).parent();
    var source = card.parent().parent().index();
    var card_id = card.attr('id').split('-')[2];
    if (card_id === '48') {
        select_airlift(card);
    } else if (card_id === '49') {
        select_forecast(card);
    } else if (card_id === '50') {
        select_gg(card);
    } else if (card_id === '51') {
        select_oqn(card);
    } else if (card_id === '52') {
        select_rp(card);
    } else {
        $.getJSON( $SCRIPT_ROOT + '/_take', { card: Number(card_id),
                                              id: source}).success(
            function(data) {
                PHASE = data.phase;
                $('#actions-'+String(PHASE)).attr('class', 'on');
                card.off().attr('class', 'card').hide(200);
                $('#card-'+card_id).on('click', give_card).show(200).addClass('giveable');
                buttons_on();
                $('#logger').html('You took '+CARDS[Number(data.card)].bold()+ ' from the '+ROLES[data.source_id].bold()+'.');
                ACTIONS++;
                if ( data.num_cards > 7 ) {
                    set_active_trash();
                }
                if (PHASE >= 4) {
                    actions_off();
                    $('#next-phase').off().on('click', end_turn).prop('disabled', false);
                } else {
                    set_cities(data.available);
                }
                $('#build-station').off().on('click', build_station).prop('disabled', !data.can_build);
                $('#make-cure').off().on('click', make_cure).prop('disabled', !data.can_cure)
                $('#undo-action').prop('disabled', ACTIONS===0);
                set_next_button();
            }).error(function(error) {console.log(errors)} );
    }
}

function escape_give_select(card, data) {
    buttons_on();
    board_on();
    if ( !body.hasClass('selecting') ) {
        team_toggle();
    } else {
        body.removeClass('selecting');
    }
    $('.role').parent().parent().attr('class', '');
    $('.role').off();

    if ( ACTIVE === 'dispatcher' ) {
        $('.role').off().on('click', select_player).attr('class', 'role choosable')
    }
    $('html').off();
    $('#logger').html('Cancelled card sharing.');
}
