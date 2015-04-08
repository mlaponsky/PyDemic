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
    } else if (card_id === '52') {
        select_rp(card);
    } else {
        $.getJSON( $SCRIPT_ROOT + '/_trash', { card: Number(card_id) }).success(
            function(data) {
                discard(String(data.card));
            }
        ).error(function(error){console.log(error)});
    }
}

function set_team_trash(card, data) {
    $('.available').off().attr('class', 'unavailable marked');
    $('.treatable').off().attr('class', 'unavailable marked-t');
    buttons_off();
    card.off().addClass('giving');
    board_off();
    $('#'+data.recipient).parent().parent().attr('class', 'can-give');
    $('#'+data.recipient+"-box li.card").off().on('click', trash).addClass('takeable');
}

function set_active_trash(card, data) {
    $('.available').off().attr('class', 'unavailable marked');
    $('.treatable').off().attr('class', 'unavailable marked-t');
    buttons_off();
    card.off().addClass('taking');
    board_off();
    $('.pl-card').off().on('click', trash).addClass('giveable');
}

function discard(card) {
    if ( $('.event-card').hasClass('down') ) {
        $('.down').removeClass('.down').hide(200);
    } else {
        $("#card-"+card).attr('class', 'pl-card').hide(200);
    }
    $("#pl-discard-"+card).show(200);
    $('#logger').html($('#logger').html()+' Discarded '+CARDS[Number(card)].bold()+'.');
}

function undo_discard(card, owner) {
    if ($('.active-player').attr('id').split('-')[1] !== owner) {
        $('#'+owner+"-card-"+card).show(200);
    } else {
        $('#card-'+card).show(200);
    }
    $("#pl-discard-"+card).hide(200);
    $('#logger').html($('#logger').html()+' Returned '+CARDS[Number(card)].bold()+' to the '+ROLES[owner].bold()+"'s hand.");
}

function board_off() {
    $('.giveable').off().removeClass('giveable').addClass('holding');
    $('.takeable').off().removeClass('takeable').addClass('holding');
    $('.role.choosable').off().removeClass('choosable').addClass('holding')
    $('.self-chooseable').off().removeClass('self-chooseable').addClass('holding');
}

function board_on() {
    $('.pl-card.down').off().removeClass('down').addClass('giveable');
    $('.card.down').off().removeClass('down').addClass('takeable');
    $('.pl-card.holding').removeClass('holding').addClass('giveable');
    $('.card.holding').removeClass('holding').addClass('takeable');
    $('.giveable').off().on('click', give_card);
    $('.takeable').off().on('click', take_card);
    $('.role.holding').off().on('click', select_player).removeClass('holding').addClass('choosable');
    $('#name.holding').off().on('click', function() {console.log('Ya')}).removeClass('holding').addClass('self-chooseable');
}

function give(card, data) {
    card.off().attr('class', 'pl-card').hide(200);
    $('#'+data.recipient+'-card-'+data.card).on('click', take_card).addClass('takeable').show(200);
    set_cities(data.available);
    var giver = $('.active-player').attr('id').split('-')[1];
    $('#logger').html('You gave '+CARDS[Number(data.card)].bold()+' to the '+ROLES[data.recipient].bold()+'.');
    ACTIONS++;
    PHASE++;
    $('#undo-action').prop('disabled', ACTIONS===0);
}

function give_card(event) {
    var card = $(event.target).parent();
    var card_id = card.attr('id').split('-')[1];
    var sel = $('.active-player').attr('id').split('-')[1];
    if ( $('.role.chosen').length !== 0 ) {
        sel = $('.chosen').attr('id');
    }
    if (card_id === '48') {
        select_airlift(card);
    } else if (card_id === '49') {
        select_forecast(card);
    } else if (card_id === '50') {
        select_gg(card);
    } else if (card_id === '52') {
        select_rp(card);
    } else {
        $.getJSON( $SCRIPT_ROOT + '/_give_card', { card: Number(card_id),
                                                   recip: sel }).success(
            function(data) {
                if (typeof data.available !== 'undefined') {
                    $('.available').off();
                    buttons_off();
                    if (!body.hasClass('menu-push-toleft')) {
                        team_toggle();
                        setTimeout( function() {
                            give(card, data);
                            setTimeout( function() {
                                team_toggle();
                                buttons_on();
                            }, 1500);
                        }, 200);
                    } else {
                        give(card, data);
                        buttons_on();
                    }
                } else if ( typeof data.resp !== 'undefined' ) {
                    set_team_trash(card, data);
                } else {
                    $('.available').off().attr('class', 'unavailable marked');
                    $('.treatable').off().attr('class', 'unavailable marked-t');
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
                        if ( $(e.target).parent().parent().attr('class') !== 'can-give' || $(e.target).parent().attr('class') === 'down') {
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
    var recip = $(event.target).attr('id');
    var card_id = $('.down').attr('id').split('-')[1];
    $.getJSON( $SCRIPT_ROOT + '/_select_recipient', { card: card_id, selected: recip }).success(
        function(data) {
            if (typeof data.resp !== 'undefined') {
                set_team_trash($('.down'), data)
            } else {
                var card = $('#card-'+data.card);
                escape_give_select(card, data);
                give(card, data);
                card.off();
            }
        }).error(function(error) {console.log(errors)} );
}

function take_card(event) {
    var card = $(event.target).parent();
    var source_id = card.attr('id').split('-')[0]
    var card_id = card.attr('id').split('-')[2];
    if (card_id === '48') {
        select_airlift(card);
    } else if (card_id === '49') {
        select_forecast(card);
    } else if (card_id === '50') {
        select_gg(card);
    } else if (card_id === '52') {
        select_rp(card);
    } else {
        $.getJSON( $SCRIPT_ROOT + '/_take', { card: Number(card_id),
                                              id: source_id}).success(
            function(data) {
                card.off().attr('class', 'card').hide(200);
                $('#card-'+card_id).on('click', give_card).show(200).addClass('giveable');
                set_cities(data.available);
                buttons_on();
                var taker = $('.active-player').attr('id').split('-')[1];
                $('#logger').html('You took '+CARDS[Number(data.card)].bold()+ ' from the '+ROLES[data.source_id].bold()+'.');
                ACTIONS++;
                PHASE++;
                $('#undo-action').prop('disabled', ACTIONS===0);
            }).error(function(error) {console.log(errors)} );
    }
}

function escape_give_select(card, data) {
    buttons_on();
    $('.available').off().on('click', execute_move);
    card.off().on('click', give_card).removeClass('down').addClass('giveable');
    $('.pl-card.holding').off().on('click', give_card).removeClass('holding').addClass('giveable');
    $('.card.holding').off().on('click', take_card).removeClass('holding').addClass('takeable');
    if ( !body.hasClass('selecting') ) {
        team_toggle();
    } else {
        body.removeClass('selecting');
    }
    $('.role').parent().parent().attr('class', '');
    $('.role').off();

    if ( $('#active-dispatcher').length !== 0 ) {
        $('.role').off().on('click', select_player).attr('class', 'role choosable')
    }
    $('html').off();
    $('#logger').html('Cancelled card sharing.');
}
