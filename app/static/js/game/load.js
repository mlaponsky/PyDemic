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
var COLOR_CODES = ["#75a4ff", "#BCAC68", "#3d3d3d", "#ff6666"]
var TRASHING = 0;
var ACTIONS = 0;
var EPIDEMIC = 0;
var PHASE = 0;
var STORE = 0;
var ACTIVE;
var COUNTER = 0;
var OQN = false;

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

        $('#stage-name').hide();
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
        init_cubes(cubes, rows, data.at_risk);
        set_cities(available);
        set_treatable(positions[0])
        set_selectable_players(roles[0]);
        $('#cp-store').hide();
        if (data.store !== null) {
            STORE = 1;
            $('#cp-store').attr('src', 'static/img/player_cards/pl-'+String(data.store)+'.svg');
            $('#cp-store').attr('class', 'store-'+String(data.store)).show();
        } else if ( ACTIVE === 'cp' ) {
            for (var l=48; l<53; l++) {
                if ( !$('#pl-discard-'+String(l)).hasClass('graveyard') ) {
                    $('#pl-discard-'+String(l)).off().on('click', store_on_cp).addClass('takeable');
                }
            }
        }
        $('#cp-store').off().on('click', select_store).addClass('giveable').css('z-index', 1000);

        for (var i=0; i<cures.length; i++) {
            set_cure(String(i), cures[i]);
        }

        $('#forecast').sortable().disableSelection();
        $('#forecast>li').hide();
        for (var n=data.forecast.length-1; n >= 0; n--) {
            $('#forecast').prepend($('#forecast-'+String(data.forecast[n])));
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
            var city = document.getElementById('city-'+positions[j]);
            var city_dims = city.getBoundingClientRect();
            set_position(player, roles[j], positions[j], city_dims);
            player.css('z-index', 500-j);
            player.css('pointer-events', 'none');
            player.appendTo('#map');
        }
        $('.menu-left li').hide();
        $('#options li').show();
        for ( var i=0; i<data.player_discard.length; i++ ) {
            var card = data.player_discard[i];
            if (card < 53) {
                $('#pl-discard-'+String(card)).show();
            }
        }
        for ( var i=0; i<data.player_grave.length; i++ ) {
            var card = data.player_grave[i];
            $('#pl-discard-'+String(card)).attr('class', 'graveyard').show();
        }
        for ( var i=0; i<data.drawn_epidemics; i++ ) {
            $('#epidemic-'+String(i+1)).show();
            $('#rate-'+String(i)).attr('class', 'off');
        }
        $('#rate-'+String(data.drawn_epidemics)).attr('class', 'on');
        for ( var j=0; j<data.infect_discard.length; j++) {
            var card = data.infect_discard[j];
            $('#infect-discard-'+String(card)).show();
        }
        for ( var j=0; j<data.infect_grave.length; j++) {
            var card = data.infect_grave[j];
            $('#infect-discard-'+String(card)).attr('class', 'graveyard').show();
        }

        for (var p=0; p<=data.phase; p++) {
            $('#actions-'+String(p)).attr('class', 'on');
        }

        $('#outbreak-'+String(data.num_outbreaks)).attr('class', 'on');
        if (PHASE === 4) {
            actions_off();
            events_on();
        }
    }).error(function(error){console.log(error);});
};
