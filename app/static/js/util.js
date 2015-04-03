function init_cities() {
    for (var i=0; i<48; i++) {
        $("#"+String(i)).click(execute_move);
        $("#"+String(i)).click(treat);
    }
}

function set_cities(cities) {
    $(".available").off().attr('class', 'unavailable');
    $(".selectable").off().attr('class', 'unavailable');
    $(".selected").off().attr('class', 'unavailable');
    for (var i=0; i<cities.length; i++) {
        $("#"+cities[i]).attr('class', 'available').off().on("click", execute_move);
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

function set_position(player, role, position, dims) {
    var city_w = dims.width;
    var city_h = dims.height;
    var city_l = dims.left;
    var city_t = dims.top;
    var index = $('#'+role).parent().parent().index();

    player.width(5*city_w/8);
    var player_t = city_t - 0.57*city_h - top_offset;
    var player_l = city_l + (index+1)*3*city_w/8 - left_offset;

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

function set_giveable(hand, can_give) {
    var roles = Object.keys(can_give);
    $('.pl-card').off().attr('class', 'pl-card');
    for (var n=0; n<hand.length; n++) {
        $("#card-"+String(hand[n])).show();
        for (var m=0; m<roles.length; m++) {
            if ( can_give[roles[m]][n] || hand[n] > 47 ) {
                $("#card-"+String(hand[n])).off().on('click', give_card).addClass('giveable');
            }
            if (hand[n] > 47) {
                $("#card-"+String(hand[n])).addClass('event-card');
            }
        }
    }
}

function set_takeable(team_hands, can_take) {
    var roles = Object.keys(can_take);
    $('.card').off().attr('class', 'card').hide();
    for (var p=0; p<team_hands.length; p++) {
        for (var n=0; n<team_hands[p].length; n++) {
            $("#"+roles[p]+"-card-"+String(team_hands[p][n])).show();
            if ( can_take[roles[p]][n] || team_hands[p][n] > 47 ) {
                $("#"+roles[p]+"-card-"+String(team_hands[p][n])).off().on('click', take_card).addClass('takeable');
            }
            if ( team_hands[p][n] > 47 ) {
                $("#"+roles[p]+"-card-"+String(team_hands[p][n])).addClass('event-card');
            }
        }
    }
}

function set_chosen_player(data, target) {
    if ($(".chosen").length !== 0) {
        $(".chosen").attr('class', 'role choosable');
    }
    $(".available").attr('class', 'unavailable');
    $(".treatable").attr('class', 'unavailable');
    set_cities(data.available);
    target.attr('class', 'role chosen');
    $('#build-station').prop('disabled', true);
    $('#make-cure').prop('disabled', true);
    $('#name').attr('class', 'self-chooseable')
}

function select_player(event) {
    var target = $(event.target);
    var select = target.parent().parent().index();
    $.getJSON( $SCRIPT_ROOT + '/_select_player', { index: select }).success(
        function(data) {
            set_chosen_player(data, target);
            escape_select_player(target);
        }
    ).error(function(error){console.log(error)});
}

function deselect_player() {
    var target = $(event.target);
    $.getJSON( $SCRIPT_ROOT + '/_select_player', { index: 0 }).success(
        function(data) {
            set_cities(data.available);
            set_treatable(data.position);
            $('#build-station').prop('disabled', !data.can_build);
            $('#make-cure').prop('disabled', !data.can_cure);
            $('.role').attr('class', 'role choosable');
            $('.role').off().on('click', select_player );
            $('.self-chooseable').attr('class', 'self-unchooseable');
        }
    )
}

function escape_select_player(target) {
    if ( $(".chosen").length !== 0 ) {
        $('html').keyup( function( e ) {
            if (e.keyCode === 27) { deselect_player() };
        });
        $('#name').off().on('click', deselect_player);
        buttons_on();
        target.off().on('click', deselect_player);
    }
}

function buttons_on() {
    $('#build-station').attr('class', 'action').off().on('click', build_station);
    $('#make-cure').attr('class', 'action').off().on('click', make_cure);
    $('#undo-action').attr('class', 'action').off().on('click', undo);
}

function buttons_off() {
    $('#build-station').attr('class', 'paused').off();
    $('#make-cure').attr('class', 'paused').off();
    $('#undo-action').attr('class', 'paused').off();
}

function escape_card_select(objects) {
    $(".marked").attr("class", "available");
    $(".selected").attr("class", "available");
    $(".available").off().on("click", execute_move);
    objects.off().removeClass('down')
    $('.holding').removeClass('holding').addClass('giveable');
    buttons_on();
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
    buttons_on();
    $('html').off();
}

function escape_cure_select() {
    $(".pl-card").children('div').attr('class', 'up').off();
    buttons_on();
    $('#make-cure').attr('class', 'action');
    $('html').off();
}
