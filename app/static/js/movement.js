function move(new_pos, data) {
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
            $("#"+data.player_id+"-piece").attr("class", new_pos+"-"+String(j));
            break;
        }
    }
    var player_t = city_t - 1.1*city_h;
    $(".available").off("click");
    $(".available").attr("class", "unavailable");
    //Animate movement and set availability.
    $("#"+data.player_id+"-piece").stop().animate({left: player_l, top: player_t}, function() { medic_with_cure(data, new_pos);
                 set_cities(data.available, new_pos); });
}

function set_position(player, position, dims) {
    var city_w = dims.width;
    var city_h = dims.height;
    var city_l = dims.left;
    var city_t = dims.top;

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

function execute_move(event) {
    var city = event.target;
    var new_pos = city.getAttribute("id");
    $.getJSON($SCRIPT_ROOT + '/_move', { id: Number(new_pos) }).success(function(data) {
        if (typeof data.available !== 'undefined') {
            move(new_pos, data);
            if (data.move === "charter") {
                $("#card-"+data.discard).remove();
            } else if (data.move === "fly") {
                $('#card-'+data.discard).remove();
            }
        } else {
            // If there are multiple ways to move to new_pos
            city.setAttribute("class", "selected");
            var selectable = data.selectable;
            for (var i=0; i<selectable.length; i++) {
                var card = $('#card-'+selectable[i]);
                card.css("border", "3px solid #fffff0");
                card.on('click', function(e) { select_card(e) });
            }
            $(".available").off("click");
            $(".available").attr("class", "unavailable holding");
            $('html').on( 'click', function( e ) {
                if ($( e.target ).closest($(".selected").length === 0 )) {
                    escape_card_select( $('#hand').children('img')) }} );
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) { escape_card_select( $('#hand').children('img') ) };
            });
        }
    }).error(function(error){console.log(error);});
};

function select_card(event) {
    var card_obj = event.target;
    var card_id = card_obj.getAttribute('id');
    var card_id_array = card_id.split('-');
    var card = card_id_array[1];
    var city_id = $(".selected").attr("id");

    $.getJSON($SCRIPT_ROOT+'/_select_card_for_move', { card: Number(card), city_id: Number(city_id) }).success(function (data) {
                move(city_id, data);
                $("#"+card_id).remove();
                $("#hand").children('img').removeAttr("border");
                $("#hand").children('img').off("click");
    }).error(function(error){console.log(error);});
}
