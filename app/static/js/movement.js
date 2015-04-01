function move(new_pos, data) {
    var city = document.getElementById(new_pos);
    var city_dims = city.getBoundingClientRect();
    var city_w = city_dims.width;
    var city_h = city_dims.height;
    var city_l = city_dims.left;
    var city_t = city_dims.top;
    var index = $('#'+data.player_id).parent().parent().index();
    var menu_on = 0;
    if ( $('body').hasClass('menu-push-toright') ) {
        menu_on = -1;
    } else if ( $('body').hasClass('menu-push-toleft') ) {
        menu_on = 1;
    }

    var player_t = city_t - 0.57*city_h - top_offset;
    var player_l = city_l + (index+1)*3*city_w/8 - left_offset + menu_on*menu_shift;

    set_giveable(data.hand, data.can_give);
    set_takeable(data.team_hands, data.can_take);
    $(".available").off();
    $(".available").attr("class", "unavailable");
    ACTIONS++;
    //Animate movement and set availability.
    $("#"+data.player_id+"-piece").stop().animate({left: player_l, top: player_t},
        function() {
            medic_with_cure(data, new_pos);
            set_cities(data.available);
            $("#undo-action").prop('disabled', ACTIONS === 0);
            var active = $(".active-player").attr('id').split('-')[1]
            if (data.player_id === active) {
                set_treatable(new_pos);
                $("#build-station").prop('disabled', !data.can_build);
                $("#make-cure").prop('disabled', !data.can_cure);
            } else {
                $("#build-station").prop('disabled', true);
                $("#make-cure").prop('disabled', true);
            }
    });

}

function execute_move(event) {
    var city = $(event.target);
    var new_pos = city.attr("id");
    var is_airlift = 0;
    if ( $('#card-48').hasClass('down') ){
        is_airlift = 1
    };
    $.getJSON($SCRIPT_ROOT + '/_move', { id: Number(new_pos),
                                         airlift: is_airlift }).success(function(data) {
        if (typeof data.available !== 'undefined') {
            move(new_pos, data);
            $('#logger').html("Moved from "+CARDS[data.origin].bold()+" to "+CARDS[new_pos].bold()+".");
            if (data.move === "charter") {
                discard(data.discard);
                $('#logger').html($('#logger').html()+" Discarded "+CARDS[data.discard].bold()+".");
            } else if (data.move === "fly") {
                discard(data.discard);
                $('#logger').html($('#logger').html()+" Discarded "+CARDS[data.discard].bold()+".");
            } else if (data.move === "airlift") {
                discard(data.discard)
                $('#logger').html($('#logger').html()+" Discarded "+CARDS[data.discard].bold()+".");
            }
            buttons_on();
            if (is_airlift === 1) {
                $('#name').off().attr('class', 'self-unchooseable');
                $('.role').off().attr('class', 'role');
                if ( $('#active-dispatcher').length !== 0 ) {
                    $('.role').off().on('click', select_player).attr('class', 'role choosable')
                }
                if (!body.hasClass('selecting')) {
                    team_toggle();
                } else {
                    body.removeClass('selecting');
                }
            }
        } else {
            // If there are multiple ways to move to new_pos
            city.attr("class", "selected");
            var selectable = data.selectable;
            buttons_off();
            for (var i=0; i<selectable.length; i++) {
                var card = $('#card-'+selectable[i]);
                card.attr('class', 'pl-card down').off().on('click', function(e) { select_discard(e) });
            }
            $(".action").off();
            $(".available").off();
            $(".available").attr("class", "unavailable holding");
            $('html').off().on( 'click', function( e ) {
                if ($( e.target ).parent().attr('class') !== 'down') {
                    escape_card_select( $('.pl-card.down') ) }} );
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) { escape_card_select( $('.pl-card.down') ) };
            });
        }
    }).error(function(error){console.log(error);});
};

function select_discard(event) {
    var image = $(event.target);
    var card_obj = image.parent();
    var card_id = card_obj.attr('id');
    var card_id_array = card_id.split('-');
    var card = card_id_array[1];
    var city_id = $(".selected").attr("id");
    console.log(Number(city_id));

    $.getJSON($SCRIPT_ROOT+'/_select_card_for_move', { card: Number(card), city_id: Number(city_id) }).success(function (data) {
                escape_card_select( $('.pl-card.down') );
                move(city_id, data);
                discard(card);
                $('#logger').html("Moved from "+CARDS[data.origin].bold()+" to "+CARDS[Number(city_id)].bold()+". Discarded "+CARDS[Number(card)].bold()+".");
                if (data.move === "station-fly") {
                    $('#logger').html($('#logger').html()+" (Cannot use this ability again this turn.)");
                }
                buttons_on();
    }).error(function(error){console.log(error);});
}
