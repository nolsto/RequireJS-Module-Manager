define(function(require) {
  'use strict';

  var _ = require('underscore');
  var mediator = require('mediator');
  var Controller = require('controllers/base/controller');
  var ConceptPageView = require('views/concept_page_view');
  var SlidePageView = require('views/slide_page_view');
  var Slides = require('models/slides');

  var SlidesController = Controller.extend({

    title: mediator.concept.get('name'),

    historyURL: function(params) {
      if (params.index != null) {
        return '' + params.index;
      } else {
        return mediator.currentSlide ? mediator.currentSlide.get('sid') : '';
      }
    },

    initialize: function() {
      var sections = mediator.concept.get('sections');
      var slides = _.chain(sections.pluck('slides'))
        .map(function(slides) {
          return slides.models;
        })
        .flatten()
        .value();

      this.collection = new Slides(slides);
      mediator.slides = this.collection;

      this.subscribeEvent('!nextController', this.next);
      this.subscribeEvent('!previousController', this.previous);
    },

    show: function(params) {
      var model;
      params = params || {};

      if (params.sid) {
        model = _(this.collection.where({sid: params.sid})).first();
      } else if (params.index != null && params.index !== undefined) {
        model = this.collection.at(parseInt(params.index, 10));
      }
      if (!model) {
        model = this.collection.first();
      }

      mediator.currentSlide = model;

      this.view = new SlidePageView({model: model});
      this.view.on('loaded', function() {
        mediator.publish('controllerLoaded');
      });
    },

    next: function() {
      if (!mediator.currentSlide) {
        return;
      }
      var index = this.collection.indexOf(mediator.currentSlide) + 1;

      if (index === this.collection.length) {
        var surveyURL = mediator.survey + mediator.concept.get('surveyID');
        window.location.href = surveyURL;
      }

      mediator.publish('!startupController', 'slides', 'show', {index: index});
    },

    previous: function() {
      if (!mediator.currentSlide) {
        return;
      }

      var index = this.collection.indexOf(mediator.currentSlide) - 1;
      mediator.publish('!startupController', 'slides', 'show', {index: index});
    }
  });

  return SlidesController;
});
