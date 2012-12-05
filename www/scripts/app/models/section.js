define(function(require) {
  'use strict';

  var Backbone = require('backbone'),
      Model = require('models/base/model'),
      Slide = require('models/slide'),
      Slides = require('models/slides');

  var Section = Model.extend({

    relations: [
      {
        type: Backbone.HasMany,
        key: 'slides',
        relatedModel: Slide,
        collectionType: Slides
      }
    ]
  });

  return Section;
});
