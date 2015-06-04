function getArt(ytID){
    return "".concat('<img class="album-art img-responsive img-rounded" src="http://img.youtube.com/vi/', ytID, '/0.jpg">');
}

//// BACKBONE.MARIONETTE ////
var App = new Marionette.Application();

App.addRegions({
  queueRegion: '#queue-region'
});

App.on("start", function(){
  console.log("in Start block");

  var listView = new App.ListView({collection:data});
  App.queueRegion.show(listView);
  Backbone.history.start();

});

// ItemView for each of the songs
App.ItemView = Backbone.Marionette.ItemView.extend({
    initialize: function() {
        //For Debugging Purposes:
        //console.log('this.model =',this.model);
        //console.log(this);
    },
    template: '#queue-item-template',
    tagName: 'div',
    className: 'list-group-item metadata',
    modelEvents : {
	"change" : function() { this.render(); }
    }
});

// CompositeView to hold all of the Items.
App.ListView = Backbone.Marionette.CollectionView.extend({
    tagName: 'ul',
    className: 'list-group music-queue',
    template: '#queue-tempate',
    childViewContainer: 'ul',
    childView: App.ItemView,
    modelEvents : {
	"change" : function() { this.render(); }
    }
});


var Song = Backbone.Model.extend();
var Songs = Backbone.Collection.extend({
    model:Song
});


var data = new Songs([]);

//var test = new Song({"songname":"Idioteque","songartist":'Radiohead',"albumarturl":"http://upload.wikimedia.org/wikipedia/en/8/8b/Radiohead.bends.albumart.jpg", "songID":"DNqv3nHyteM"});
//var test2 = new Song({"songname":"GDFR","songartist":'Flo Rida',"albumarturl":"http://upload.wikimedia.org/wikipedia/en/8/8b/Radiohead.bends.albumart.jpg", "songID":"F8Cg572dafQ"});
//data.push(test);
//data.push(test2);
//console.log(test);


// Controllers, etc
var MyController = Marionette.Controller.extend({
    makeHome: function() {
	var listView = new App.ListView({model:song,collection:data});
	App.queueRegion.show(listView);
    }
});


App.controller = new MyController();

// Routers
App.router = new Marionette.AppRouter({
    controller : App.controller,
    appRoutes : {
    default  :  "makeHome",     //  /#
    }
});



App.start();

///////// Youtube Iframe API shizz


// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
var playIndex;
var videoData;




function onYouTubeIframeAPIReady() {
     playIndex = 0;
     player = new YT.Player('player', {
        height: '0',
        width: '0',
        videoId: data.models[playIndex].attributes.songID, //yass
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

function onPlayerReady(event) {
    console.log("player ready");
}

function onPlayerStateChange(event) {
    $(".now-playing-song-name").html(player.getVideoData()['title']);
    $(".song-artist").html(player.getVideoData()['author']);
    var albumart = "".concat('<img class="album-art img-responsive img-rounded" src="http://img.youtube.com/vi/', data.models[playIndex].attributes.songID, '/0.jpg">');
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
    player.loadVideoById(data.models[playIndex].attributes.songID);
};

function prevVideo(){
    playIndex--;
    player.loadVideoById(data.models[playIndex].attributes.songID);
};

$(document).ready(function() {
    vynl.sockets.join();

    vynl.sockets.socket.on('join', function(songs) {
        console.log("joined");
        console.log(songs.songs);
        var i;
        for (i = 0; i < songs.songs.length; i++) {
            data.push(songs.songs[i]);
        }
        if (songs.songs.length > 0) {
        	onYouTubeIframeAPIReady();
        }
    });

    vynl.sockets.socket.on('updateSongs', function(songs) {
        data.reset();
        for (i = 0; i < songs.songs.length; i++) {
            data.push(songs.songs[i]);
        }
    });

    vynl.sockets.socket.on('addSongs', function(songs) {
        console.log(songs);
        data.reset();
        for (i = 0; i < songs.songs.length; i++) {
            data.push(songs.songs[i]);
        }
        if (data.models.length < 2) {
            onYouTubeIframeAPIReady();
        }
    });

    var handleClick = function(e) {
        console.log(e);

        if (e.srcElement.className == "fa fa-thumbs-up" || e.srcElement.className == "fa fa-thumbs-down") {
            id = e.srcElement.dataset.id;
            console.log(e.srcElement.dataset.id);

            vote = e.srcElement.dataset.vote;
            console.log(e.srcElement.dataset.vote);

            vynl.sockets.vote({"songID": id}, parseInt(vote), ipAddress);
        }
    }

    if (document.addEventListener) {
        document.addEventListener('click', handleClick, false);
    } else if (document.attachEvent) {
        document.attachEvent('onClick', handleClick);
    }

    window.onbeforeunload = function(e) {
        console.log("nigga left");
        vynl.sockets.leave();
        return null;
    };
});
