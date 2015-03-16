function create_station(loc) {
    var city = document.getElementById(String(loc));
    var dims = city.getBoundingClientRect();

    var station = $('<img/>');
    station.attr('id', 'station-'+String(loc));
    station.attr('class', 'unbuilt');
    station.attr('src', '../static/img/research.svg');
    station.width(dims.width/2);
    station.height(dims.height/2);
    menu_on = 0;
    if ( $('body').hasClass('menu-push-toright') ) {
        menu_on = -1;
    } else if ( $('body').hasClass('menu-push-toleft') ) {
        menu_on = 1;
    }

    station.offset({left: dims.left - 0.2*dims.width - left_offset + menu_on*menu_shift,
                    top: dims.top + 0.6*dims.height - top_offset
                    }).css('position', 'absolute');
    station.css('z-index', '800');
    station.css('pointer-events', 'none');
    station.appendTo('#map');
    station.hide();
}

function set_stations(num_cities, rs) {
    for ( var i=0; i<num_cities; i++) {
        create_station(i);
    }
    for ( var j=0; j<rs.length; j++) {
        $('#station-'+String(rs[j])).show().attr('class', 'built');
    }
}

function select_station(event) {
    var city = event.target;
    var to_remove = city.getAttribute("id");
    $.getJSON( $SCRIPT_ROOT + '/_select_station', { id: Number(to_remove) }, function(data) {
        $("#station-"+to_remove).hide().attr('class', 'unbuilt');
        $("#station-"+String(data.position)).show().attr('class', 'built');
        ACTIONS++;
        if (data.discard) {
            $("#card-"+String(data.position)).hide();
        }
        set_cities(data.available);
        set_treatable(String(data.position));
        $('#build-station').attr('class', 'action').prop('disabled', true);
        $("#undo-action").prop('disabled', ACTIONS === 0);
    })
}

function build_station() {
    $.getJSON( $SCRIPT_ROOT + '/_build_station').success( function(data) {
        if (data.num_stations < 6) {
            $("#station-"+String(data.position)).show().attr('class', 'built');
            ACTIONS++
            if ( data.discard ) {
                $("#card-"+String(data.position)).hide();
            }
            document.getElementById("research-cnt").getElementsByTagName('tspan')[0].textContent = String(6-data.num_stations-1);
            set_cities(data.available);
            set_treatable(data.position);
            $("#build-station").attr('class', 'action').prop('disabled', true);
            $("#undo-action").prop('disabled', ACTIONS === 0);
        } else {
            $('.action').off();
            $("#build-station").attr('class', 'action activated');
            $("#"+String(data.position)).off().attr('class', 'building');
            $(".available").off().attr('class', 'unavailable holding');
            var ids = $('.built');
            for (var i=0; i<ids.length; i++) {
                var true_id = $(ids[i]).attr('id').split('-')[1];
                $('#'+true_id).off().on('click',
                                         select_station).attr('class',
                                                              'selectable holding');
            }
            $('html').off().on('click', function(e) {
                if ( $(e.target).attr('id') !== 'build-station' ||
                     $(e.target).attr('class') !== '.selectable' ) {
                    escape_station_select( data.available, data.position);
                }
            });
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) {
                    escape_station_select( data.available, data.position)
                };
            });
        }
    }).error(function(error){console.log(error);});
}
