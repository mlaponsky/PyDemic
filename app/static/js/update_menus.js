function update_char_menus() {
    var lists = document.getElementsByClassName('char-select');
    for (var n=0; n<lists.length; n++) {
        for (var m=0; m<lists[n].options.length; m++) {
            lists[n].options[m].disabled = false;
        }
    }
    for (var i=0; i<lists.length; i++) {
        var index = lists[i].selectedIndex;
        if ( (lists[i].value !== "none") && (lists[i].value !== "random") ) {
            for (var j=0; j<lists.length; j++) {
                lists[j].options[index].disabled = (i !== j) ? true : lists[j].options[index].disabled;
            };
        };
    };
}

window.onload = function () {
    var lists = document.getElementsByClassName('char-select');
    for (var i=0; i<lists.length; i++) {
        lists[i].onchange = update_char_menus;
        if (i<3) {
            lists[i].options[1].selected = "selected";
        }
    }
    document.getElementById('difficulty').options[1].selected = "selected";
}
