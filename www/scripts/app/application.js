define(function(require) {
  'use strict';

  var Chaplin = require('chaplin'),
      mediator = require('mediator'),
      routes = require('dispatcher'),
      Layout = require('views/layout'),
      ConceptController = require('controllers/concept_controller'),
      NavigationController = require('controllers/navigation_controller'),
      StatusController = require('controllers/status_controller'),
      CursorController = require('controllers/cursor_controller');

  // The application object
  // Choose a meaningful name for your application
  var Application = Chaplin.Application.extend({

    // Set your application name here so the document title is set to
    // “Controller title – Site title” (see Layout#adjustTitle)
    title: 'Digital Greetings RFI 1 Demos',

    constructor: function(attrs, conceptData) {
      console.log('Application#constructor');
      this.attrs = attrs;
      this.conceptData = conceptData;

      Chaplin.Application.prototype.constructor.apply(this, arguments);
    },

    initialize: function() {
      console.log('Application#initialize');
      // Call the parent constructor.
      Chaplin.Application.prototype.initialize.apply(this, arguments);
      //console.debug 'HelloWorldApplication#initialize'

      // Initialize core components
      this.initDispatcher();
      this.initMediator();
      this.initLayout();

      // Application-specific scaffold
      this.initControllers();

      // Register all routes and start routing
      this.initRouter(routes, {pushState: false});
      // You might pass Router/History options as the second parameter.
      // Chaplin enables pushState per default and Backbone uses / as
      // the root per default. You might change that in the options
      // if necessary:
      // this.initRouter(routes, { pushState: false , root: '/subdir/' });

      // Freeze the application instance to prevent further changes
      if (Object.freeze) {
        Object.freeze(this);
      }
    },

    // Override standard layout initializer
    // ------------------------------------
    initLayout: function() {
      // Use an application-specific Layout class. Currently this adds
      // no features to the standard Chaplin Layout, it’s an empty placeholder.
      this.layout = new Layout({title: this.title});
    },

    // Instantiate common controllers
    // ------------------------------
    initControllers: function() {
      // These controllers are active during the whole application runtime.
      // You don’t need to instantiate all controllers here, only special
      // controllers which do not to respond to routes. They may govern models
      // and views which are needed the whole time, for example header, footer
      // or navigation views.
      new ConceptController(this.conceptData);
      new StatusController();
      new NavigationController();
      new CursorController();
    },

    // Create additional mediator properties
    // -------------------------------------
    initMediator: function() {
      // Create a user property
      mediator.user = null;
      // Add additional application-specific properties and methods
      mediator.survey = 'http://www.surveymonkey.com/s/';

      mediator.conceptDirectory = this.attrs.conceptDirectory;
      mediator.imagePath = 'images/' + this.attrs.conceptDirectory;
      mediator.videoPath = 'videos/' + this.attrs.conceptDirectory;

      mediator.concept = null;
      mediator.slides = null;
      mediator.currentSlide = null;

      mediator.hammerDefaults = {
        prevent_default: false,
        swipe_time: 700,
        swipe_min_distance: 50,
        drag: false
      };

      // Seal the mediator
      mediator.seal();
    }
  });

  return Application;
});
