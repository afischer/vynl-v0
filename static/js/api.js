var vynl = {
};

vynl.api = (function() {
	var endpoint = "/api/";
	
	var addSong = function(song, callback) {
		$.ajax({
			type: "POST",
			url: endpoint + window.location.pathname,
			contentType: "application/json",
			dataType: "json",
			data: song,
			success: callback(data),
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
			data: song,
			success: callback(data)
		});
	};

	var updateSong = function(song, callback) {
		$.ajax({
			type: "PATCH",
			url: endpoint + window.location.pathname,
			contentType: "application/json",
			dataType: "json",
			data: song,
			success: callback(data)
		});
	};

	var getSongs = function(song, callback) {
		$.ajax({
			type: "GET",
			url: endpoint + window.location.pathname,
			contentType: "application/json",
			dataType: "json",
			data: song,
			success: callback(data)
		});
	};
}());
