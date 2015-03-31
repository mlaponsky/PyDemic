function make_cure() {
    $.getJSON( $SCRIPT_ROOT + '/_make_cure').success(
        function(data) {
            if (typeof data.cured !== 'undefined') {
                for ( var i=0; i<data.cards.length; i++ ) {
                    $("#card-"+data.cards[i]).hide();
                }
                set_cure(String(data.c), data.cured);
                console.log($("#medic"))
                if ( $("#medic").length !== 0) {
                    $(".city-"+data.position+".cube-"+String(data.c)).remove();
                    document.getElementById(String(data.c)+"-cnt").getElementsByTagName('tspan')[0].textContent = String(data.cubes_left);
                }
                ACTIONS++;
                $('.available').attr('class', 'unavailable');
                set_cities(data.available);
                $('#make-cure').prop('disabled', true);
                $('#undo-action').prop('disabled', ACTIONS === 0)
            } else {
                $(".action").off();
                $(".pl-card").off()
                for ( var i=0; i<data.cards.length; i++ ) {
                    $("#card-"+data.cards[i]).off().on('click', { needed: data.needed }, select_keepers ).attr('class', 'down');
                }
                $('#make-cure').attr('class', 'action activated');
                $('html').off().on( 'click', function( e ) {
                    if ( $( e.target ).attr('id') === 'make-cure' ||
                        $( e.target ).attr('class') !== 'down' ) {
                        escape_cure_select();
                    }});
                $('html').keyup( function( e ) {
                    if (e.keyCode === 27) { escape_cure_select() };
                });
            }
        }).error(function(error){console.log(error)});
}

function select_keepers(event) {
    $(event.target).attr('class', 'up');
    if ( $('.down').length === event.data.needed ) {
        var cards = [];
        $('.down').each( function(index) {
            cards[index] = $(this).parent().attr('id').split('-')[1];
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
                $('.down').parent().each( function() {
                                            var card = $(this).attr('id').split('-')[1];
                                            discard(card);
                                        })
                set_cure(String(data.c), data.cured);
                if ( (data.role === 'medic') || ($("#medic").length !== 0) ) {
                    $(".city-"+data.position+".cube-"+String(data.c)).remove();
                    document.getElementById(String(data.c)+"-cnt").getElementsByTagName('tspan')[0].textContent = String(data.cubes_left);
                }
                buttons_on();
                $('#make-cure').prop('disabled', true).attr('class', 'action');
                ACTIONS++;
                $('.available').attr('class', 'unavailable');
                set_cities(data.available);
                $('#undo-action').prop('disabled', ACTIONS === 0)
            }

        ).error(function(error){console.log(error)});
    }
}
