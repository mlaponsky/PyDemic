function select_oqn(target) {
    var select = 0;
    if ( target.hasClass('card') ) {
        select = target.parent().parent().index();
    }
    target.addClass('down').removeClass('giveable takeable trashable');
    board_off();
    $.getJSON( $SCRIPT_ROOT + '/_execute_oqn', { index: select,
                                                 trashing: TRASHING }).success(
        function(data) {
            if (target.attr('id') !== 'cp-store') {
                discard('51');
            } else {
                $('#cp-store').hide(200);
                $('#pl-discard-51').off().show(200).attr('class', 'graveyard');
                STORE = 0;
            }
            $('.holding.down').removeClass('down').hide(200);
            board_on();
            if (TRASHING === 0) {
                ACTIONS++;
            }
            $('#logger').html('(One Quient Night) You will skip the next Infection Phase.');
            $('#undo-action').prop('disabled', ACTIONS === 0);
            if (data.num_cards <= 7) {
                TRASHING = 0;
                if (data.phase === 4) {
                    infect_phase();
                }
            } else {
                set_active_trash();
            }
        }
    ).error(function(error){console.log(error)});
}
