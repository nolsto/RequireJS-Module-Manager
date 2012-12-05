define(function(require) {
  'use strict';

  var _ = require('underscore'),
      Model = require('models/base/model');

  var frames = {
    none: {
      className: '',
      dimensions: {w: 640, h: 480}
    },
    iphone_portrait: {
      className: 'iphone portrait',
      dimensions: {w: 240, h: 360}
    },
    iphone_landscape: {
      className: 'iphone landscape',
      dimensions: {w: 360, h: 240}
    },
    browser: {
      className: 'browser',
      dimensions: {w: 640, h: 480}
    }
  };

  var Screen = Model.extend({

    defaults: {frame: 'none'},

    initialize: function() {
      var frameAttrs = this.get('frame').split('@');
      var frameKey = frameAttrs[0];
      var dimensionString = frameAttrs[1];

      this.frame = _.extend({}, frames[frameKey]);

      if (dimensionString != null) {
        var dimensions = _.map(dimensionString.split('x'), function(s) {
          return parseInt(s, 0);
        });
        var w = dimensions[0];
        var h = dimensions[1];
        this.frame.dimensions = {w: w, h: h};
      }
    },

    getWidth: function() {
      return this.frame.dimensions.w;
    },

    getHeight: function() {
      return this.frame.dimensions.h;
    },

    getClassName: function() {
      return this.frame.className;
    }
  });

  return Screen;
});
