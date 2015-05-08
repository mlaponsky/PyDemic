function undo() {
    $.getJSON( $SCRIPT_ROOT + '/_undo').success( function(data) {
        data=data.result;
        undo_trash(data);
        if ( (data['act'] === "drive") || (data['act'] === "shuttle") || (data['act'] === "dispatch") ) {
            undo_move(data);
            PHASE--;
        } else if ((data['act'] === "charter") ||
                   (data['act'] === "fly") ||
                   (data['act'] === "station-fly")) {
            undo_discard(data['cards'], data['owner']);
            undo_move(data);
            PHASE--;
        } else if (data['act'] === "airlift") {
            undo_discard(data['cards'], data['owner']);
            undo_move(data);
        } else if (data['act'] === "build") {
            undo_station(data);
            PHASE--;
        } else if (data['act'] === "gg") {
            undo_station(data);
        } else if (data['act'] === "treat") {
            undo_treatment(data);
            PHASE--;
        } else if (data['act'] === "cure") {
            undo_cure(data);
            PHASE--;
        } else if (data['act'] === "take") {
            undo_take(data);
            PHASE--;
        } else if (data['act'] === "give") {
            undo_give(data);
            PHASE--;
        } else if (data['act'] === "rp") {
            undo_rp(data);
        } else if (data['act'] === "oqn") {
            undo_oqn(data);
        }
        ACTIONS--;
        $('#undo-action').prop('disabled', ACTIONS === 0);
    }).error(function(error){console.log(error)});
}

function undo_discard(card, owner) {
    if ($('.active-player').attr('id').split('-')[1] !== owner) {
        $('#'+owner+"-card-"+card).show(200);
    } else {
        $('#card-'+card).show(200);
    }
    $("#pl-discard-"+card).hide(200);
    $('#logger').html( $('#logger').html()+' Returned '+CARDS[Number(card)].bold()+' to the '+ROLES[owner].bold()+"'s hand.");
}

function undo_move(data) {
    var city = document.getElementById(String(data['origin']));
    var city_dims = city.getBoundingClientRect();
    var city_w = city_dims.width;
    var city_h = city_dims.height;
    var city_l = city_dims.left;
    var city_t = city_dims.top;
    var index = $('#'+data['id']).parent().parent().index();
    var menu_on = 0;
    if ( $('body').hasClass('menu-push-toright') ) {
        menu_on = -1;
    } else if ( $('body').hasClass('menu-push-toleft') ) {
        menu_on = 1;
    }
    var player_t = city_t - 0.57*city_h;
    var player_l = city_l + (index+1)*3*city_w/8;
    for (var i=0; i<data['cubes'].length; i++) {
        if ($(".city-"+String(data['destination'])+".cube-"+String(i)).length !== data['cubes'][i]) {
            var cube_counter = document.getElementById(String(i)+"-cnt").getElementsByTagName('tspan')[0].textContent;
            var cubes_left = Number(cube_counter);
            var prev_city = document.getElementById(String(data['destination']));
            var prev_dims = prev_city.getBoundingClientRect();
            add_cubes(String(data['destination']), prev_dims, String(i), data['rows'][i], data['cubes'][i]);
            cubes_left += data['cubes'][i];
            document.getElementById(String(i)+"-cnt").getElementsByTagName('tspan')[0].textContent = String(cubes_left);
        }
    }

    $(".available").off();
    $(".available").attr("class", "unavailable");
    //Animate movement and set availability.
    $("#"+data['id']+"-piece").offset({left: player_l, top: player_t});
    set_cities(data['available']);
    if ( $('#'+data['id']).length === 0 ) {
        set_treatable(data['origin'])
    }
    set_giveable(data['hand'], data['give']);
    set_takeable(data['team_hands'], data['take']);
    $('#logger').html("(UNDO) Return "+ROLES[data['id']].bold()+" to "+CARDS[data['origin']].bold()+".");
    $("#build-station").prop('disabled', !data['can_build']);
    $("#make-cure").prop('disabled', !data['can_cure']);
}

function undo_station(data) {
    var city = Number(data['origin']);
    console.log($('#station-'+data['origin']));
    $('#station-'+data['origin']).attr('class', 'unbuilt').hide();
    $('#logger').html('(UNDO) Removed station from '+CARDS[city].bold()+'.');
    if ( data['removed'] !== 'none' ) {
        $('#station-'+data['removed']).attr('class', 'built').show();
        $('#logger').html($('#logger').html()+' Returned station to '+CARDS[Number(data['removed'])].bold()+'.')
    }
    if ( data['discard'] !== '-1') {
        undo_discard(data['discard'], data['owner']);
    }
    set_cities(data['available']);
    if (data['discard'] !== '50' || data['can_build']) {
        $("#build-station").prop('disabled', false);
    }
    if ( data['removed'] === 'none' ) {
        var stations_left = Number(document.getElementById("research-cnt").getElementsByTagName('tspan')[0].textContent)

        if (stations_left < 6)
        document.getElementById("research-cnt").getElementsByTagName('tspan')[0].textContent = stations_left + 1;
    }
}

function undo_treatment(data) {
    var city = document.getElementById(data['origin']);
    var dims = city.getBoundingClientRect();
    add_cubes(data['origin'], dims, data['color'],
                Number(data['color']), data['rows'][Number(data['color'])], data['cubes']);

    var cubes_left = Number(document.getElementById(data['color']+"-cnt").getElementsByTagName('tspan')[0].textContent)
    document.getElementById(data['color']+"-cnt").getElementsByTagName('tspan')[0].textContent = cubes_left - data['removed'];
    set_treatable(data['origin']);
    $('#logger').html('(UNDO) Returned '+String(data['removed'])+' '+COLORS[Number(data['color'])].bold()+' cube(s) to '+CARDS[Number(data['origin'])].bold()+'.');
}

function undo_cure(data) {
    $('#logger').html('(UNDO) Removed '+COLORS[data['color']]+' cure. Returned cards to hand.');
    set_cure(String(data['color']), data['cured']);
    for ( var i=0; i<data['cards'].length; i++ ) {
        undo_discard(data['cards'][i], data['id']);
    }
    var city = document.getElementById(String(data['origin']));
    var dims = city.getBoundingClientRect();
    add_cubes(String(data['origin']), dims, String(data['color']),
                data['color'], data['rows'][Number(data['color'])], data['cubes']);

    if ( $("#medic").length !== 0) {
        var cubes_left = Number(document.getElementById(data['color']+"-cnt").getElementsByTagName('tspan')[0].textContent)

        document.getElementById(data['color']+"-cnt").getElementsByTagName('tspan')[0].textContent = cubes_left - data['cubes'];
    }
    $('#make-cure').prop('disabled', false);
    $('#make-cure').attr('class', 'action');
}

function undo_take(data) {
    $('#'+data['giver']+'-card-'+data['card']).on('click', take_card).attr('class', 'card takeable').show(200);
    $('#card-'+data['card']).off().hide(200).attr('class', 'pl-card');
    set_cities(data['available']);
    $('#logger').html('(UNDO) Returned '+CARDS[Number(data['card'])].bold()+' to the '+ROLES[data['giver']].bold()+'.');
}

function undo_give(data) {
    $('#'+data['taker']+'-card-'+data['card']).off().attr('class', 'card').hide(200);
    $('#card-'+data['card']).off().on('click', give_card).attr('class', 'pl-card giveable').show(200);
    set_cities(data['available']);
    $('#logger').html('(UNDO) Returned '+CARDS[Number(data['card'])].bold()+' to the '+ROLES[data['giver']]+'.');
}

function undo_rp(data) {
    $('#infect-discard-'+String(data['deleted'])).off().attr('class', 'infect-discard');
    $('#logger').html('(UNDO) Returned '+CARDS[data['deleted']].bold()+' from the graveyard.')
    undo_discard('52', data['owner']);
}

function undo_oqn(data) {
    $('#logger').html('(UNDO) ');
    undo_discard('51', data['owner']);
}

function undo_trash(data) {
    var trash = data['trash'];
    if (typeof trash !== 'undefined') {
        if (trash['act'] === 'airlift') {
            undo_discard(trash['cards'], trash['owner']);
            undo_move(trash);
        } else if (trash['act'] === 'rp') {
            undo_rp(trash);
        } else if (trash['act'] === 'gg') {
            undo_station(trash);
        } else if (trash['act'] === 'oqn') {
            undo_oqn(trash);
        } else if (trash['act'] === 'trash') {
            undo_discard(trash['cards'], trash['owner']);
            set_cities(trash['available']);
        }
    }
}
