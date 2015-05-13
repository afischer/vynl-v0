function handleClientLoad() {
    gapi.client.setApiKey(apiKey);
    gapi.client.load('youtube', 'v3', function() {});
    console.log("youtube client loaded");
}

function search(query, callback) {
    var q = query;
    var request = gapi.client.youtube.search.list({
        q: q,
        part: 'snippet'
    });

    request.execute(callback);
}

var SearchSongRow = React.createClass({
    render: function() {
        var title = this.props.song.snippet.title;
        var rowStyle = {
            paddingTop: '3px',
            paddingBottom: '3px'
        };
        return (
            <li style={rowStyle}><a href="#">{title}</a></li>
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

/*
var SearchSongBar = React.createClass({
	handleOnKeyUp: function() {
		console.log("bad key up");
	},
	render: function() {
		return (
			<input onKeyUp={this.handleOnKeyUp} id={"search_input"} data-toggle={"dropdown"} type={"text"} className={"form-control"} placeholder={"Search"} autoFocus={"autofocus"} autoComplete={"off"} />
		);
	}
});
*/

var SearchSongDynamic = React.createClass({	
	getInitialState: function() {
		return {songs: [],
			value: ''};
	},
	componentDidMount: function() {
	},
	componentWillUnmount: function() {
	},
	handleOnChange: function(event) {
		this.setState({value: event.target.value});

		var query = event.target.value;
		search(query, function(response) {
			console.log(response.items);
			this.setState({songs: response.items});
		}.bind(this));
	},
	render: function() {
		var value = this.state.value;
		return (
			<div>
				<input onChange={this.handleOnChange} value={value} id={"search_input"} data-toggle={"dropdown"} type={"text"} className={"form-control"} placeholder={"Search"} autoFocus={"autofocus"} autoComplete={"off"} />
				<SearchSongDropDown songs={this.state.songs} />
			</div>
		);
	}
});

React.render(<SearchSongDynamic />, document.getElementById('SearchSongDynamic'));

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
