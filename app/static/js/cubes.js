window.onload = function() {
    $.getJSON($SCRIPT_ROOT + '/_load').success(function(result) {
        var svgObj = document.getElementById("cities");
        var doc = svgObj.contentDocument;
        $.each( result, function(i, field) {
            var a = doc.getElementById(field);
            a.setAttribute("class", "available");
        })
    }).error(function(error){console.log(error);});
}
