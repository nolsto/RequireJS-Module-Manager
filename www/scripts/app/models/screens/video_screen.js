define(function(require) {
  'use strict';

  var Backbone = require('backbone');
  var Screen = require('models/screens/base/screen');
  var Video = require('models/video');

  var VideoScreen = Screen.extend({

    mediaType: 'video',

    relations: [
      {
        type: Backbone.HasOne,
        key: 'video',
        relatedModel: Video,
        reverseRelation: {
          type: Backbone.HasOne,
          key: 'parent',
          includeInJSON: false
        }
      }
    ]
  });

  return VideoScreen;
});
