function init_cities() {
    for (var i=0; i<48; i++) {
        $("#"+String(i)).click(execute_move);
        $("#"+String(i)).click(treat);
    }
}

function set_cities(cities) {
    $(".available").off().attr('class', 'unavailable');
    $(".selectable").off().attr('class', 'unavailable');
    for (var i=0; i<cities.length; i++) {
        $("#"+cities[i]).attr("class", "available");
        $("#"+cities[i]).off().on("click", execute_move);
    }
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

function set_selectable_players(active) {
    if (active === 'dispatcher') {
        $('.role').attr('class', 'role choosable');
        $('.role').click( select_player );
    } else {
        $('#team-players .role').attr('class', 'role');
        $('#team-players .role').off();
    }
}

function set_giveable(card) {
    $("#card-"+card).attr('class', 'pl-card giveable');
    $("#card-"+card).children('div').off().on('click', give_card);
}

function set_takeable(card, role) {
    $("#"+role+"-card-"+card).off().on('click', take_card).attr('class', 'card takeable');
}

function select_player(event) {
    var target = $(event.target);
    var select = target.parent().parent().index();
    $.getJSON( $SCRIPT_ROOT + '/_select_player', { index: select }).success(
        function(data) {
            if ($(".chosen").length !== 0) {
                $(".chosen").attr('class', 'role choosable');
            }
            $(".available").attr('class', 'unavailable');
            $(".treatable").attr('class', 'unavailable');
            set_cities(data.available);
            target.attr('class', 'role chosen');
            $('#build-station').prop('disabled', true);
            $('#make-cure').prop('disabled', true);
            escape_select_player(target);
        }
    ).error(function(error){console.log(error)});
}

function deselect_player() {
    var target = $(event.target);
    $.getJSON( $SCRIPT_ROOT + '/_select_player', { index: 0 }).success(
        function(data) {
            $(".available").attr('class', 'unavailable');
            set_cities(data.available);
            set_treatable(data.position);
            $('#build-station').prop('disabled', !data.can_build);
            $('#make-cure').prop('disabled', !data.can_cure);
            $('.role').attr('class', 'role choosable');
            $('.role').off().on('click', select_player );
        }
    )
}

function buttons_on() {
    $('#build-station').off().on('click', build_station);
    $('#make-cure').off().on('click', make_cure);
    $('#undo-action').off().on('click', undo);
}

function escape_select_player(target) {
    if ( $(".chosen").length !== 0 ) {
        $('html').keyup( function( e ) {
            if (e.keyCode === 27) { deselect_player() };
        });
        $('#name').off().on('click', deselect_player);
        target.off().on('click', deselect_player);
    }
}

function escape_card_select(objects) {
    $(".holding").attr("class", "available");
    $(".selected").attr("class", "available");
    $(".available").off().on("click", execute_move);
    objects.off().attr('class', 'up');
    $('html').off();
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

function escpae_station_select(available, city) {
    $(".holding").attr("class", "unavailable");
    set_cities(available);
    set_treatable(city);
    buttons_on();
    $("#build-station").attr('class', 'action');
    $('html').off()
}

function escape_cure_select() {
    $(".pl-card").children('div').attr('class', 'up').off();
    $(".pl-card").children('div');
    buttons_on();
    $('#make-cure').attr('class', 'action');
    $('html').off();
}
