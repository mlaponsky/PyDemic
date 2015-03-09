function select_card(event) {
    var card_obj = $(event.target);
    if (card_obj.attr('class') === 'down') {
        console.log(card_obj.attr('class'));
        card_obj.attr('class', 'up');
        card_obj.css('border', '3px solid #fffff0');
    } else if (card_obj.attr('class') === 'up') {
        console.log(card_obj.attr('class'));
        card_obj.attr('class', 'down');
        card_obj.css('border', '');
    }
}

function create_card(city, data) {
    var card = $('<li class="pl-card"></li>');
    card.attr( 'id', "card-"+String(city) );
    var image = $('<div></div>');
    image.attr('title', data['name'] + '\n' + data['description'] );
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
