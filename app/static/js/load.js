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
            $("#card-"+String(k)).children('div').attr('class', 'up')
            $("#card-"+String(k)).hide();
        }

        for (var n=0; n<hand.length; n++) {
            $("#card-"+String(hand[n])).show();
            for (var m=1; m<data.roles.length; m++) {
                if ( data.can_give[data.roles[m]][n] ) {
                    set_giveable(String(data.hand[n]));
                }
            }
        }

        $('.card').hide();
        for (var p=1; p<data.team_hands.length; p++) {
            for (var n=0; n<data.team_hands[p].length; n++) {
                $("#"+data.roles[p]+"-card-"+String(data.team_hands[p][n])).show();
                if ( data.can_take[data.roles[p]][n]) {
                    set_takeable(String(data.team_hands[p][n]), data.roles[p]);
                }
            }
        }
        $(".players li:first").hide();

        buttons_on();
        $('#build-station').prop('disabled', !can_build);
        $('#make-cure').prop('disabled', !can_cure);
        $('#undo-action').prop('disabled', (ACTIONS === 0))

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
