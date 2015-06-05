function select_airlift(target) {
    var map = Snap.select('#cities');
    target.off().addClass('down').removeClass('giveable takeable trashable');
    buttons_off();
    board_off();
    $('.role').attr('class', 'role choosable').off().on('click', airlift_select_player);
    $('#name').attr('class', 'self-chooseable').off().on('click', airlift_select_self);
    target.off().on('click', escape_airlift );
    $('html').keyup( function( e ) {
        if (e.keyCode === 27) { escape_airlift() };
    });
    map.selectAll('.available').forEach( function(el) {
		el.unavailable();
	});
    map.selectAll('.treatable').forEach( function(el) {
		el.unavailable();
	});

    if (!body.hasClass('menu-push-toleft')) {
        team_toggle();
    } else {
        body.addClass('selecting');
    }
    $('#logger').html('(Airlift) Select a player to move.')
}

function airlift_select_player(event) {
    var map = Snap.select('#cities');
    var target = $(event.target);
    var select = target.parent().parent().index();
    var is_airlift = 0;
    if ( $('.event-card').hasClass('down') || $('#cp-store').hasClass('down') || PHASE >= 4) {
        is_airlift = 1;
    }
    $.getJSON( $SCRIPT_ROOT + '/_select_player', { index: select,
                                                   airlift: is_airlift,
                                                   store: STORE }).success(
        function(data) {
            set_cities(data.available);
            target.attr('class', 'role chosen');
            $('#name').off().attr('class', 'self-unchooseable');
            map.select('#city-'+String(data.position)).selected();
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
            $('#logger').html('(Airlift) Select a destination for the  '+ROLES[data.role].bold()+'.');
        }
    ).error(function(error){console.log(error)});
}

function airlift_select_self(event) {
    var map = Snap.select('#cities');
    var is_airlift = 0;
    if ( $('.event-card').hasClass('down') || $('#cp-store').hasClass('down') || PHASE >= 4) {
        is_airlift = 1;
    }
    $.getJSON( $SCRIPT_ROOT + '/_select_player', { index: 0,
                                                   airlift: is_airlift,
                                                   store: STORE }).success(
        function(data) {
            set_cities(data.available);
            $('.role').off().attr('class', 'role');
            $('#name').attr('class', 'self-chosen');
            map.select('#city-'+String(data.position)).selected();
            $('#name').off().on('click', function(data) {
                escape_airlift()
            });
            $('.down').off().on('click', function(data) {
                escape_airlift();
            });
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) { escape_airlift() };
            });
            $('#logger').html('(Forecast) Select a destination for the  '+ROLES[data.role].bold()+'.');
        }
    ).error(function(error){console.log(error)});
}

function escape_airlift_select() {
    if ($('.down').length !== 0 && TRASHING === 0 ) {
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
        board_on();
    }
}

function escape_airlift() {
    $.getJSON( $SCRIPT_ROOT + '/_select_player', { index: 0, airlift: 0 }).success(
        function(data) {
            $('#logger').html('Cancelled AIRLIFT.')
            if (TRASHING === 0) {
                set_cities(data.available);
                set_treatable(data.position);
                escape_airlift_select();
            } else {
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
                $('html').off();
                $('.down').off().on('click', trash).removeClass('down').addClass('trashable');
                $('.holding-t').off().on('click', trash).removeClass('holding-t').addClass('trashable');
                if ( !body.hasClass('selecting') ) {
                    team_toggle();
                } else {
                    body.removeClass('selecting');
                }
                $('#logger').html($('#logger').html() + ' Select a card to discard.');
            }
        }).error(function(error){console.log(error)});
}
