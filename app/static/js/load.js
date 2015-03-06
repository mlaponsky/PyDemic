function initial_load() {
    $.getJSON($SCRIPT_ROOT + '/_load').success(function(data) {
        var available = data.available;
        var pieces = data.pieces;
        var roles = data.roles;
        var positions = data.positions;
        var cubes = data.cubes;
        var images = data.colors;
        var rows = data.cube_rows
        var rs = data.rs

        place_cubes(cubes, rows, images);
        init_cities();
        set_cities(available, positions[0]);
        set_stations(rs);

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

window.onload = initial_load;
