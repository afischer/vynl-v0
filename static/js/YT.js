///////// Youtube Iframe API shizz


// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
var playlist = [];
var playIndex;
var videoData;

// For demo purposes:
playlist.push("DNqv3nHyteM");
playlist.push("OPf0YbXqDm0");
playlist.push("onRk0sjSgFU");



function onYouTubeIframeAPIReady() {
     playIndex = 0;
     player = new YT.Player('player', {
        height: '0',
        width: '0',
        videoId: playlist[playIndex], //yass
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

function onPlayerReady(event) {
    // $(".song-name").html(player.getVideoData()['title']);
    // $(".song-artist").html(player.getVideoData()['author']);
    // $("div.album-art").html("".concat('<img class="img-rounded" src="img.youtube.com/vi/', playlist[playIndex], '/0.jpg"'));
}

function onPlayerStateChange(event) {
    $(".song-name").html(player.getVideoData()['title']);
    $(".song-artist").html(player.getVideoData()['author']);
    // $("#AA").html("".concat('<img class="img-rounded" src="http://img.youtube.com/vi/', playlist[playIndex], '/0.jpg"'));
    var albumart = "".concat('<img class="album-art img-responsive img-rounded" src="http://img.youtube.com/vi/', playlist[playIndex], '/0.jpg">');
    console.log(albumart)
     $(".album-art").html(albumart);


    if (event.data == YT.PlayerState.ENDED){
        nextVideo();
    }
};

function playVideo() {
    player.playVideo();
    $('.play').removeClass("glyphicon-play").addClass("glyphicon-pause");
    $('.play').attr("onclick", "pauseVideo()");
};

function pauseVideo() {
    player.pauseVideo();
    $('.play').removeClass("glyphicon-pause").addClass("glyphicon-play");
    $('.play').attr("onclick", "playVideo()");
};

function nextVideo(){
    playIndex++;
    player.loadVideoById(playlist[playIndex]);
};

function prevVideo(){
    playIndex--;
    player.loadVideoById(playlist[playIndex]);
};


//search
document.getElementById("search_input").addEventListener( "keydown", function( e ) {
    var keyCode = e.keyCode || e.which;
    if ( keyCode === 13 ) {
       playlist.push(this.value);
       console.log("added " + this.value + " to playlist.");
    }
}, false);
