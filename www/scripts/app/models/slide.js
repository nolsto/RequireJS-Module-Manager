define(function(require) {
  'use strict';

  var Backbone = require('backbone');
  var Model = require('models/base/model');
  var ImageScreen = require('models/screens/image_screen');
  var VideoScreen = require('models/screens/video_screen');

  var menuItemCount = 0;

  var Slide = Model.extend({

    relations: [
      {
        type: Backbone.HasOne,
        key: 'imageScreen',
        relatedModel: ImageScreen
      }, {
        type: Backbone.HasOne,
        key: 'videoScreen',
        relatedModel: VideoScreen
      }
    ],

    initialize: function() {
      if (this.has('menuItem')) {
        this.set('sid', 's' + menuItemCount);
        menuItemCount++;
      }
    }
  });

  return Slide;
});
