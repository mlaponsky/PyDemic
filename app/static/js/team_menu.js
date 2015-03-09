var menu_right = document.getElementById( 'team-menu' ),
				team_menu = document.getElementById( 'team-button' ),
				body = document.body;

			team_menu.onclick = function() {
				classie.toggle( this, 'active' );
				classie.toggle( body, 'menu-push-toleft' );
				classie.toggle( menu_right, 'menu-open' );	
			};
