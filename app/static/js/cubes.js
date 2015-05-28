function set_cube_dimensions(cube, dims, row, num) {
    var menu_on = 0;
    if ( $('body').hasClass('menu-push-toright') ) {
        menu_on = -1;
    } else if ( $('body').hasClass('menu-push-toleft') ) {
        menu_on = 1;
    }
    cube.width(0)
    cube.stop().animate( {width: dims.width/2.2}, 300 );
    cube_l = dims.left + dims.width/3 + (num)*dims.width/2.4 - left_offset + menu_on*menu_shift;
    cube_t = dims.top + (row+1)*dims.height/2.2 - top_offset;
    cube.offset({ left: cube_l, top: cube_t }).css('position', 'absolute');
    cube.css('z-index', 900);
    cube.css('pointer-events', 'none');
}

function create_cube(position, dims, color, row, num) {
    var cube = $('<img/>');
    var class_name = "city-"+position + " " + "cube-"+color + " " + "row-"+String(row);
    cube.attr("class", class_name);
    cube.attr("src", "static/img/cubes/cube-"+String(color)+".svg");
    set_cube_dimensions(cube, dims, row, num);
    cube.appendTo('#map');
}

function set_cube_position(position, dims, color, row, num) {
    var class_name = ".city-"+position+".cube-"+color+".row-"+String(row);
    var cube = $(class_name);
    set_cube_dimensions(cube, dims, row, num);
}

function create_cube_row(position, dims, color, row, total) {
    for (var num=0; num<total; num++) {
        create_cube(position, dims, String(color), row, num);
    }
}

function set_cube_row(position, dims, color, row, total) {
    for (var num=0; num<total; num++) {
        set_cube_position(position, dims, String(color), row, num);
    }
}

function add_cubes(position, dims, color, row, added, at_risk) {
    if (added > 0) {
        var class_name = ".city-"+position+".cube-"+color+".row-"+String(row);
        var cubes = $(class_name);
        var orig_cubes = cubes.length;
        for (var i=orig_cubes; i<orig_cubes+added; i++) {
            create_cube(position, dims, color, row, i);
        }
        var cubes_left = document.getElementById(color+"-cnt").getElementsByTagName('tspan')[0].textContent;
        document.getElementById(color+"-cnt").getElementsByTagName('tspan')[0].textContent = cubes_left - added;
        flash_svg(position, true);
        for (var i=0; i<at_risk.length; i++) {
            pulse_svg(at_risk[i]);
        }
    }
};

function init_cubes(cubes, rows, at_risk) {
    var positions = Object.keys(cubes);
    for (var i=0; i<positions.length; i++ ) {
        var cube_set = cubes[positions[i]];
        if ( at_risk.indexOf(Number(positions[i])) !== -1 ) {
            pulse_svg(positions[i]);
        }
        for (var color=0; color<cube_set.length; color++) {
            if (cube_set[color] !== 0) {
                var city = document.getElementById('city-'+positions[i]);
                var dims = city.getBoundingClientRect();
                create_cube_row(positions[i], dims, color, rows[positions[i]][color], cube_set[color]);
            }
        }
    }
}

function set_cubes(cubes, rows) {
    positions = Object.keys(cubes);
    for (var i=0; i<positions.length; i++ ) {
        var cube_set = cubes[positions[i]];
        for (var color=0; color<cube_set.length; color++) {
            if (cube_set[color] !== 0) {
                var city = document.getElementById('city-'+positions[i]);
                var dims = city.getBoundingClientRect();
                set_cube_row(positions[i], dims, color, rows[positions[i]][color], cube_set[color]);
            }
        }
    }
}

function remove_cubes(city, color, num_cubes, cubes_left, at_risk) {
    var map = Snap.select('#cities');
    var cubes = $(".city-"+city+".cube-"+color);
    var to_remove = cubes.slice(cubes.length-num_cubes, cubes.length);
    for (var i=0; i<to_remove.length; i++) {
        $(to_remove[i]).hide(200, function() { this.remove();
                                               if (PHASE < 4) {
                                                   set_treatable(city);
                                            }});
    }
    document.getElementById(color+"-cnt").getElementsByTagName('tspan')[0].textContent = String(cubes_left);
    if ( $.inArray(Number(city), at_risk) === -1 ) {
        stop_svg(city);
    }
    $('#logger').html('Removed '+String(num_cubes)+' '+COLORS[color].bold()+' cube(s) from '+CARDS[Number(city)].bold()+' ('+String(cubes.length-num_cubes)+' remaining).');
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
    var map = Snap.select('#cities');
    var city = $(event.target).attr('id').split('-')[1];
    $.getJSON( $SCRIPT_ROOT + '/_treat_disease').success( function(data) {
        if (typeof data.c !== 'undefined') {
            PHASE = data.phase;
            $('#actions-'+String(PHASE)).attr('class', 'on');
            remove_cubes(city, data.c, data.num_cubes, data.cubes_left, data.at_risk);
            ACTIONS++;
            if (PHASE >= 4) {
                actions_off();
            }
            $("#undo-action").prop('disabled', ACTIONS === 0);
        } else {
            $(".city-"+city).css("border", "2px solid #FFFFF0");
            $(".city-"+city).css('-webkit-border-radius', 4);
            $(".city-"+city).css('-moz-border-radius', 4);
            $(".city-"+city).css('border-radius', 4);
            $(".city-"+city).css("pointer-events", '');
            $(".city-"+city).off().on('click', function(e) { select_cube_color(e) });
            map.selectAll(".available").forEach( function(el) {
        		el.unavailable();
                el.addClass('marked');
        	});
            map.selectAll(".treatable").forEach( function(el) {
        		el.treating();
        	});
            board_off();
            $('#logger').html('(TREATING) Choose a disease color to treat.');
            $('html').on( 'click', function( e ) {
                if ( $(e.target).attr('class') === 'treating' ) {
                    escape_cube_select( $(".city-"+city), city )
                }
            });
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) {
                    escape_cube_select( $(".city-"+city), city )
                };
            });
        }
    }).error(function(error){console.log(error);});
}

function select_cube_color(event) {
    var cube = $(event.target).attr('class');
    var class_array = cube.split(' ');
    var city = class_array[0].split('-')[1];
    var color = class_array[1].split('-')[1];

    $.getJSON( $SCRIPT_ROOT + '/_select_color', { color: Number(color) }).success(
        function(data) {
            PHASE = data.phase;
            $('#actions-'+String(PHASE)).attr('class', 'on');
            remove_cubes(city, color, data.num_cubes, data.cubes_left);
            board_on();
            $('.marked').off().on('click', execute_move).attr('class', 'available');
            ACTIONS++;
            $("#undo-action").prop('disabled', ACTIONS === 0);
            $("."+class_array[0]).css("border", '')
            $("."+class_array[0]).css("fill", '')
            $("."+class_array[0]).off();
            $("."+class_array[0]).css('pointer-events', 'none');
            if (PHASE === 4) {
                actions_off();
            }
        }).error(function(error){console.log(error);});
}

function escape_cube_select(objects, city) {
    var map = Snap.select('#cities');
    map.selectAll(".marked").forEach( function(el) {
		el.available();
	});;
    map.selectAll(".selected").forEach( function(el) {
		el.available();
	});
    set_treatable(city);
    objects.css("border", '');
    objects.off();
    objects.css("pointer-events", "none");
    buttons_on();
    $('html').off();
}
