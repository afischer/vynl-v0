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
