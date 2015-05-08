function select_oqn(target) {
    var select = 0;
    if ( target.hasClass('card') ) {
        select = target.parent().parent().index();
        console.log(select);
    }
    target.addClass('down').removeClass('giveable takeable trashable');
    board_off();
    $.getJSON( $SCRIPT_ROOT + '/_execute_oqn', { index: select,
                                                 trashing: TRASHING }).success(
        function(data) {
            discard('51');
            board_on();
            if (TRASHING === 0) {
                ACTIONS++;
            }
            $('#logger').html('(One Quient Night) You will skip the next Infection Phase.');
            $('#undo-action').prop('disabled', ACTIONS === 0);
        }
    ).error(function(error){console.log(error)});
}
