var ACTIONS = 0;
function initial_load() {
    $.getJSON($SCRIPT_ROOT + '/_load').success(function(data) {
        var available = data.available;
        var pieces = data.pieces;
        var roles = data.roles;
        var positions = data.positions;
        var cubes = data.cubes;
        var images = data.colors;
        var rows = data.cube_rows
        var cures = data.cures
        var rs = data.rs
        var can_build = data.can_build;
        var can_cure = data.can_cure;
        var hand = data.hand;
        actions = data.actions;
        ACTIONS = actions.length;

        place_cubes(cubes, rows, images);
        init_cities();
        set_cities(available, positions[0]);
        set_stations(rs);

        for (var i=0; i<cures.length; i++) {
            set_cure(String(i), cures[i]);
        }

        $('.pl-name').css('background', "url("+data.role_img+") no-repeat center center");
        for (var n=0; n<hand.length; n++) {
            $("#card-"+String(hand[n])).children('div').css('background', "url("+data.cards[hand[n]]['player_card']+") no-repeat center center");
            $("#card-"+String(hand[n])).children('div').css('background-size', 'contain');
        }
        $('#build-station').prop('disabled', !can_build);
        $('#make-cure').prop('disabled', !can_cure);
        $('#undo-action').prop('disabled', (ACTIONS === 0))

        for (var j=0; j<pieces.length; j++) {
            var player = $('<img/>');
            player.attr('id', roles[j]+"-piece" );
            player.attr('src', pieces[j]);
            var city = document.getElementById(positions[j]);
            var city_dims = city.getBoundingClientRect();
            set_position(player, positions[j], city_dims);
            player.css('z-index', 1000-j);
            player.css('pointer-events', 'none');
            player.appendTo('#map');
        }

    }).error(function(error){console.log(error);});
};
