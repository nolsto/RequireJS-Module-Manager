define(function(require) {
  'use strict';

  var Backbone = require('backbone');
  var Screen = require('models/screens/base/screen');
  var Image = require('models/image');
  var Action = require('models/action');

  var ImageScreen = Screen.extend({

    mediaType: 'image',

    relations: [
      {
        type: Backbone.HasOne,
        key: 'image',
        relatedModel: Image,
        reverseRelation: {
          type: Backbone.HasOne,
          key: 'parent',
          includeInJSON: false
        }
      }, {
        type: Backbone.HasOne,
        key: 'action',
        relatedModel: Action,
        reverseRelation: {
          type: Backbone.HasOne,
          key: 'parent',
          includeInJSON: false
        }
      }
    ]
  });

  return ImageScreen;
});
