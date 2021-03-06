var team_menu = $( '#team-menu' ),
	team_button = $( '#team-button' ),
	infect_menu = $( '#infect-menu' ),
	infect_button = $( '#infect-button' ),
	player_menu = $( '#player-menu' ),
	player_button = $( '#player-button' ),
	options_menu = $('#options-menu' ),
	options_button = $('#options-button')
	body = $( 'body' );

function team_toggle() {
	team_button.toggleClass( 'active' );
	body.toggleClass( 'menu-push-toleft' );
	if ( infect_button.attr('class') === 'active' ) {
		infect_button.toggleClass( 'active' );
		infect_menu.toggleClass( 'menu-open' );
		body.toggleClass( 'menu-push-toright' );
	} else if (player_button.attr('class') === 'active') {
		player_button.toggleClass( 'active' );
		player_menu.toggleClass( 'menu-open' );
		body.toggleClass( 'menu-push-toright' );
	} else if (options_button.attr('class') === 'active') {
		options_button.toggleClass( 'active' );
		options_menu.toggleClass( 'menu-open' );
		body.toggleClass( 'menu-push-toright' );
	}
	team_menu.toggleClass( 'menu-open' );
	if (body.hasClass('menu-push-toleft')) {
		menu_on = 1;
	} else {
		menu_on = 0;
	}
}

function infect_toggle() {
	infect_button.toggleClass( 'active' );
	if ( player_button.attr('class') === 'active' ) {
		player_button.toggleClass( 'active' );
		player_menu.toggleClass( 'menu-open' ).removeClass('selecting');
	} else if (options_button.attr('class') === 'active') {
		options_button.toggleClass( 'active' );
		options_menu.toggleClass( 'menu-open' );
	} else if (team_button.attr('class') === 'active') {
		team_button.toggleClass( 'active' );
		team_menu.toggleClass( 'menu-open' );
		body.toggleClass( 'menu-push-toleft' );
		body.toggleClass( 'menu-push-toright' );
	} else {
		body.toggleClass( 'menu-push-toright' );
	}
	infect_menu.toggleClass( 'menu-open' );
	if (body.hasClass('menu-push-toright')) {
		menu_on = -1;
	} else {
		menu_on = 0;
	}
}

function player_toggle() {
	player_button.toggleClass( 'active' );
	if ( team_button.attr('class') === 'active' ) {
		team_button.toggleClass( 'active' );
		team_menu.toggleClass( 'menu-open' );
		body.toggleClass( 'menu-push-toleft' );
		body.toggleClass( 'menu-push-toright' );
	} else if (infect_button.attr('class') === 'active') {
		infect_button.toggleClass( 'active' );
		infect_menu.toggleClass( 'menu-open' );
	} else if (options_button.attr('class') === 'active') {
		options_button.toggleClass( 'active' );
		options_menu.toggleClass( 'menu-open' );
	} else {
		body.toggleClass( 'menu-push-toright' );
	}
	player_menu.toggleClass( 'menu-open' );
	if (body.hasClass('menu-push-toright')) {
		menu_on = -1;
	} else {
		menu_on = 0;
	}
}

function options_toggle() {
	options_button.toggleClass( 'active' );
	if ( team_button.attr('class') === 'active' ) {
		team_button.toggleClass( 'active' );
		team_menu.toggleClass( 'menu-open' );
		body.toggleClass( 'menu-push-toleft' );
		body.toggleClass( 'menu-push-toright' );
	} else if (infect_button.attr('class') === 'active') {
		infect_button.toggleClass( 'active' );
		infect_menu.toggleClass( 'menu-open' );
	} else if (player_button.attr('class') === 'active') {
		player_button.toggleClass( 'active' );
		player_menu.toggleClass( 'menu-open' );
	} else {
		body.toggleClass( 'menu-push-toright' );
	}
	options_menu.toggleClass( 'menu-open' );
	if (body.hasClass('menu-push-toright')) {
		menu_on = -1;
	} else {
		menu_on = 0;
	}
}

	team_button.on('click', function() {
		team_toggle();
	});

	infect_button.on( 'click', function() {
		infect_toggle();
	});

	player_button.on( 'click', function() {
		player_toggle();
	});

	options_button.on( 'click', function() {
		options_toggle();
	});
