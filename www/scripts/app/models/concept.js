define(function(require) {
  'use strict';

  var Backbone = require('backbone');
  var mediator = require('mediator');
  var Model = require('models/base/model');
  var Section = require('models/section');
  var Sections = require('models/sections');

  var Concept = Model.extend({

    url: function() {
      return 'data/' + mediator.conceptDirectory + '.json';
    },

    relations: [
      {
        type: Backbone.HasMany,
        key: 'sections',
        relatedModel: Section,
        collectionType: Sections
      }
    ]
  });

  return Concept;
});
