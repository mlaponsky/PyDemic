function undo() {
    $.getJSON( $SCRIPT_ROOT + '/_undo').success( function(data) {
        if ( (data.result['act'] === "drive") || (data.result['act'] === "shuttle") ) {
            undo_move(data.result['data']);
            ACTIONS--;
        } else if ((data.result['act'] === "charter") || (data.result['act'] === "fly")) {
            undo_move(data.result['data']);
            undo_discard(data.result['data']);
            ACTIONS--;
        } else if (data.result['act'] === "build") {
            undo_station(data.result['data']);
            ACTIONS--;
        } else if (data.result['act'] === "treat") {
            undo_treatment(data.result['data']);
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
    var player_l;
    var player_t = city_t - 0.57*city_h;
    // Find the first open player position
    for (var j=0; j<4; j++) {
        if ( $("."+String(data['origin'])+"-"+String(j)).length === 0 ) {
            player_l = city_l + (j+1)*3*city_w/8;
            $("#"+data['role']+"-piece").attr("class", String(data['origin'])+"-"+String(j));
            break;
        }
    }
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
    $("#"+data['role']+"-piece").offset({left: player_l, top: player_t});
    set_cities(data['available'], data['origin']);
    $("#build-station").prop('disabled', !data['can_build']);
    $("#make-cure").prop('disabled', !data['can_cure']);
}

function undo_discard(data) {
    var city = Number(data['discard']);
    var card_data = data['card'];
    create_card(city, card_data);
}

function undo_station(data) {
    var city = Number(data['position']);
    console.log(city);
    $('#station-'+data['position']).remove();
    if ( data['discard'] !== 'none') {
        undo_discard(data);
    }
    set_cities(data['available'], data['position']);
    ("#build-station").prop('disabled', false);
}

function undo_treatment(data) {
    var city = document.getElementById(data['city']);
    var dims = city.getBoundingClientRect();
    add_cubes(data['city'], dims, data['color'], data['image'], data['row'], data['num_cubes']);

    var cubes_left = document.getElementById(data['color']+"-cnt").getElementsByTagName('tspan')[0].textContent
    cubes_left = String(Number(cubes_left) + data['num_cubes']);
}
