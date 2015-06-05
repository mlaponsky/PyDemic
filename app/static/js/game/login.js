function resume_game() {
    $.ajax( $SCRIPT_ROOT + '/_resume').success(
        function() {
            console.log('Resumed game');
        }
    )
}
