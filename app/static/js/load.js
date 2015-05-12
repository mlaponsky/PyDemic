var CARDS = [
    'ATLANTA', 'CHICAGO', 'ESSEN', 'LONDON', 'MADRID', 'MILAN', 'MONTREAL', 'NEW YORK', 'PARIS', 'St. PETERSBURG', 'SAN FRANCISCO', 'WASHINTON',

    'BOGOT\u00C1', 'BUENOS AIRES', 'JOHANNESBURG', 'KHARTOUM', 'KINSHASA', 'LAGOS', 'LIMA', 'LOS ANGELES', 'MEXICO CITY', 'MIAMI', 'SANTIAGO', 'S\u00C3O PAULO',

    'ALGIERS', 'BAGHDAD', 'CAIRO', 'CHENNAI', 'DELHI', 'ISTANBUL', 'KARACHI', 'KOLKATA', 'MOSCOW', 'MUMBAI', 'RIYADH', 'TEHRAN',

    'BANGKOK', 'BEIJING', 'HO CHI MINH CITY', 'HONG KONG', 'JAKARTA', 'MANILA', 'OSAKA', 'SEOUL', 'SHANGHAI', 'SYDNEY', 'TAIPEI', 'TOKYO',

    'AIRLIFT', 'FORECAST', 'GOVERNMENT GRANT', 'ONE QUIET NIGHT', 'RESILIENT POPULATION', 'EPIDEMIC'
];

var ROLES = { 'cp': "CONTINGENCY PLANNER",
              'dispatcher': "DISPATCHER",
              'medic': "MEDIC",
              'oe': "OPERATIONS EXPERT",
              'qs': "QUARANTINE SPECIALST",
              'researcher': "RESEARCHER",
              'scientist': "SCIENTIST" };

var COLORS = ['BLUE', 'YELLOW', 'BLACK', 'RED', 'EVENT'];
var TRASHING = 0;
var ACTIONS = 0;
var PHASE = 0;
var STORE = 0;
var ACTIVE;

function initial_load() {
    $.getJSON($SCRIPT_ROOT + '/_load').success(function(data) {
        var available = data.available;
        var pieces = data.pieces;
        var roles = data.roles;
        var positions = data.positions;
        var cubes = data.cubes;
        var rows = data.cube_rows
        var cures = data.cures
        var rs = data.rs
        var can_build = data.can_build;
        var can_cure = data.can_cure;
        var hand = data.hand;
        var actions = data.actions;
        ACTIONS = actions.length;
        PHASE = data.phase;
        ACTIVE = roles[0];

        set_stations(48, rs);
        for (var k=0; k<53; k++ ) {
            $("#card-"+String(k)).children('div').css('background', "url(static/img/player_cards/pl-"+String(k)+".svg) no-repeat center center");
            $("#card-"+String(k)).children('div').css('background-size', 'contain');
            $("#card-"+String(k)).attr('class', 'pl-card')
            $("#card-"+String(k)).hide();
        }

        set_giveable(data.hand, data.can_give);
        set_takeable(data.team_hands, data.can_take);
        $(".players li:first").hide();
        init_cubes(cubes, rows);
        init_cities();
        set_cities(available);
        set_treatable(positions[0])
        set_selectable_players(roles[0]);
        $('#cp-store').hide();
        if ( ACTIVE === 'cp' ) {
            for (var l=48; l<53; l++) {
                if ( !$('#pl-discard-'+String(l)).hasClass('graveyard') ) {
                    $('#pl-discard-'+String(l)).off().on('click', store_on_cp).addClass('takeable');
                }
            }
            if (data.store !== null) {
                STORE = 1;
                $('#cp-store').attr('src', 'static/img/player_cards/pl-'+String(data.store)+'.svg');
                $('#cp-store').attr('class', 'store-'+String(data.store)).show();
            }
            $('#cp-store').off().on('click', select_store).addClass('giveable').css('z-index', 1000);
        }

        for (var i=0; i<cures.length; i++) {
            set_cure(String(i), cures[i]);
        }

        $('#forecast').sortable().disableSelection();
        for (var n=0; n<data.forecast.length; n++) {
            $('#forecast-'+String(data.forecast[n])).show();
        }

        $('.pl-name').css('background', "url("+data.role_img+") no-repeat center center");

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
            set_position(player, roles[j], positions[j], city_dims);
            player.css('z-index', 500-j);
            player.css('pointer-events', 'none');
            player.appendTo('#map');
        }
        $('.menu-left li').hide();
        for ( var i=0; i<data.player_discard.length; i++ ) {
            var card = data.player_discard[i];
            $('#pl-discard-'+String(card)).show();
        }
        for ( var i=0; i<data.player_grave.length; i++ ) {
            var card = data.player_grave[i];
            $('#pl-discard-'+String(card)).attr('class', 'graveyard').show();
        }
        for ( var j=0; j<data.infect_discard.length; j++) {
            var card = data.infect_discard[j];
            $('#infect-discard-'+String(card)).show();
        }
        for ( var j=0; j<data.infect_grave.length; j++) {
            var card = data.infect_grave[j];
            $('#infect-discard-'+String(card)).attr('class', 'graveyard').show();
        }

    }).error(function(error){console.log(error);});
};
