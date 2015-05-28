function move(new_pos, data, is_airlift) {
    var map = Snap.select('#cities');
    var city = document.getElementById('city-'+new_pos);
    var city_dims = city.getBoundingClientRect();
    var city_w = city_dims.width;
    var city_h = city_dims.height;
    var city_l = city_dims.left;
    var city_t = city_dims.top;
    var index = $('#'+data.mover_id).parent().parent().index();
    var player_t = city_t - 0.57*city_h - top_offset;
    var player_l = city_l + (index+1)*3*city_w/8 - left_offset + menu_on*menu_shift;

    set_giveable(data.hand, data.can_give);
    set_takeable(data.team_hands, data.can_take);
    map.selectAll(".available").forEach( function(el) {
		el.unavailable();
	});
    ACTIONS++;
    //Animate movement and set availability.
    $("#"+data.mover_id+"-piece").stop().velocity({left: player_l, top: player_t},
        function() {
            medic_with_cure(data, new_pos);
            $("#undo-action").prop('disabled', ACTIONS === 0);
            if (data.player_id === ACTIVE) {
                if (PHASE < 4) {
                    set_treatable(data.player_pos);
                }
                $("#build-station").prop('disabled', !data.can_build);
                $("#make-cure").prop('disabled', !data.can_cure);
            } else {
                $("#build-station").prop('disabled', true);
                $("#make-cure").prop('disabled', true);
            }
            if (is_airlift === 1) {
                $('#name').off().attr('class', 'self-unchooseable');
                $('.role').off().attr('class', 'role');
                if ( $('#active-dispatcher').length !== 0 ) {
                    $('.role').off().on('click', select_player).attr('class', 'role choosable')
                }
                if (!body.hasClass('selecting') || PHASE === 4 ) {
                    team_toggle();
                } else {
                    body.removeClass('selecting');
                }
            }
            if (data.num_cards <= 7) {
                buttons_on();
            } else {
                TRASHING = 1;
                $('#logger').html( $('#logger').html() + ' Still over the card limit; choose another card to discard.');
                board_off();
                set_active_trash();
            }
            if (PHASE >= 4) {
                actions_off();
            } else {
                set_cities(data.available);
            }
    });

}

function execute_move(event) {
    var map = Snap.select('#cities');
    var city = $(event.target);
    var new_pos = city.attr("id").split('-')[1];
    var is_airlift = 0;
    var select = 0;
    if ( $('.event-card').hasClass('down') || $('#cp-store').hasClass('down')){
        is_airlift = 1
        if ( $('.card.down').length !== 0 ) {
            select  = $('.event-card.down').parent().parent().index();
        }
    };
    $.getJSON($SCRIPT_ROOT + '/_move', { id: Number(new_pos),
                                         airlift: is_airlift,
                                         index: select,
                                         trashing: TRASHING
                                       }).success(function(data) {
        if (typeof data.available !== 'undefined') {
            if (data.move === "drive") {
                $('#logger').html("Drove from "+CARDS[data.origin].bold()+" to "+CARDS[new_pos].bold()+".");
                PHASE = data.phase;
                $('#actions-'+String(PHASE)).attr('class', 'on');
            } else if (data.move === "charter") {
                $('#logger').html("Flew from "+CARDS[data.origin].bold()+" to "+CARDS[new_pos].bold()+".");
                discard(data.discard);
                PHASE = data.phase;
                $('#actions-'+String(PHASE)).attr('class', 'on');
            } else if (data.move === "fly") {
                $('#logger').html("Flew from "+CARDS[data.origin].bold()+" to "+CARDS[new_pos].bold()+".");
                discard(data.discard);
                PHASE = data.phase;
                $('#actions-'+String(PHASE)).attr('class', 'on');
            } else if (data.move === "airlift") {
                $('#logger').html("Airlifted "+ROLES[data.mover_id]+" from "+CARDS[data.origin].bold()+".");
                if ( !$('#cp-store').hasClass('down') ) {
                    discard(data.discard);
                } else {
                    $('#cp-store').hide(200);
                    $('#pl-discard-48').off().show(200).attr('class', 'graveyard');
                    STORE = 0;
                }
                $('.holding.down').removeClass('down').hide(200);
                if ( TRASHING === 1 ) {
                    ACTIONS--;
                }
            } else if (data.move === "dispatch") {
                $('#logger').html("Dispatched "+ROLES[data.player_id]+" from "+CARDS[data.origin].bold()+".");
                PHASE = data.phase;
                $('#actions-'+String(PHASE)).attr('class', 'on');
            } else if (data.move === "station-fly") {
                $('#logger').html("Flew from "+CARDS[data.origin].bold()+" to "+CARDS[new_pos].bold()+". Discarded "+CARDS[data.discard].bold()+". (Cannot use this ability again this turn.)");
                PHASE = data.phase;
                $('#actions-'+String(PHASE)).attr('class', 'on');
            } else if (data.move === "shuttle") {
                $('#logger').html("Shuttled from "+CARDS[data.origin].bold()+" to "+CARDS[new_pos].bold()+".");
                PHASE = data.phase;
                $('#actions-'+String(PHASE)).attr('class', 'on');
            }
            move(new_pos, data, is_airlift);
            if (PHASE === 4) {
                actions_off();
            }
        } else {
            // If there are multiple ways to move to new_pos
            map.select('#city-'+new_pos).selected();
            var selectable = data.selectable;
            buttons_off();
            for (var i=0; i<selectable.length; i++) {
                var card = $('#card-'+selectable[i]);
                if (card.hasClass('giveable') ) {
                    card.removeClass('giveable').addClass('holding');
                }
                card.addClass('down').off().on('click', function(e) { select_discard(e) });
            }
            $(".action").off();
            map.selectAll(".available").forEach( function(el) {
        		el.unavailable();
                el.addClass('marked');
        	});
            $('html').off().on( 'click', function( e ) {
                if ($( e.target ).parent().attr('class') !== 'down') {
                    escape_card_select( $('.pl-card.down') ) }} );
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) { escape_card_select( $('.pl-card.down') ) };
            });
            TRASHING = 0;
        }
    }).error(function(error){console.log(error);});
};

function select_discard(event) {
    var map = Snap.select('#cities');
    var image = $(event.target);
    var card_obj = image.parent();
    var card_id = card_obj.attr('id');
    var card_id_array = card_id.split('-');
    var card = card_id_array[1];
    var city_id = $(".selected").attr("id").split('-')[1];

    $.getJSON($SCRIPT_ROOT+'/_select_card_for_move', { card: Number(card), city_id: Number(city_id) }).success(function (data) {
                escape_card_select( $('.pl-card.down') );
                $('#logger').html("Flew from "+CARDS[data.origin].bold()+" to "+CARDS[Number(city_id)].bold()+".")
                discard(card);
                if (data.move === "station-fly") {
                    $('#logger').html($('#logger').html()+" (Cannot use this ability again this turn.)");
                }
                PHASE = data.phase;
                $('#actions-'+String(PHASE)).attr('class', 'on');
                move(city_id, data, 0);
                buttons_on();
                if (PHASE === 4) {
                    actions_off();
                }
    }).error(function(error){console.log(error);});
}
