
function handleClientLoad() {
    gapi.client.setApiKey(apiKey);
    gapi.client.load('youtube', 'v3', function() {});
    console.log("youtube client loaded");
}

function search(query, callback) {
    var request = gapi.client.youtube.search.list({
        q: query,
        type: 'video',
        part: 'snippet'
    });
    request.execute(callback);
}

var SearchSongRow = React.createClass({
	handleOnClick: function() {
		var song = new Song({
			"songname": this.props.song.snippet.title,
			"songartist": this.props.song.snippet.channelTitle,
			"albumarturl": this.props.song.snippet.thumbnails.default.url,
			"songID": this.props.song.id.videoId,
                        "upvotes": 0,
                        "downvotes": 0,
                        "upvoted": false,
                        "downvoted": false
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
            <li style={rowStyle}><a onClick={this.handleOnClick} href="javascript:void(0);">{title}</a></li>
        );
    }
});

var SearchSongDropDown = React.createClass({
    componentDidMount: function() {
    },
    render: function() {
        var rows = [];
        this.props.songs.forEach(function(song) {
            rows.push(<SearchSongRow song={song} key={song.snippet.title} />);
        });
        return (
            <ul id={'search_results'} className={'dropdown-menu search-option'} role={'menu'}>
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
		if (e.target.className != 'form-control' || this.state.value == '') {
			$(React.findDOMNode(this.refs.searchSongDropDown)).hide();
		} else if (e.target.className == 'form-control') {
			$(React.findDOMNode(this.refs.searchSongDropDown)).show();
		}
	},
	componentDidMount: function() {
		document.addEventListener("click", this.handleClick);
	},
    handleOnKeyDown: function(event) {
        if(event.which == 40) { // down
            $(".search-option").children().first().focus();
            return false; // stops the page from scrolling
        }
        else if(event.which == 38) { // up
            $(".search-option").children().first().focus();
            return false; // stops the page from scrolling
        }
    },
    handleOnChange: function(event) {
        this.setState({value: event.target.value});

        var query = event.target.value;

        if (query != null && query != '') {
            search(query, function(response) {
                console.log(response.items);
                this.setState({songs: response.items});
            }.bind(this));
            $(React.findDOMNode(this.refs.searchSongDropDown)).show();
        }
    },
    render: function() {
        var value = this.state.value;
        return (
                <div className={"dropdown"}>
                    <input onChange={this.handleOnChange} onKeyDown={this.handleOnKeyDown} value={value} id={"search_input"} data-toggle={"dropdown"} type={"text"} className={"form-control dropdown-toggle"} placeholder={"Search"} autoFocus={"autofocus"} autoComplete={"off"} />
                    <SearchSongDropDown songs={this.state.songs} ref="searchSongDropDown" />
                </div>
                );
    }
});

React.render(<SearchSongDynamic />, document.getElementById('SearchSongDynamic'));

        console.log("component mounted");
        $("#search-input").keydown(function(e){
            console.log("hello");
            if(e.which == 13) { // enter
                setTimeout(function(){
                    $(".search-option:first").focus();
                },100);
            }
        });

        $(".search-option").keydown(function(e){
            console.log("hello");
            if(e.which == 40) { // down
                console.log("down");
                $(this).parent().next().find(".search-option").focus();
                return false; // stops the page from scrolling
            }
            if(e.which == 38) { // up
                $(this).parent().prev().find(".search-option").focus();
                return false; // stops the page from scrolling
            }
        });

/*
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
   } */

/*
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
} */

/*
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
*/
