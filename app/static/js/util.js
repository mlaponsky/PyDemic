function init_cities() {
    for (var i=0; i<48; i++) {
        $("#"+String(i)).click(execute_move);
        $("#"+String(i)).click(treat);
    }
}

function set_cities(cities, position) {
    for (var i=0; i<cities.length; i++) {
        $("#"+cities[i]).attr("class", "available");
        $("#"+cities[i]).off().on("click", execute_move);
    }
    set_treatable(position);
    $(".unavailable").off('click');
}

function set_treatable(position) {
    if ( $(".city-"+position).length !== 0 ) {
        $("#"+position).attr("class", "treatable");
        $("#"+position).off().on("click", treat);
    } else {
        $("#"+position).attr("class", "unavailable");
        $("#"+position).off();
    }
}

function set_position(player, position, dims) {
    var city_w = dims.width;
    var city_h = dims.height;
    var city_l = dims.left;
    var city_t = dims.top;

    player.width(5*city_w/8);
    var player_l;
    var player_t = city_t - 0.57*city_h - top_offset;

    for (var i=0; i<4; i++) {
        if ( $("."+position+"-"+String(i)).length == 0 ) {
            player_l = city_l + (i+1)*3*city_w/8 - left_offset;
            player.attr("class", position+"-"+String(i));
            break;
        }
    }
    player.offset({ left: player_l,
                    top: player_t }).css("position", "absolute");
}

function set_cure(color, cured) {
    if (cured === 1) {
        document.getElementById("cure-"+color).getElementsByTagName('tspan')[0].textContent = '✓';
    } else if (cured === 2) {
        document.getElementById("cure-"+color).getElementsByTagName('tspan')[0].textContent = '✕';
    } else {
        document.getElementById("cure-"+color).getElementsByTagName('tspan')[0].textContent = '○';
    }
}

function escape_card_select(objects) {
    $(".holding").attr("class", "available");
    $(".selected").attr("class", "available");
    $(".available").off().on("click", execute_move);
    objects.css("border", '');
    objects.off("click");
    $('html').off('click');
    $('html').off('keyup');
}

function escape_cube_select(objects, city) {
    $(".holding").attr("class", "available");
    $(".selected").attr("class", "available");
    $(".available").off().on("click", execute_move);
    set_treatable(city);
    objects.css("border", '');
    objects.off();
    objects.css("pointer-events", "none");
    $('html').off();
}

function escape_station_select(available, city) {
    $(".holding").attr("class", "unavailable");
    set_cities(available, city);
    $("#build-station").attr('class', 'action');
}
