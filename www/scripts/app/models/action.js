define(function(require) {
  'use strict';

  var Backbone = require('backbone'),
      Model = require('models/base/model');

  var Action = Model.extend({

    defaults: {visible: true},

    relations: [
      {
        type: Backbone.HasOne,
        key: 'target',
        relatedModel: Model,
        reverseRelation: {
          type: Backbone.HasOne,
          key: 'parent',
          includeInJSON: false
        }
      }
    ]
  });

  return Action;
});
