function set_available(cities) {
    $(".available").attr("class", "unavailable");
    for (var i=0; i<cities.length; i++) {
        $("#"+cities[i]).attr("class", "available");
        $("#"+cities[i]).attr("onclick", "execute_move(this)");
    }
    $(".unavailable").removeAttr("onclick");
}

function move(new_pos, player_id, available) {
    var city = document.getElementById(new_pos);
    var city_dims = city.getBoundingClientRect();
    var city_w = city_dims.width;
    var city_h = city_dims.height;
    var city_l = city_dims.left;
    var city_t = city_dims.top;
    var player_l = 200;
    // Find the first open player position
    for (var j=0; j<4; j++) {
        if ( $("."+new_pos+"-"+String(j)).length == 0 ) {
            player_l = city_l + (j+1)*3*city_w/8;
            $("#"+player_id+"-piece").attr("class", new_pos+"-"+String(j));
            break;
        }
    }
    var player_t = city_t - 1.1*city_h;

    //Animate movement and set availability.
    $("#"+player_id+"-piece").animate({left: player_l, top: player_t});
    set_available(available);
}

function set_position(player, position) {
    var city = document.getElementById(position);
    var city_dims = city.getBoundingClientRect();
    var city_w = city_dims.width;
    var city_h = city_dims.height;
    var city_l = city_dims.left;
    var city_t = city_dims.top;

    player.width(5*city_w/8);
    var player_l;
    var player_t = city_t - 1.1*city_h

    for (var i=0; i<4; i++) {
        if ( $("."+position+"-"+String(i)).length == 0 ) {
            player_l = city_l + (i+1)*3*city_w/8;
            player.attr("class", position+"-"+String(i));
            break;
        }
    }
    player.offset({ left: player_l,
                    top: player_t }).css("position", "absolute");
}

function initial_load() {
    $.getJSON($SCRIPT_ROOT + '/_load').success(function(data) {
        var available = data.available;
        var pieces = data.pieces;
        var roles = data.roles;
        var positions = data.positions;

        set_available(available);

        for (var j=0; j<pieces.length; j++) {
            var player = $('<img/>');
            player.attr('id', roles[j]+"-piece" );
            player.attr('src', pieces[j]);
            set_position(player, positions[j]);
            player.css('z-index', 1000-j);
            player.appendTo('#map');
        }
    }).error(function(error){console.log(error);});
};

function execute_move(sel) {
    var new_pos = sel.getAttribute('id');
    $.getJSON($SCRIPT_ROOT + '/_move', { id: Number(new_pos) }).success(function(data) {
        if (typeof data.available !== 'undefined') {
            move(new_pos, data.player_id, data.available);
            if (data.move === "charter") {
                $("#card-"+data.discard).remove();
            } else if (data.move === "fly") {
                $('#card-'+data.discard).remove();
            }
        } else {
            // If there are multiple ways to move to new_pos
            sel.setAttribute("class", "selected");
            var selectable = data.selectable;
            for (var i=0; i<selectable.length; i++) {
                var card = $('#card-'+selectable[i]);
                card.attr("border", "3px solid #fffff0");
                card.attr("onclick", "select_card(this)");
            }
            $(".available").removeAttr("onclick");
            $(".available").attr("class", "unavailable holding");
            $('html').on( 'click', function(e) {
                if ($( e.target ).closest($(".selected").length === 0 )) {
                    escape_select() }} );
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) { escape_select() };
            });
        }
    }).error(function(error){console.log(error);});
};

function escape_select() {
    $(".holding").attr("class", "available");
    $(".selected").attr("class", "available");
    $(".available").attr("onclick", "execute_move(this)");
    $("#hand").children('img').removeAttr("border");
    $("#hand").children('img').removeAttr("onclick");
}

function select_card(sel) {
    var card_id = sel.getAttribute('id');
    var card_id_array = card_id.split('-');
    var card = card_id_array[1];
    var city_id = $(".selected").attr("id");

    $.getJSON($SCRIPT_ROOT+'/_select_card_for_move', { card: Number(card), city_id: Number(city_id) }).success(function (data) {
                move(city_id, data.player_id, data.available);
                $("#"+card_id).remove();
                $("#hand").children('img').removeAttr("border");
                $("#hand").children('img').removeAttr("onclick");
                $("#"+city_id).attr("class", "unavailable");
    }).error(function(error){console.log(error);});
}

window.onload = initial_load;
