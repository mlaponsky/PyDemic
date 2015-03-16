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

function give_card(event) {
    var card = $(event.target).parent();
    var card_id = card.attr('id').split('-')[1];
    $.getJSON( $SCRIPT_ROOT + '/_give_card', { card: Number(card_id) }).success(
        function(data) {
            if (typeof data.available !== 'undefined') {
                card.off().attr('class', 'pl-card').hide();
                $('#'+data.recipient+'-card-'+data.card).attr('class', 'card takeable').show();
                set_cities(data.available);
                ACTIONS++;
                $('#undo-action').prop('disabled', ACTIONS===0);
            }
        }
    )
}

function take_card(event) {
    var card = $(event.target).parent();
    var source_id = card.attr('id').split('-')[0]
    var card_id = card.attr('id').split('-')[2];
    $.getJSON( $SCRIPT_ROOT + '/_take', { card: Number(card_id),
                                          id: source_id}).success( function(data) {
            card.off().attr('class', 'card').hide();
            $('#card-'+card_id).show().attr('class', 'pl-card giveable');
            set_cities(data.available);
            ACTIONS++;
            $('#undo-action').prop('disabled', ACTIONS===0);
        })
}
