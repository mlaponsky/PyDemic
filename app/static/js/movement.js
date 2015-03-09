function move(new_pos, data) {
    var city = document.getElementById(new_pos);
    var city_dims = city.getBoundingClientRect();
    var city_w = city_dims.width;
    var city_h = city_dims.height;
    var city_l = city_dims.left;
    var city_t = city_dims.top;
    var player_l;
    var player_t = city_t - 0.57*city_h - top_offset;
    // Find the first open player position
    for (var j=0; j<4; j++) {
        if ( $("."+new_pos+"-"+String(j)).length === 0 ) {
            player_l = city_l + (j+1)*3*city_w/8 - left_offset;
            $("#"+data.player_id+"-piece").attr("class", new_pos+"-"+String(j));
            break;
        }
    }
    $(".available").off();
    $(".available").attr("class", "unavailable");
    ACTIONS++;
    //Animate movement and set availability.
    $("#"+data.player_id+"-piece").stop().animate({left: player_l, top: player_t}, function() { medic_with_cure(data, new_pos);
                 set_cities(data.available, new_pos);
                 $("#build-station").prop('disabled', !data.can_build);
                 $("#make-cure").prop('disabled', !data.can_cure),
                 $("#undo-action").prop('disabled', ACTIONS === 0);
    });

}

function execute_move(event) {
    var city = event.target;
    var new_pos = city.getAttribute("id");
    $.getJSON($SCRIPT_ROOT + '/_move', { id: Number(new_pos) }).success(function(data) {
        if (typeof data.available !== 'undefined') {
            move(new_pos, data);
            $("#undo-action").prop('disabled', ACTIONS === 0);
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
                card.children('div').css("border", "4px solid #fffff0");
                card.children('div').off().on('click', function(e) { select_discard(e) });
            }
            $(".available").off("click");
            $(".available").attr("class", "unavailable holding");
            $('html').off().on( 'click', function( e ) {
                if ($( e.target ).closest($(".selected").length === 0 )) {
                    escape_card_select( $('#hand').children('img')) }} );
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) { escape_card_select( $('#hand').children('img') ) };
            });
        }
    }).error(function(error){console.log(error);});
};

function select_discard(event) {
    var image = event.target;
    var card_obj = image.parentNode;
    var card_id = card_obj.getAttribute('id');
    var card_id_array = card_id.split('-');
    var card = card_id_array[1];
    var city_id = $(".selected").attr("id");

    $.getJSON($SCRIPT_ROOT+'/_select_card_for_move', { card: Number(card), city_id: Number(city_id) }).success(function (data) {
                move(city_id, data);
                $("#"+card_id).remove();
                $(".pl-card").children('div').css("border", '');
                $(".pl-card").children('div').off("click");
    }).error(function(error){console.log(error);});
}
