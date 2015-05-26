var vynl = {
};

vynl.api = (function() {
	var endpoint = "/api";

	var addSong = function(song, callback) {
		$.ajax({
			type: "POST",
			url: endpoint + window.location.pathname,
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: JSON.stringify(song),
			success: callback,
			error: function() {
				console.log("error");
			}
		});
	};

	var deleteSong = function(song, callback) {
		$.ajax({
			type: "DELETE",
			url: endpoint + window.location.pathname,
			contentType: "application/json",
			dataType: "json",
			data: JSON.stringify(song),
			success: callback
		});
	};

	var updateSong = function(song, callback) {
		$.ajax({
			type: "PATCH",
			url: endpoint + window.location.pathname,
			contentType: "application/json",
			dataType: "json",
			data: JSON.stringify(song),
			success: callback
		});
	};

	var getSongs = function(callback) {
		$.ajax({
			type: "GET",
			url: endpoint + window.location.pathname,
			contentType: "application/json",
			dataType: "json",
			success: callback
		});
	};

        return {
            addSong: addSong,
            deleteSong: deleteSong,
            updateSong: updateSong,
            getSongs: getSongs
        };
}());

vynl.sockets = (function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/party');

    var getPartyID = function() {
        var pathname = document.location.pathname;
        var length = pathname.length;
        var room = pathname.slice(length - 8, length);
        return room;
    };

    var join = function() {
        socket.emit('join', {room: getPartyID()});
    };

    var leave = function() {
        socket.emit('leave', {room: getPartyID()});
    };

    var addSong = function(song) {
        room = getPartyID();
        socket.emit('addSong', {room: room, song: song});
    };

    var vote = function(song, vote) {
        if (vote == 1 || vote == -1) {
            room = getPartyID();
            socket.emit('voteSong', {room: room, song: song, vote: vote});
        } else {
            console.error("vote must be -1 or 1");
        };
    };

    socket.on('updateSongs', function(songs) {
        console.log('updatesongs');
        console.log(songs);
    });

    socket.on('addSong', function(song) {
        console.log('addSong');
        console.log(song);
    });

    return {
        socket: socket,
        join: join,
        leave: leave,
        addSong: addSong,
        vote: vote,
        getPartyID: getPartyID
    };
}());
