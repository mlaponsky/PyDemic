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
    $("#card-"+card).children('div').attr('class', 'up');
    $("#card-"+card).hide();
    $("#pl-discard-"+card).show();
}

function undo_discard(card) {
    $('#card-'+card).show();
    $("#card-"+card).children('div').attr('class', 'up');
    $("#pl-discard-"+card).hide();
}

function give(card, data) {
    card.attr('class', 'pl-card').hide();
    card.children('div').off();
    $('#'+data.recipient+'-card-'+data.card).on('click', take_card).attr('class', 'card takeable').show();
    set_cities(data.available);
    ACTIONS++;
    $('#undo-action').prop('disabled', ACTIONS===0);
}

function give_card(event) {
    var card = $(event.target).parent();
    var card_id = card.attr('id').split('-')[1];
    $.getJSON( $SCRIPT_ROOT + '/_give_card', { card: Number(card_id) }).success(
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
                card.attr('class', 'pl-card down');
                card.children('div').off();
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
        }
    )
}

function select_recipient(event) {
    var recip = $(event.target).attr('id');
    var card_id = $('.down').attr('id').split('-')[1];
    $.getJSON( $SCRIPT_ROOT + '/_select_recipient', { card: card_id, selected: recip }).success(
        function(data) {
            var card = $('#card-'+data.card);
            escape_give_select(card, data);
            give(card, data);
            card.children('div').off();
        }).error(function(error) {console.log(errors)} );
}

function take_card(event) {
    var card = $(event.target).parent();
    var source_id = card.attr('id').split('-')[0]
    var card_id = card.attr('id').split('-')[2];
    $.getJSON( $SCRIPT_ROOT + '/_take', { card: Number(card_id),
                                          id: source_id}).success( function(data) {
            card.off().attr('class', 'card').hide();
            $('#card-'+card_id).on('click', give_card).show().attr('class', 'pl-card giveable');
            set_cities(data.available);
            ACTIONS++;
            buttons_on();
            $('#undo-action').prop('disabled', ACTIONS===0);
        })
}
