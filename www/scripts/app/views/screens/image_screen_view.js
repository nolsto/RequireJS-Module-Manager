define(function(require) {
  'use strict';

  var _ = require('underscore'),
      ScreenView = require('views/screens/base/screen_view'),
      ImageView = require('views/image_view'),
      ActionView = require('views/action_view');

  var ImageScreenView = ScreenView.extend({

    actionDelay: 1500,

    renderSubviews: function() {
      this.subview('mediaView', new ImageView({
        container: this.el,
        model: this.model.get('image')
      }));
      this.subview('actionView', new ActionView({
        container: this.el,
        model: this.model.get('action')
      })).on('completed', function() {
        this.trigger('completed');
      }, this);

      ScreenView.prototype.renderSubviews.apply(this, arguments);
    },

    start: function() {
      if (!this.isReady) {
        return;
      }

      setTimeout(_.bind(function() {
        this.subview('actionView').render();
      }, this), this.actionDelay);
    }
  });

  return ImageScreenView;
});
