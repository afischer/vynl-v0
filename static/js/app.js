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
var test = new Song({"songname":"The Bends","songartist":'Radiohead',"albumarturl":"http://upload.wikimedia.org/wikipedia/en/8/8b/Radiohead.bends.albumart.jpg"});
data.push(test);
console.log(test);


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

