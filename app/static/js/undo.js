function undo() {
    $.getJSON( $SCRIPT_ROOT + '/_undo').success( function(data) {
        if ( (data.result['act'] === "drive") || (data.result['act'] === "shuttle") || (data.result['act'] === "dispatch") ) {
            undo_move(data.result['data']);
            ACTIONS--;
        } else if ((data.result['act'] === "charter") ||
                   (data.result['act'] === "fly") ||
                   (data.result['act'] === "station-fly") ||
                   (data.result['act'] === "airlift")) {
            undo_move(data.result['data']);
            undo_discard(data.result['data']['cards'], data.result['data']['owner']);
            ACTIONS--;
        } else if ( (data.result['act'] === "build") ||
                    (data.result['act'] === "gg") ) {
            undo_station(data.result['data']);
            ACTIONS--;
        } else if (data.result['act'] === "treat") {
            undo_treatment(data.result['data']);
            ACTIONS--;
        } else if (data.result['act'] === "cure") {
            undo_cure(data.result['data']);
            ACTIONS--;
        } else if (data.result['act'] === "take") {
            undo_take(data.result['data']);
            ACTIONS--;
        } else if (data.result['act'] === "give") {
            undo_give(data.result['data']);
            ACTIONS--;
        } else if (data.result['act'] === "rp") {
            undo_rp(data.result['data']);
            ACTIONS--;
        }
        $('#undo-action').prop('disabled', ACTIONS === 0);
    }).error(function(error){console.log(error)});
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
            add_cubes(String(data['destination']), prev_dims, String(i), data['color_img'][i], data['rows'][i], data['cubes'][i]);
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
                data['color_img'][Number(data['color'])], data['rows'][Number(data['color'])], data['cubes']);

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
                data['color_img'][data['color']], data['rows'][Number(data['color'])], data['cubes']);

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
    $('#infect-discard-'+String(data['deleted'])).off().attr('class', 'card');
    undo_discard('52', data['owner']);
}
