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

function discard(card) {
    $("#card-"+card).attr('class', 'pl-card');
    $("#card-"+card).hide(200);
    $("#pl-discard-"+card).show(200);
}

function undo_discard(card) {
    $('#card-'+card).show(200);
    $("#card-"+card).attr('class', 'pl-card');
    $("#pl-discard-"+card).hide(200);
}

function escape_cards() {
    $('.pl-card.down').switchClass('down', 'giveable');
    $('.card.down').switchClass('down', 'takeable');
    $('.pl-card.holding').switchClass('holding', 'giveable');
    $('.giveable').off().on('click', give_card);
    $('.card.holding').switchClass('holding', 'takeable');
    $('.takeable').off().on('click', take_card);
}

function give(card, data) {
    card.off().attr('class', 'pl-card').hide(200);
    $('#'+data.recipient+'-card-'+data.card).on('click', take_card).addClass('takeable').show(200);
    set_cities(data.available);
    ACTIONS++;
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
                } else {
                    $('.available').off();
                    buttons_off();
                    card.off().attr('class', 'pl-card down');
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
                }
            }).error(function(error) {console.log(errors)} );

    }
}

function select_recipient(event) {
    var recip = $(event.target).attr('id');
    var card_id = $('.down').attr('id').split('-')[1];
    $.getJSON( $SCRIPT_ROOT + '/_select_recipient', { card: card_id, selected: recip }).success(
        function(data) {
            var card = $('#card-'+data.card);
            escape_give_select(card, data);
            give(card, data);
            card.off();
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
    } else {
        $.getJSON( $SCRIPT_ROOT + '/_take', { card: Number(card_id),
                                              id: source_id}).success(
            function(data) {
                card.off().attr('class', 'card').hide(200);
                $('#card-'+card_id).on('click', give_card).show(200).addClass('giveable');
                set_cities(data.available);
                ACTIONS++;
                buttons_on();
                $('#undo-action').prop('disabled', ACTIONS===0);
            }).error(function(error) {console.log(errors)} );
    }
}

function escape_give_select(card, data) {
    buttons_on();
    $('.available').off().on('click', execute_move);
    card.off().on('click', give_card).addClass('giveable');
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
}
