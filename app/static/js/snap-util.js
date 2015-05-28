/* Class setting methods extending Snap SVG */
function hover_available() {
	this.attr({strokeWidth: 8});
}

function unhover_available() {
	this.attr({strokeWidth: 2});
}

function hover_treatable() {
	this.attr({fill: '#32CD32',
               strokeWidth: 8});
}

function unhover_treatable() {
    var color = Math.floor( Number(this.attr('id').split('-')[1])/12 );
	this.attr({fill: COLOR_CODES[color],
               strokeWidth: 2});
}

function hover_selectable() {
	this.attr({fill: '#FFFFF0'});
}

function unhover_selectable() {
    var color = Math.floor( Number(this.attr('id').split('-')[1])/12 );
	this.attr({fill: COLOR_CODES[color]});
}



Snap.plugin(function (Snap, Element) {
    Element.prototype.available = function() {
        var color = Math.floor( Number(this.attr('id').split('-')[1])/12 );
        this.attr({class: 'available',
                   fill: COLOR_CODES[color],
                   strokeWidth: 2})
            .unclick()
            .unhover()
            .hover( hover_available, unhover_available )
            .click( execute_move );
    }

    Element.prototype.treatable = function() {
        var color = Math.floor( Number(this.attr('id').split('-')[1])/12 );
        this.attr({class: 'treatable',
                   fill: COLOR_CODES[color],
                   strokeWidth: 2})
            .unclick()
            .unhover()
            .hover( hover_treatable, unhover_treatable )
            .click( treat );
    }

    Element.prototype.selectable = function() {
        var color = Math.floor( Number(this.attr('id').split('-')[1])/12 );
        this.attr({class: 'selectable',
                   fill: COLOR_CODES[color],
                   strokeWidth: 8})
            .unclick()
            .unhover()
            .hover( hover_selectable, unhover_selectable )
            .click( build_station );
    }

    Element.prototype.removable = function() {
        var color = Math.floor( Number(this.attr('id').split('-')[1])/12 );
        this.attr({class: 'selectable',
                   fill: COLOR_CODES[color],
                   strokeWidth: 8})
            .unclick()
            .unhover()
            .hover( hover_selectable, unhover_selectable )
            .click( select_station );
    }

    Element.prototype.unavailable = function() {
        var color = Math.floor( Number(this.attr('id').split('-')[1])/12 );
        this.attr({class: 'available',
                   fill: COLOR_CODES[color],
                   strokeWidth: 2})
            .unclick()
            .unhover()
    }

    Element.prototype.treating = function() {
        this.attr({class: 'available',
                   fill: '#32CD32',
                   strokeWidth: 2})
            .unclick()
            .unhover()
    }

    Element.prototype.selected = function() {
        this.attr({class: 'available',
                   fill: '#FFFFF0',
                   strokeWidth: 2})
            .unclick()
            .unhover()
    }

    Element.prototype.building = function() {
        this.attr({class: 'available',
                   fill: '#FFFFF0',
                   strokeWidth: 2})
            .unclick()
            .unhover()
    }
});
