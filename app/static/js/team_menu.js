/**
 * @author max
 */

var menuRight = document.getElementById( 'team-menu' ),
				teamMenu = document.getElementById( 'team-button' ),
				body = document.body;

			teamMenu.onclick = function() {
				classie.toggle( this, 'active' );
				classie.toggle( body, 'menu-push-toleft' );
				classie.toggle( menuRight, 'menu-open' );
				disableOther( 'team-button' );
			};