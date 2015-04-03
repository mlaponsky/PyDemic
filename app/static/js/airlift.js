function select_airlift(target) {
    target.off().addClass('down').removeClass('giveable takeable');
    $('.giveable').off().switchClass('giveable', 'holding');
    $('.takeable').off().switchClass('takeable', 'holding');
    buttons_off();
    $('.role').attr('class', 'role choosable').off().on('click', airlift_select_player);
    $('#name').attr('class', 'self-chooseable').off().on('click', airlift_select_self);
    target.off().on('click', escape_airlift );
    $('html').keyup( function( e ) {
        if (e.keyCode === 27) { escape_airlift() };
    });
    $('.available').off().attr('class', 'unavailable');
    $('.treatable').off().attr('class', 'unavailable');

    if (!body.hasClass('menu-push-toleft')) {
        team_toggle();
    } else {
        body.addClass('selecting');
    }
}

function airlift_select_player(event) {
    var target = $(event.target);
    var select = target.parent().parent().index();
    var is_airlift = 0;
    if ( $('.event-card').hasClass('down') ) {
        is_airlift = 1;
    }
    $.getJSON( $SCRIPT_ROOT + '/_select_player', { index: select,
                                                   airlift: is_airlift }).success(
        function(data) {
            set_cities(data.available);
            target.attr('class', 'role chosen');
            $('#name').off().attr('class', 'self-unchooseable');
            $('#'+String(data.position)).off().attr('class', 'selected');
            buttons_off();
            $('.chosen').off().on('click', function(data) {
                    escape_airlift();
            });
            $('.down').off().on('click', function(data) {
                    escape_airlift();
            });
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) { escape_airlift() };
            });
        }
    ).error(function(error){console.log(error)});
}

function airlift_select_self(event) {
    var is_airlift = 0;
    if ( $('.event-card').hasClass('down') ) {
        is_airlift = 1;
    }
    $.getJSON( $SCRIPT_ROOT + '/_select_player', { index: 0,
                                                   airlift: is_airlift }).success(
        function(data) {
            set_cities(data.available);
            $('.role').off().attr('class', 'role');
            $('#name').attr('class', 'self-chosen');
            if ( $('#'+String(data.position)).attr('class') === 'unavailable marked_t' ) {
                $('#'+String(data.position)).off().attr('class', 'selected marked_t');
            } else {
                $('#'+String(data.position)).off().attr('class', 'selected');
            }
            $('#name').off().on('click', function(data) {
                escape_airlift()
            });
            $('.down').off().on('click', function(data) {
                escape_airlift();
            });
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) { escape_airlift() };
            });
        }
    ).error(function(error){console.log(error)});
}

function escape_airlift_select() {
    if ($('.down').length !== 0 ) {
        escape_cards();

        $('#name').off().attr('class', 'self-unchooseable');
        $('.role').off().attr('class', 'role');
        if ( $('#active-dispatcher').length !== 0 ) {
            $('.role').off().on('click', select_player).attr('class', 'role choosable')
        }
        if ( !body.hasClass('selecting') ) {
            team_toggle();
        } else {
            body.removeClass('selecting');
        }
        buttons_on();
        $('html').off();
    }
}

function escape_airlift() {
    $.getJSON( $SCRIPT_ROOT + '/_select_player', { index: 0, airlift: 0 }).success(
        function(data) {
            set_cities(data.available);
            set_treatable(data.position);
            escape_airlift_select();
        }).error(function(error){console.log(error)});
}
