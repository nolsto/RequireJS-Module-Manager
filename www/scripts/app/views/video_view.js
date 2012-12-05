define(function(require) {
  'use strict';

  var $ = require('jquery'),
      View = require('views/base/view'),
      mediator = require('mediator'),
      VideoJS = require('videojs');

  var VideoView = View.extend({

    tagName: 'video',

    className: 'media',

    videoPlayer: null,

    videoOptions: {
      controls: false,
      autoplay: false,
      preload: 'auto'
    },

    attributes: function() {
      return {
        width: this.model.get('parent').getWidth(),
        height: this.model.get('parent').getHeight()
      };
    },

    afterRender: function() {
      View.prototype.afterRender.apply(this, arguments);
      var view = this;

      this.videoPlayer = VideoJS(this.el, this.videoOptions, function() {
        this.src(view.model.get('sources'));

        this.$videoEl = $('video', this.el);
        this.videoEl = this.$videoEl[0];

        this.handleLoadedData = function(view) {
          this.removeEvent('loadeddata', this.handleLoadedData);
          // find and apply correct aspect ratio
          var videoRatio = this.videoEl.videoWidth / this.videoEl.videoHeight;
          var targetRatio = view.attributes().width / view.attributes().height;
          var adjustmentRatio = (targetRatio / videoRatio).toFixed(3);

          this.$videoEl.css({
            '-webkit-transform': 'scaleX(' + adjustmentRatio + ')',
            '-moz-transform': 'scaleX(' + adjustmentRatio + ')',
            '-o-transform': 'scaleX(' + adjustmentRatio + ')',
            '-ms-transform': 'scaleX(' + adjustmentRatio + ')',
            'transform': 'scaleX(' + adjustmentRatio + ')'
          });

          view.trigger('loaded');
        };

        this.handleEnded = function(view) {
          this.removeEvent('ended', this.handleEnded);
          view.trigger('completed');
        };

        this.addEvent('loadeddata', this.handleLoadedData);
        this.addEvent('ended', this.handleEnded);
      });
    },

    start: function() {
      this.videoPlayer.play();
    }
  });

  return VideoView;
});
