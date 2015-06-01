function undo() {
    $.getJSON( $SCRIPT_ROOT + '/_undo').success( function(data) {
        action=data.result;
        undo_trash(action);
        if ( (action['act'] === "drive") || (action['act'] === "shuttle") || (action['act'] === "dispatch") ) {
            undo_move(action);$('#actions-'+String(PHASE)).attr('class', 'off');
            PHASE--;
        } else if ((action['act'] === "charter") ||
                   (action['act'] === "fly") ||
                   (action['act'] === "station-fly")) {
            undo_discard(action['cards'], action, action['owner']);
            undo_move(action);
            $('#actions-'+String(PHASE)).attr('class', 'off');
            PHASE--;
        } else if (action['act'] === "airlift") {
            undo_discard(action['cards'], action, action['owner']);
            undo_move(action);
        } else if (action['act'] === "build") {
            undo_station(action);
            $('#actions-'+String(PHASE)).attr('class', 'off');
            PHASE--;
        } else if (action['act'] === "gg") {
            undo_station(action);
        } else if (action['act'] === "treat") {
            undo_treatment(action);
            $('#actions-'+String(PHASE)).attr('class', 'off');
            PHASE--;
        } else if (action['act'] === "cure") {
            undo_cure(action);
            $('#actions-'+String(PHASE)).attr('class', 'off');
            PHASE--;
        } else if (action['act'] === "take") {
            undo_take(action);
            $('#actions-'+String(PHASE)).attr('class', 'off');
            PHASE--;
        } else if (action['act'] === "give") {
            undo_give(action);
            $('#actions-'+String(PHASE)).attr('class', 'off');
            PHASE--;
        } else if (action['act'] === "rp") {
            undo_rp(action);
        } else if (action['act'] === "oqn") {
            undo_oqn(action);
        } else if (action['act'] === "store") {
            undo_store(action);
        }
        ACTIONS--;
        if (PHASE < 5) {
            set_cities(data.available);
            set_giveable(data.hand, data.can_give);
            set_takeable(data.team_hands, data.can_take);
            $('#build-station').prop('disabled', !data.can_build);
            $('#make-cure').prop('disabled', !data.can_cure);
        }
        if (ACTIVE === 'cp') {
            set_cp_store();
        }
        events_on();
        $('#undo-action').prop('disabled', ACTIONS === 0);
        set_next_button();
    }).error(function(error){console.log(error)});
}

function undo_discard(card, action, owner) {
    if (action.is_stored) {
        $('#cp-store').off().on('click', select_store).show(200).attr('class', '.store-'+String(card)).addClass('giveable').attr('src', 'static/img/player_cards/pl-'+String(card)+'.svg');
    } else if ($('.active-player').attr('id').split('-')[1] !== owner) {
        $('#'+owner+"-card-"+card).show(200);
    } else {
        $('#card-'+card).show(200);
    }
    $("#pl-discard-"+card).hide(200);
    $('#logger').html( $('#logger').html()+' Returned '+CARDS[Number(card)].bold()+' to the '+ROLES[owner].bold()+"'s hand.");
}

function undo_move(action) {
    var map = Snap.select('#cities');
    var city = document.getElementById('city-'+String(action['origin']));
    var city_dims = city.getBoundingClientRect();
    var city_w = city_dims.width;
    var city_h = city_dims.height;
    var city_l = city_dims.left;
    var city_t = city_dims.top;
    var index = $('#'+action['mover']).parent().parent().index();
    var menu_on = 0;
    if ( $('body').hasClass('menu-push-toright') ) {
        menu_on = -1;
    } else if ( $('body').hasClass('menu-push-toleft') ) {
        menu_on = 1;
    }
    var player_t = city_t - 0.57*city_h;
    var player_l = city_l + (index+1)*3*city_w/8;
    for (var i=0; i<action['cubes'].length; i++) {
        if ($(".city-"+String(action['destination'])+".cube-"+String(i)).length !== action['cubes'][i]) {
            var cube_counter = document.getElementById(String(i)+"-cnt").getElementsByTagName('tspan')[0].textContent;
            var cubes_left = Number(cube_counter);
            var prev_city = document.getElementById('city-'+String(action['destination']));
            var prev_dims = prev_city.getBoundingClientRect();
            add_cubes(String(action['destination']), prev_dims, String(i), action['rows'][i], action['cubes'][i]);
            stop_svg(action['origin']);
            if ( $.inArray(Number(action['origin']), action['at_risk']) !== -1 ) {
                pulse_svg(action['origin']);
            }
            cubes_left += action['cubes'][i];
            document.getElementById(String(i)+"-cnt").getElementsByTagName('tspan')[0].textContent = String(cubes_left);
        }
    }

    map.selectAll(".available").forEach( function(el) {
		el.unavailable();
	});
    $("#"+action['mover']+"-piece").offset({left: player_l, top: player_t});
    set_cities(action['available']);
    if ( action['mover'] === ACTIVE ) {
        set_treatable(action['origin'])
    }
    set_giveable(action['hand'], action['give']);
    set_takeable(action['team_hands'], action['take']);
    $('#logger').html("(UNDO) Return "+ROLES[action['mover']].bold()+" to "+CARDS[action['origin']].bold()+".");
    $("#build-station").prop('disabled', !action['can_build']);
    $("#make-cure").prop('disabled', !action['can_cure']);
}

function undo_station(action) {
    var city = Number(action['origin']);
    $('#station-'+action['origin']).attr('class', 'unbuilt').hide();
    $('#logger').html('(UNDO) Removed station from '+CARDS[city].bold()+'.');
    if ( action['removed'] !== '-1' ) {
        $('#station-'+action['removed']).attr('class', 'built').show();
        $('#logger').html($('#logger').html()+' Returned station to '+CARDS[Number(action['removed'])].bold()+'.')
    }
    if ( action['cards'] !== -1) {
        undo_discard(action['cards'], action, action['owner']);
    }
    set_cities(action['available']);
    if (action['cards'] !== '50' || action['can_build']) {
        $("#build-station").prop('disabled', false);
    }
    if ( action['removed'] === 'none' ) {
        var stations_left = Number(document.getElementById("research-cnt").getElementsByTagName('tspan')[0].textContent)

        if (stations_left < 6)
        document.getElementById("research-cnt").getElementsByTagName('tspan')[0].textContent = stations_left + 1;
    }
    events_on();
}

function undo_treatment(action) {
    var city = document.getElementById('city-'+action['origin']);
    var dims = city.getBoundingClientRect();
    add_cubes(action['origin'], dims, action['color'],
                action['rows'][Number(action['color'])], action['removed'], action['at_risk']);
    stop_svg(action['origin']);
    if ( $.inArray(Number(action['origin']), action['at_risk']) !== -1 ) {
        pulse_svg(action['origin']);
    }

    var cubes_left = Number(document.getElementById(action['color']+"-cnt").getElementsByTagName('tspan')[0].textContent)
    document.getElementById(action['color']+"-cnt").getElementsByTagName('tspan')[0].textContent = cubes_left - action['removed'];
    set_treatable(action['origin']);
    $('#logger').html('(UNDO) Returned '+String(action['removed'])+' '+COLORS[Number(action['color'])].bold()+' cube(s) to '+CARDS[Number(action['origin'])].bold()+'.');
}

function undo_cure(action) {
    set_cure(String(action['color']), action['cured']);
    for ( var i=0; i<action['cards'].length; i++ ) {
        undo_discard(action['cards'][i], action, action['id']);
    }
    var city = document.getElementById('city-'+String(action['origin']));
    var dims = city.getBoundingClientRect();
    if ($(".city-"+String(action['origin'])+".cube-"+String(action['color'])).length !== action['cubes']) {
        var cube_counter = document.getElementById(String(action['color'])+"-cnt").getElementsByTagName('tspan')[0].textContent;
        var cubes_left = Number(cube_counter);
        add_cubes(String(action['origin']), dims, String(action['color']), action['rows'][action['color']], action['cubes']);
        stop_svg(action['origin']);
        if ( $.inArray(Number(action['origin']), action['at_risk']) !== -1 ) {
            pulse_svg(action['origin']);
        }

        cubes_left += action['cubes'];
        document.getElementById(String(action['color'])+"-cnt").getElementsByTagName('tspan')[0].textContent = String(cubes_left);
    }
    $('#logger').html('(UNDO) Removed '+COLORS[action['color']]+' cure. Returned cards to hand.');
    $('#make-cure').prop('disabled', false);
    $('#make-cure').attr('class', 'action');
}

function undo_take(action) {
    $('#'+action['giver']+'-card-'+action['card']).on('click', take_card).attr('class', 'card takeable').show(200);
    $('#card-'+action['card']).off().hide(200).attr('class', 'pl-card');
    set_cities(action['available']);
    $('#logger').html('(UNDO) Returned '+CARDS[Number(action['card'])].bold()+' to the '+ROLES[action['giver']].bold()+'.');
}

function undo_give(action) {
    $('#'+action['taker']+'-card-'+action['card']).off().attr('class', 'card').hide(200);
    $('#card-'+action['card']).off().on('click', give_card).attr('class', 'pl-card giveable').show(200);
    set_cities(action['available']);
    $('#logger').html('(UNDO) Returned '+CARDS[Number(action['card'])].bold()+' to the '+ROLES[action['giver']]+'.');
}

function undo_rp(action) {
    $('#infect-discard-'+String(action['deleted'])).off().attr('class', 'infect-discard');
    $('#logger').html('(UNDO) Returned '+CARDS[action['deleted']].bold()+' from the graveyard.')
    undo_discard('52', action, action['owner']);
}

function undo_oqn(action) {
    $('#logger').html('(UNDO) ');
    undo_discard('51', action, action['owner']);
}

function undo_store(action) {
    $('#logger').html('(UNDO) Return '+CARDS[action['card']]+' to the discard pile.');
    $('#cp-store').off().hide();
    $('#pl-discard-'+String(action['card'])).off().on('click', store_on_cp).addClass('pl-discard takeable').show();
}

function undo_trash(action) {
    var trash = action['trash'];
    if (typeof trash !== 'undefined') {
        if (trash['act'] === 'airlift') {
            undo_discard(trash['cards'], action, trash['owner']);
            undo_move(trash);
        } else if (trash['act'] === 'rp') {
            undo_rp(trash);
        } else if (trash['act'] === 'gg') {
            undo_station(trash);
        } else if (trash['act'] === 'oqn') {
            undo_oqn(trash);
        } else if (trash['act'] === 'trash') {
            undo_discard(trash['cards'], action, trash['owner']);
            set_cities(trash['available']);
        }
    }
}
