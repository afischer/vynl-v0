var typingTimer;
var doneTypingInterval = 250;

function handleClientLoad() {
    gapi.client.setApiKey(apiKey);
    gapi.client.load('youtube', 'v3', function() {});
}

function search(query, callback) {
    var request = gapi.client.youtube.search.list({
        q    : query,
        type : 'video',
        part : 'snippet'
    });
    request.execute(callback);
}

var SearchSongRow = React.createClass({
	handleOnClick: function() {
		var song = new Song({
			"songname"    : this.props.song.snippet.title,
			"songartist"  : this.props.song.snippet.channelTitle,
			"albumarturl" : this.props.song.snippet.thumbnails.default.url,
			"songID"      : this.props.song.id.videoId,
            "upvotes"     : 0,
            "downvotes"   : 0,
            "upvoted"     : false,
            "downvoted"   : false
        });
        vynl.sockets.addSong(song);
	},
    render: function() {
        var title = this.props.song.snippet.title;
        var rowStyle = {
            paddingTop: '3px',
            paddingBottom: '3px'
        };
        return (
            <li style={rowStyle}><a onClick={this.handleOnClick} className={'dropdown-row'} href="javascript:void(0);">{title}</a></li>
        );
    }
});

var SearchSongDropDown = React.createClass({
    render: function() {
        var rows = [];
        this.props.songs.forEach(function(song) {
            rows.push(<SearchSongRow song={song} key={song.snippet.title} />);
        });
        return (
            <ul id={'search_results'} className={'dropdown-menu'} role={'menu'}>
            {rows}
            </ul>
        );
    }
});

var SearchSongDynamic = React.createClass({
    getInitialState: function() {

        return {
            songs: [],
            value: ''
        };
    },
	handleClick: function(e) {
        console.log(e.target.className);
        if (e.target.className == 'dropdown-row' || e.target.className == 'dropdown-menu') {
            $("#search_input").val("");
            //console.log("hiiii");
			//$(React.findDOMNode(this.refs.searchSongDropDown)).show();
		}
		if (e.target.className != 'form-control' || this.state.value == '') {
			//console.log("hola");
            $(React.findDOMNode(this.refs.searchSongDropDown)).hide();
		} else if (e.target.className == 'form-control') {
			$(React.findDOMNode(this.refs.searchSongDropDown)).show();
		}
	},
	componentDidMount: function() {
        document.addEventListener("tap", this.handleClick);
        document.addEventListener("click", this.handleClick);
	},
    handleOnChange: function(event) {
        this.setState({value: event.target.value});
        function doThang(that,query) {
            if (query) {
                search(query, function(response) {
                    console.log(response.items);
                    that.setState({songs: response.items});
                }.bind(that));
                $(React.findDOMNode(that.refs.searchSongDropDown)).show();
            }
        }
        function delay(that,q){
            clearTimeout(typingTimer);
            if ($("#search_input").val) {
                console.log("we're in");
                function what(){
                    return doThang(that,q);
                }
                typingTimer = setTimeout(what, doneTypingInterval);
            }
        }
        var query = event.target.value;
        $("#search_input").keyup(delay(this , query));


    },
    render: function() {
        var value = this.state.value;
        return (
                <div>
                    <input onChange={this.handleOnChange} value={value} id={"search_input"} data-toggle={"dropdown"} type={"text"} className={"form-control"} placeholder={"Enter the name of a song."} autoFocus={"autofocus"} autoComplete={"off"} />
                    <SearchSongDropDown songs={this.state.songs} ref="searchSongDropDown" />
                </div>
                );
    }
});

React.render(<SearchSongDynamic />, document.getElementById('SearchSongDynamic'));
