function select_airlift() {
    $('.giveable').off().attr('class', 'pl-card holding');
    $('.takeable').off().attr('class', 'card marked');
    $(this).off().attr('class', 'pl-card down');
    buttons_off();
    $('.role').attr('class', 'role choosable').off().on('click', airlift_select_player);
    $('#name').attr('class', 'self-chooseable').off().on('click', airlift_select_self);
    $(this).off().on('click', escape_airlift_select );
    $('html').keyup( function( e ) {
        if (e.keyCode === 27) { escape_airlift_select() };
    });
    for (var n=0; n<48; n++) {
        if ( $('#'+String(n)).hasClass('available') ) {
            $('#'+String(n)).off().attr('class',' unavailable marked');
        } else {
            $('#'+String(n)).off().attr('class', 'unavailable');
        }
    }
    if (!body.hasClass('menu-push-toleft')) {
        team_toggle();
    } else {
        body.addClass('selecting');
    }
}

function airlift_select_player(event) {
    var target = $(event.target);
    var select = target.parent().parent().index();
    $.getJSON( $SCRIPT_ROOT + '/_select_player', { index: select }).success(
        function(data) {
            target.attr('class', 'role chosen');
            $('#name').off().attr('class', 'self-unchooseable');
            for (var n=0; n<48; n++) {
                if ( $('#'+String(n)).hasClass('marked') ) {
                    $('#'+String(n)).off().on('click', execute_move).attr('class', 'available marked');
                } else {
                    $('#'+String(n)).off().on('click', execute_move).attr('class', 'available');
                }
            }
            $('#'+String(data.position)).off().attr('class', 'selected');
            buttons_off();
            $('.chosen').off().on('click', function(data) {
                    escape_airlift_player(data.position);
            });
            $('.down').off().on('click', function(data) {
                    escape_airlift_player(data.position);
            });
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) { escape_airlift_player(data.position) };
            });
        }
    ).error(function(error){console.log(error)});
}

function airlift_select_self(event) {
    $.getJSON( $SCRIPT_ROOT + '/_select_player', { index: 0 }).success(
        function(data) {
            $('.role').off().attr('class', 'role');
            $('#name').attr('class', 'self-chosen');
            for (var n=0; n<48; n++) {
                if ( $('#'+String(n)).hasClass('marked') ) {
                    $('#'+String(n)).off().on('click', execute_move).attr('class', 'available marked');
                } else {
                    $('#'+String(n)).off().on('click', execute_move).attr('class', 'available');
                }
            }
            $('#'+String(data.position)).off().attr('class', 'selected');
            $('#name').off().on('click', function(data) {
                escape_airlift_player(data.position)
            });
            $('.down').off().on('click', function(data) {
                escape_airlift_player(data.position);
            });
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) { escape_airlift_player(data.position) };
            });
        }
    ).error(function(error){console.log(error)});
}

function escape_airlift_select() {
    if ($('.down').length !== 0 ) {
        $('.holding').attr('class', 'pl-card giveable');
        $('.giveable').off().on('click', give_card);
        $('.card.holding').off().on('click', take_card).attr('class', 'card takeable');
        $('.down').attr('class', 'pl-card giveable');
        $('#card-48').off().on('click', select_airlift);

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

function escape_airlift_player(position) {
    $.getJSON( $SCRIPT_ROOT + '/_select_player', { index: 0 }).success(
        function() {
            for (var n=0; n<48; n++) {
                if ( $('#'+String(n)).hasClass('marked') ) {
                    $('#'+String(n)).off().on('click', execute_move).attr('class', 'available');
                } else {
                    $('#'+String(n)).off().attr('class', 'unavailable');
                }
            }
            set_treatable(String(position));
            escape_airlift_select();
        }
    ).error(function(error){console.log(error)});
}
