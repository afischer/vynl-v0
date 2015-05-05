var search = function(query, key) {
    $.ajax({
        url : 'http://tinysong.com/s/' + query + '?format=json&key='+key,
        type : 'get',
        dataType : 'json',
        success : function(response){
            console.log(response);
        },
        error: function(error){
            console.warn('ERROR');
            console.warn(error);
        }
    });
}

    function doSearch(e)
    {
        results = [];

        if (e != "")
        {
            $.each(searchJSON, function(t, n) {
                var r = n.title, i = n.title, s = n.artist, o=n.album && results.push([r, s, o])
            });

            printResults();
        }
        else
        {
            $("#search_results").html();
            results = [];
            printResults();
        }
    }

    function printResults()
    {
        var e = $("#search_results");

        e.html("");

        e.html(function() {
            if (results.length == 0)
            {
                e.append('<li style="padding-top: 3px; padding-bottom: 3px"><a style="color: #999; word-wrap: break-word; white-space: normal" href="#">No results found</a></li>');
            }
            else
            {
                $.each(results, function(t, n) {
                    e.append('<li style="padding-top: 3px; padding-bottom: 3px"><a style="color: #999; word-wrap: break-word; white-space: normal" href="' + n[1] + '">' + n[0] + '</a></li>');
                });
            }
        });
    }

    // Show the dropdown menu as long as there are characters in the text field
    function checkTextField()
    {
        // If the value of id search_input is not empty show id search_results otherwise hide it
        if ($('#search_input').val() != '')
        {
            $('#search_results').show();
        }
        else
        {
            $('#search_results').hide();
        }
    }

    // Hide the dropdown menu if there is a left mouse click outside of it
    $(document).mouseup(function (e)
    {
        var container = $("#search_results");

        // if the target of the click isn't the
        // container nor a descendant of the container
        if (!container.is(e.target) && container.has(e.target).length === 0)
        {
            container.hide();
        }
    });

    $(document).ready(function() {

        // Continually update search results as characters are typed
        $("#search_input").keyup(function() {
            // Make search inputs are case insensitive
            var e = $(this).val().toLowerCase();

            // Do the actual search
            doSearch(e);
        });
    });



// SVG ANIM

var w = $(window).width(),
    h = $(window).height();

$(function() {

    animateLine = function(canvas, DivName, colorNumber, pathString) {
        $('#' + DivName).hover(

        function() {
            var line = canvas.path(pathString).attr({
                stroke: colorNumber,
                // width:"10%",
                // height:"10%",
                // preserveAspectRatio:"x200Y200 meet",
            });
            var length = line.getTotalLength();

            $('path[fill*="none"]').animate({
                'to': 1
            }, {
                duration: 3000,
                step: function(pos, fx) {
                    var offset = length * fx.pos;
                    var subpath = line.getSubpath(0, offset);
                    canvas.clear();
                    canvas.path(subpath).attr({
                        'stroke-width': 30,
                        stroke: colorNumber,
                        name: "svgLogo"
                    });

                },
            });
        });
    };

    var canvas = Raphael('svg-canvas', w, h);
    var pathString = "m 143.32746,66.817649 c 0.62624,62.638961 0.53055,126.276801 15.46506,187.468461 7.38969,21.55331 22.35489,-16.55205 28.26232,-24.44185 30.34844,-54.10627 53.94709,-112.49891 90.01863,-163.093984 -20.01651,42.208284 -45.41319,82.107184 -61.01499,126.336474 -7.08661,30.24276 32.30111,61.02393 58.83819,43.10937 19.53824,-22.49063 20.78664,-54.46063 30.01612,-81.78952 8.20148,-27.2598 -1.18085,16.69229 -3.01143,25.21441 -2.50601,23.40081 -16.07736,49.05502 -3.84759,71.56531 15.64581,15.0452 44.79895,-0.0794 51.83645,-17.83649 11.08976,-26.76118 14.49679,-55.77498 20.63915,-83.86329 -8.59237,63.0825 -11.46484,127.69676 -28.49804,189.46039 -4.53675,19.08721 -19.79411,55.36485 -44.46456,37.64723 -15.98836,-13.92003 -6.14509,-37.90902 6.91302,-50.21653 42.8869,-44.22453 102.78583,-75.55552 126.47171,-135.61032 5.89805,-10.639 5.5067,-29.78844 9.00449,-37.16406 -3.37429,31.9652 -17.9024,61.82916 -19.70394,93.91665 11.07424,25.44041 27.69784,-20.73703 32.93076,-32.58049 10.20077,-22.09274 21.86167,-44.71576 38.94316,-62.01821 0.081,29.95882 -13.288,60.82906 -4.64264,90.94521 10.69628,26.00878 43.19625,6.5647 57.03063,-6.57724 21.20525,-26.27067 32.54634,-59.00025 48.89601,-88.34294 14.61109,-31.7198 33.67709,-63.474085 35.62142,-99.101731 -4.8302,-34.414639 -37.91965,-10.841928 -49.63985,14.81752 -23.60354,45.124421 -28.00266,97.169831 -31.03406,147.142231 -2.57905,22.31754 15.4446,53.92921 41.10048,40.4448 13.16793,-5.54287 24.87033,-14.11635 35.71247,-23.30186";

    animateLine(canvas, "svg-canvas", "#000", pathString);

    $().ready(function(){
        var svg = document.getElementsByTagName('svg')[0];
        $(svg).attr("preserveAspectRatio","xMinYMin meet");
        $(svg).setAttribute('viewbox','75 10 600 700');
    });

    $(window).resize(function(){
         w = "100%"
         h = "100%"
         canvas.setSize(w,h);
    });

});
