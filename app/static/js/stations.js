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
    var city = $(event.target);
    var to_remove = city.attr("id");
    var position = Number($('.building').attr('id'));
    $.getJSON( $SCRIPT_ROOT + '/_select_station', { id: Number(to_remove),
                                                    position: position}).success(
        function(data) {
            $("#station-"+to_remove).hide().attr('class', 'unbuilt');
            $("#station-"+String(data.station)).show().attr('class', 'built');
            ACTIONS++;
            if (data.discard !== '-1') {
                discard(data.discard);
            }
            set_cities(data.available);
            set_treatable(data.position);
            $('.holding').attr('class', 'pl-card giveable');
            $('.giveable').off().on('click', give_card);
            $('.card.holding').off().on('click', take_card).attr('class', 'card takeable');
            $('.down').attr('class', 'pl-card giveable');
            $('#card-48').off().on('click', select_airlift);
            $('#build-station').attr('class', 'action').prop('disabled', true);
            $("#undo-action").prop('disabled', ACTIONS === 0);
            buttons_on();
            $('html').off();
        }
    ).error(function(error){console.log(error);});
}

function build_station() {
    var position;
    if ( $(this).attr('id') !== 'build-station' ) {
        position = Number($(this).attr('id'));
    }
    $.getJSON( $SCRIPT_ROOT + '/_build_station', { position:  position }).success( function(data) {
        if (data.num_stations < 6) {
            $("#station-"+String(data.station)).show().attr('class', 'built');
            ACTIONS++
            if ( data.discard !== '-1' ) {
                discard(data.discard);
            }
            document.getElementById("research-cnt").getElementsByTagName('tspan')[0].textContent = String(6-data.num_stations-1);
            set_cities(data.available);
            set_treatable(data.position);
            $('.holding').attr('class', 'pl-card giveable');
            $('.giveable').off().on('click', give_card);
            $('.card.holding').off().on('click', take_card).attr('class', 'card takeable');
            $('.down').attr('class', 'pl-card giveable');
            $('#card-48').off().on('click', select_airlift);
            $("#build-station").attr('class', 'action').prop('disabled', true);
            $("#undo-action").prop('disabled', ACTIONS === 0);
            buttons_on();
        } else {
            buttons_off();
            $("#build-station").attr('class', 'action activated');
            $("#"+String(data.station)).off().attr('class', 'building');
            $(".selectable").off().attr('class', 'unavailable');
            $(".available").off().attr('class', 'unavailable marked');
            var ids = $('.built');
            for (var i=0; i<ids.length; i++) {
                var true_id = $(ids[i]).attr('id').split('-')[1];
                $('#'+true_id).off().on('click',
                                         select_station).attr('class',
                                                              'selectable marked');
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

function escape_station_select(available, city) {
    $(".marked").attr("class", "unavailable");
    set_cities(available);
    set_treatable(city);
    buttons_on();
    if ($('.down').length !== 0 ) {
        $('.holding').attr('class', 'pl-card giveable');
        $('.giveable').off().on('click', give_card);
        $('.card.holding').off().on('click', take_card).attr('class', 'card takeable');
        $('.down').attr('class', 'pl-card giveable');
        $('#card-48').off().on('click', select_airlift);
        $('#card-50').off().on('click', select_gg);
    }
    $("#build-station").attr('class', 'action');
    $('html').off()
}
