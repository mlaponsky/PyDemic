function create_station(loc) {
    var city = document.getElementById(String(loc));
    var dims = city.getBoundingClientRect();

    var station = $('<img/>');
    station.attr('id', 'station-'+String(loc));
    station.attr('class', 'station');
    station.attr('src', '../static/img/research.svg');
    station.width(dims.width/2);
    station.height(dims.height/2);
    var menu_on = 0;
    if ( $('#team-menu').hasClass('menu-open') ) {
        menu_on = 1;
    }
    station.offset({left: dims.left - 0.2*dims.width - left_offset + menu_on*menu_shift,
                    top: dims.top + 0.6*dims.height - top_offset
                    }).css('position', 'absolute');
    station.css('z-index', '800');
    station.css('pointer-events', 'none');
    station.appendTo('#map');
}

function set_stations(rs) {
    for (var i=0; i<rs.length; i++) {
        create_station(rs[i]);
    }
}

function select_station(event) {
    var city = event.target;
    var to_remove = city.getAttribute("id");
    $.getJSON( $SCRIPT_ROOT + '/_select_station', { id: Number(to_remove) }, function(data) {
        $("#station-"+to_remove).remove();
        create_station(data.position);
        ACTIONS++;
        if (data.discard) {
            $("#card-"+String(data.position)).remove()
        }
        set_cities(data.available, data.position);
        set_treatable(data.posittion);
        $('#build-station').attr('class', 'action');
        $("#build-station").prop('disabled', true);
        $("#undo-action").prop('disabled', ACTIONS === 0);
    })
}

function build_station() {
    $("#build-station").attr('class', 'action activated');
    $.getJSON( $SCRIPT_ROOT + '/_build_station').success( function(data) {
        if (data.num_stations < 6) {
            create_station(data.position);
            ACTIONS++
            if ( data.discard ) {
                $("#card-"+String(data.position)).remove();
            }
            document.getElementById("research-cnt").getElementsByTagName('tspan')[0].textContent = String(6-data.num_stations-1);
            set_cities(data.available, data.position);
            set_treatable(data.position);
            $("#build-station").attr('class', 'action');
            $("#build-station").prop('disabled', true);
            $("#undo-action").prop('disabled', ACTIONS === 0);
        } else {
            $("#"+String(data.position)).attr('class', 'building');
            $("#"+String(data.position)).off();
            $(".available").off();
            $(".available").attr('class', 'unavailable holding');
            var ids = $('.station');
            for (var i=0; i<ids.length; i++) {
                true_id = ids[i].getAttribute('id').split('-')[1];
                $('#'+true_id).attr('class', 'selectable holding');
                $('#'+true_id).off().on('click', select_station);
            }
            $('html').on( 'click', function( e ) {
                if ($( e.target ).closest($("#build-station").length === 0 )) {
                    escape_station_select( data.available, data.position ) }} );
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) { escape_station_select( data.available, data.position ) };
            });
        }
    }).error(function(error){console.log(error);});
}
