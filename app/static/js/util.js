function init_cities() {
    for (var i=0; i<48; i++) {
        $("#"+String(i)).click(execute_move);
        $("#"+String(i)).click(treat);
    }
}
function set_cities(cities, position) {
    for (var i=0; i<cities.length; i++) {
        $("#"+cities[i]).attr("class", "available");
        $("#"+cities[i]).on("click", execute_move);
        $("#"+cities[i]).off("click", treat);
    }
    set_treatable(position);
    $(".unavailable").off('click');
}

function set_treatable(position) {
    if ( $(".city-"+position).length !== 0 ) {
        $("#"+position).attr("class", "treatable");
        $("#"+position).off("click", execute_move);
        $("#"+position).on("click", treat);
    }
}

function escape_card_select(objects) {
    $(".holding").attr("class", "available");
    $(".selected").attr("class", "available");
    $(".available").on("click", execute_move);
    objects.css("border", '');
    objects.off("click");
    $('html').off('click');
    $('html').off('keyup');
}

function escape_cube_select(objects, city) {
    $(".holding").attr("class", "available");
    $(".selected").attr("class", "available");
    $(".available").on("click", execute_move);
    set_treatable(city);
    objects.css("border", '');
    objects.off("click");
    objects.css("pointer-events", "none");
    $('html').off('click');
    $('html').off('keyup');
}

function set_stations(rs) {
    for (var i=0; i<rs.length; i++) {
        var city = document.getElementById(String(rs[i]));
        var dims = city.getBoundingClientRect();

        var station = $('<img/>');
        station.attr('id', 'station-'+String(rs[i]));
        station.attr('src', '../static/img/research.svg');
        station.width(dims.width/2);
        station.height(dims.height/2);
        station.offset({left: dims.left-dims.width/5, top: dims.top + dims.height/10}).css('position', 'absolute');
        station.css('z-index', '800');
        station.css('pointer-events', 'none');
        station.appendTo('#map');
    }
}
