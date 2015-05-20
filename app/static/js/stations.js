function create_station(loc) {
    var city = document.getElementById(String(loc));
    var dims = city.getBoundingClientRect();

    var station = $('<img/>');
    station.attr('id', 'station-'+String(loc));
    station.attr('class', 'unbuilt');
    station.attr('src', '../static/img/research.svg');
    station.width(dims.width/2);
    station.height(dims.height/2);
    menu_on = 0;
    if ( $('body').hasClass('menu-push-toright') ) {
        menu_on = -1;
    } else if ( $('body').hasClass('menu-push-toleft') ) {
        menu_on = 1;
    }

    station.offset({left: dims.left - 0.2*dims.width - left_offset + menu_on*menu_shift,
                    top: dims.top + 0.6*dims.height - top_offset
                    }).css('position', 'absolute');
    station.css('z-index', '800');
    station.css('pointer-events', 'none');
    station.appendTo('#map');
    station.hide();
}

function set_stations(num_cities, rs) {
    for ( var i=0; i<num_cities; i++) {
        create_station(i);
    }
    for ( var j=0; j<rs.length; j++) {
        $('#station-'+String(rs[j])).show().attr('class', 'built');
    }
}

function select_station(event) {
    var city = $(event.target);
    var to_remove = city.attr("id");
    var position = Number($('.building').attr('id'));
    var select = 0;
    var is_gg = 0;
    if ( $('.event-card.down').length !== 0 ) {
        select  = $('.down').parent().parent().index();
        is_gg = 1;
    } else if ( $('#cp-store').hasClass('down') ) {
        is_gg = 1;
    }
    $.getJSON( $SCRIPT_ROOT + '/_select_station', { id: Number(to_remove),
                                                    position: position,
                                                    index: select,
                                                    trashing: TRASHING,
                                                    is_gg: is_gg,
                                                    is_stored: is_stored }).success(
        function(data) {
            $("#station-"+to_remove).hide(200).attr('class', 'unbuilt');
            $("#station-"+String(data.station)).show(200).attr('class', 'built');
            $('#logger').html('Built a station in '+CARDS[data.station].bold()+'. Removed station from '+CARDS[Number(to_remove)]+'.');
            if (TRASHING === 0) {
                ACTIONS++;
                PHASE++;
            }
            if ( data.discard === 50 ) {
                if ( !$('#cp-store').hasClass('down') ) {
                    $('.down').off().on('click', select_gg);
                } else {
                    $('#cp-store').hide(200);
                    $('#pl-discard-50').off().show(200).attr('class', 'graveyard');
                    STORE = 0;
                }
                PHASE--;
            } else {
                discard(String(data.discard));
            }
            $('.holding.down').removeClass('down').hide(200);
            board_on();
            set_cities(data.available);
            set_treatable(data.position);
            if ( data.can_build && data.station !== data.position ) {
                $("#build-station").attr('class', 'action').prop('disabled', false);
            } else {
                $("#build-station").attr('class', 'action').prop('disabled', true);
            }
            $("#undo-action").prop('disabled', ACTIONS === 0);
            buttons_on();
            $('html').off();
            if ( data.num_cards <= 7) {
                TRASHING = 0;
                if (data.phase === 8 || data.phase === 9) {
                    infect_phase();
                }
            } else {
                set_active_trash();
            }
        }
    ).error(function(error){console.log(error);});
}

function build_station() {
    var position;
    var select;
    if ( $(this).attr('id') !== 'build-station' ) {
        position = Number($(this).attr('id'));
    }
    if ( $('.card.down').length !== 0 ) {
        select  = $('.down').parent().parent().index();
    }

    $.getJSON( $SCRIPT_ROOT + '/_build_station', { position:  position,
                                                   index: select,
                                                   trashing: TRASHING}).success(
    function(data) {
        if (data.num_stations < 6) {
            $("#station-"+String(data.station)).show(200).attr('class', 'built');
            $('#logger').html('Built a station in '+CARDS[data.station].bold()+'.');
            if (TRASHING === 0) {
                ACTIONS++;
                PHASE++;
            }
            if ( data.discard === '50' ) {
                if ( !$('#cp-store').hasClass('down') ) {
                    $('.down').off().on('click', select_gg);
                } else {
                    $('#cp-store').hide(200);
                    $('#pl-discard-50').off().show(200).attr('class', 'graveyard');
                    STORE = 0;
                }
                PHASE--;
            } else {
                discard(data.discard);
            }
            document.getElementById("research-cnt").getElementsByTagName('tspan')[0].textContent = String(6-data.num_stations-1);
            set_cities(data.available);
            set_treatable(data.position);
            $('.holding.down').removeClass('down').hide(200);
            board_on();
            if ( data.can_build && data.station !== data.position ) {
                $("#build-station").attr('class', 'action').prop('disabled', false);
            } else {
                $("#build-station").attr('class', 'action').prop('disabled', true);
            }
            $("#undo-action").prop('disabled', ACTIONS === 0);
            buttons_on();
            $('html').off();
            if ( data.num_cards <= 7 ) {
                TRASHING = 0;
                if (data.phase === 8 || data.phase === 9) {
                    infect_phase();
                }
            } else {
                set_active_trash();
            }
        } else {
            buttons_off();
            $("#build-station").attr('class', 'action activated');
            $("#"+String(data.station)).off().attr('class', 'building');
            $(".selectable").off().attr('class', 'unavailable');
            $(".available").off().attr('class', 'unavailable marked');
            var ids = $('.built');
            for (var i=0; i<ids.length; i++) {
                var true_id = $(ids[i]).attr('id').split('-')[1];
                $('#'+true_id).off().on('click',
                                         select_station).attr('class',
                                                              'selectable marked');
            }
            $('#logger').html('There are already 6 stations. Either cancel action or select a station to remove.');
            $('html').off().on('click', function(e) {
                if ( $(e.target).attr('id') === 'build-station' ) {
                    escape_station_select( data.available, data.position);
                }
            });
            $('html').keyup( function( e ) {
                if (e.keyCode === 27) {
                    escape_station_select( data.available, data.position)
                };
            });
        }
    }).error(function(error){console.log(error);});
}

function escape_station_select(available, city) {
    $(".marked").attr("class", "unavailable");
    set_cities(available);
    set_treatable(city);
    buttons_on();
    if ($('.down').length !== 0 ) {
        $('.pl-card.down').removeClass('down').addClass('giveable');
        $('.card.down').removeClass('down').addClass('takeable');
        $('.pl-card.holding').removeClass('holding').addClass('giveable');
        $('.giveable').off().on('click', give_card);
        $('.card.holding').removeClass('holding').addClass('takeable');
        $('.takeable').off().on('click', take_card);
    }
    $("#build-station").attr('class', 'action');
    $('html').off()
    $('#logger').html('Cancelled station construction.')
}
