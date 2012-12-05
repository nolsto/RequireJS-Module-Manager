define(function(require) {
  'use strict';

  var mediator = require('mediator');
  var Controller = require('controllers/base/controller');
  var Slides = require('models/slides');
  var NavigationView = require('views/navigation_view');

  var NavigationController = Controller.extend({

    initialize: function() {
      this.collection = mediator.concept.get('sections');
      this.view = new NavigationView({collection: this.collection});
    }
  });

  return NavigationController;
});
