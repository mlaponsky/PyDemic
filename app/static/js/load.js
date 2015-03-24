var CARDS = [
    'ATLANTA', 'CHICAGO', 'ESSEN', 'LONDON', 'MADRID', 'MILAN', 'MONTREAL', 'NEW YORK', 'PARIS', 'St. PETERSBURG', 'SAN FRANCISCO', 'WASHINTON',

    'BOGOT\u00C1', 'BUENOS AIRES', 'JOHANNESBURG', 'KHARTOUM', 'KINSHASA', 'LAGOS', 'LIMA', 'LOS ANGELES', 'MEXICO CITY', 'MIAMI', 'SANTIAGO', 'S\u00C3O PAULO',

    'ALGIERS', 'BAGHDAD', 'CAIRO', 'CHENNAI', 'DELHI', 'ISTANBUL', 'KARACHI', 'KOLKATA', 'MOSCOW', 'MUMBAI', 'RIYADH', 'TEHRAN',

    'BANGKOK', 'BEIJING', 'HO CHI MINH CITY', 'HONG KONG', 'JAKARTA', 'MANILA', 'OSAKA', 'SEOUL', 'SHANGHAI', 'SYDNEY', 'TAIPEI', 'TOKYO',

    'AIRLIFT', 'FORECAST', 'GOVERNMENT GRANT', 'ONE QUIET NIGHT', 'RESILIENT POPULATION', 'EPIDEMIC'
];


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

        init_cubes(cubes, rows, images);
        init_cities();
        set_cities(available);
        set_treatable(positions[0])
        set_stations(48, rs);
        set_selectable_players(roles[0]);

        for (var i=0; i<cures.length; i++) {
            set_cure(String(i), cures[i]);
        }

        $('.pl-name').css('background', "url("+data.role_img+") no-repeat center center");

        for (var k=0; k<data.cards.length; k++ ) {
            $("#card-"+String(k)).children('div').css('background', "url("+data.cards[k]['player_card']+") no-repeat center center");
            $("#card-"+String(k)).children('div').css('background-size', 'contain');
            $("#card-"+String(k)).attr('class', 'pl-card up')
            $("#card-"+String(k)).hide();
        }

        set_giveable(data.hand, data.can_give);
        set_takeable(data.team_hands, data.can_take);

        $(".players li:first").hide();

        buttons_on();
        $('#build-station').prop('disabled', !can_build);
        $('#make-cure').prop('disabled', !can_cure);
        $('#undo-action').prop('disabled', ACTIONS === 0)

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

        $('.menu-left li').hide();

    }).error(function(error){console.log(error);});
};
