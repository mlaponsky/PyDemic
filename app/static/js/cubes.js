function create_cube(position, dims, color, image, num, row) {
    var cube = $('<img/>');
    var class_name = "city-"+position + " " + "cube-"+color;
    cube.attr("class", class_name);
    cube.attr("src", image);
    cube.width(dims.width/2.2);
    cube_l = dims.left + dims.width/3 + (num)*dims.width/2.2;
    cube_t = dims.top + dims.height/2.5 + (row-1)*dims.width/2.5;
    cube.offset({ left: cube_l, top: cube_t }).css('position', 'absolute');
    cube.css('z-index', 900);
    cube.css('pointer-events', 'none');
    cube.appendTo('#map');
}

function create_cube_row(position, dims, color, image, row, total) {
    for (var num=0; num<total; num++) {
        create_cube(position, dims, String(color), image, num, row);
    }
}

function place_cubes(cubes, rows, images) {
    positions = Object.keys(cubes);
    for (var i=0; i<positions.length; i++ ) {
        var cube_set = cubes[positions[i]];
        for (var color=0; color<cube_set.length; color++) {
            if (cube_set[color] !== 0) {
                var city = document.getElementById(positions[i]);
                var dims = city.getBoundingClientRect();
                create_cube_row(positions[i], dims, color, images[color], rows[positions[i]][color], cube_set[color]);
            }
        }
    }
}

function remove_cubes(city, color, num_cubes, cubes_left) {
    var cubes = $(".city-"+city+".cube-"+color);
    var to_remove = cubes.slice(cubes.length-num_cubes, cubes.length);
    for (var i=0; i<to_remove.length; i++) {
        to_remove[i].remove();
    }    document.getElementById(color+"-cnt").getElementsByTagName('tspan')[0].textContent = String(cubes_left);
}

function medic_with_cure(data, position) {
    if (typeof data.cures !== 'undefined') {
        for (var color=0; color<4; color++) {
            if (data.cures[color] > 0) {
                $(".city-"+position+".cube-"+String(color)).remove();
                document.getElementById(String(color)+"-cnt").getElementsByTagName('tspan')[0].textContent = String(data.cubes_left[color]);
            }
        }
    }
}

function treat(event) {
    var city = event.target.getAttribute('id');
    $.getJSON( $SCRIPT_ROOT + '/_treat_disease').success( function(data) {
        if (typeof data.c !== 'undefined') {
            remove_cubes(city, data.c, data.num_cubes, data.cubes_left);
        } else {
            $(".city-"+city).css("border", "2px solid #FFFFF0");
            $(".city-"+city).css("pointer-events", '');
            $(".city-"+city).off().on('click', function(e) { select_cube_color(e) });

            $(".available").off("click");
            $(".treatable").off("click");
            $(".treatable").attr("class", "treating");
            $(".available").attr("class", "unavailable holding");
            $('html').on( 'click', function( e ) {
                if ($( e.target ).closest($(".treating").length === 0 )) {
                    escape_cube_select( $(".city-"+city), city ) }} );
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) { escape_cube_select( $(".city-"+city), city ) };
            });
        }
    }).error(function(error){console.log(error);});
}

function select_cube_color(event) {
    var cube = event.target.getAttribute('class');
    var class_array = cube.split(' ');
    var city = class_array[0].split('-')[1];
    var color = class_array[1].split('-')[1];

    $.getJSON( $SCRIPT_ROOT + '/_select_color', { color: Number(color) }).success(
        function(data) {
            remove_cubes(city, color, data.num_cubes, data.cubes_left);
            $("."+class_array[0]).css("border", '')
            $("."+class_array[0]).css("fill", '')
            $("."+class_array[0]).off('click');
            $("."+class_array[0]).css('pointer-events', 'none');

        }).error(function(error){console.log(error);});
}
