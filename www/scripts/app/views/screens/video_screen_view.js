define(function(require) {
  'use strict';

  var ScreenView = require('views/screens/base/screen_view'),
      VideoView = require('views/video_view');

  var VideoScreenView = ScreenView.extend({

    renderSubviews: function() {
      this.subview('mediaView', new VideoView({
        id: this.cid,
        container: this.el,
        model: this.model.get('video')
      })).on('completed', function() {
        this.trigger('completed');
      }, this);

      ScreenView.prototype.renderSubviews.apply(this, arguments);
    },

    start: function() {
      if (!this.isReady) {
        return;
      }
      this.subview('mediaView').start();
    }
  });

  return VideoScreenView;
});
