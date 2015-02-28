function updateMenus() {
    var lists = document.getElementsByClassName('char-select');
    for (var i=0; i<lists.length; i++) {
        var index = lists[i].selectedIndex;
        if ( (lists[i].value != "none") && (lists[i].value != "random") ) {
            for (var j=0; j<lists.length; j++) {
                lists[j].options[index].disabled = (lists[j] != lists[i]) ? true : lists[j].options[index].disabled;
            };
        };
    };
}
