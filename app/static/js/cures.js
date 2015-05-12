function make_cure() {
    $.getJSON( $SCRIPT_ROOT + '/_make_cure').success(
        function(data) {
            if (typeof data.cured !== 'undefined') {
                $('#logger').html('Made '+COLORS[data.c].bold()+' cure!');
                for ( var i=0; i<data.cards.length; i++ ) {
                    discard(data.cards[i]);
                }
                set_cure(String(data.c), data.cured);
                if ( data.medic !== -1 ) {
                    $(".city-"+data.medic+".cube-"+String(data.c)).remove();
                    document.getElementById(String(data.c)+"-cnt").getElementsByTagName('tspan')[0].textContent = String(data.cubes_left);
                }
                ACTIONS++;
                PHASE++;
                set_cities(data.available);
                set_treatable(data.position);
                $('#make-cure').prop('disabled', true);
                $('#undo-action').prop('disabled', ACTIONS === 0);
            } else {
                buttons_off();
                $('#logger').html('(CURE) Deselect which cards you wish to keep, then click NEXT.');
                board_off();
                $('.available').off().attr('class', 'unavailable marked');
                $('.treatable').off().attr('class', 'unavailable marked-t');
                for ( var i=0; i<data.cards.length; i++ ) {
                    $("#card-"+data.cards[i]).off().on('click', toggle_select ).removeClass('giveable').addClass('down curingo');
                    $("#card-"+data.cards[i]).children('div').off().css('pointer-events', 'none');
                }
                $('#make-cure').attr('class', 'action activated');
                $('html').off().on( 'click', function( e ) {
                    if ( $( e.target ).attr('id') === 'make-cure' ) {
                        escape_cure_select();
                    }});
                $('html').keyup( function( e ) {
                    if (e.keyCode === 27) { escape_cure_select() };
                });
            }
        }).error(function(error){console.log(error)});
}

function toggle_select(event) {
    var active = $('.active-player').attr('id').split('-')[1];
    var needed = 5;
    if (active == 'scientist') {
      needed = 4;
    }
    if ( $(event.target).hasClass('down') ) {
        $(event.target).removeClass('down').addClass('giveable');
    } else {
        $(event.target).removeClass('giveable').addClass('down');
    }
    $('#next-phase').off().on('click', execute_cure).prop('disabled', $('.down').length !== needed);
}

function execute_cure() {
    var cards = [];
    $('.down').each( function(index) {
        cards[index] = $(this).attr('id').split('-')[1];
    })
    var card0 = Number(cards[0]);
    var card1 = Number(cards[1]);
    var card2 = Number(cards[2]);
    var card3 = Number(cards[3]);
    if ( $('.down').length === 5 ) {
        var card4 = Number(cards[4]);
    } else {
        var card5 = -1;
    }
    $.getJSON( $SCRIPT_ROOT + '/_select_cure', { card0: card0,
                                                 card1: card1,
                                                 card2: card2,
                                                 card3: card3,
                                                 card4: card4 } ).success(
        function(data) {
            $('.down').each( function() {
                                        var card = $(this).attr('id').split('-')[1];
                                        discard(card);
                                    })
            $('#logger').html('Made '+COLORS[data.c].bold()+' cure!');
            set_cure(String(data.c), data.cured);
            if ( (data.role === 'medic') || ($("#medic").length !== 0) ) {
                $(".city-"+data.position+".cube-"+String(data.c)).remove();
                document.getElementById(String(data.c)+"-cnt").getElementsByTagName('tspan')[0].textContent = String(data.cubes_left);
            }
            buttons_on();
            $('#make-cure').prop('disabled', true).attr('class', 'action');
            ACTIONS++;
            PHASE++;
            set_cities(data.available);
            set_treatable(data.position);
            $('#undo-action').prop('disabled', ACTIONS === 0);
            $('#next-phase').prop('disabled', true);
            board_on();
        }).error(function(error){console.log(error)});
}


function escape_cure_select() {
    $('.marked').off().on('click', execute_move).attr('class','available');
    $('.marked-t').off().on('click', treat).attr('class','treatable')
    buttons_on();
    $('#make-cure').attr('class', 'action');
    $('#next-phase').prop('disabled', true);
    board_on();
    $('html').off();
}
