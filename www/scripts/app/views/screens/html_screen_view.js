define(function(require) {
  'use strict';

  var _ = require('underscore'),
      ScreenView = require('views/screens/base/screen_view'),
      ImageView = require('views/image_view'),
      ActionView = require('views/action_view');

  var HtmlScreenView = ScreenView.extend({

    actionDelay: 600,

    afterRender: function() {
      ScreenView.prototype.afterRender.apply(this, arguments);

      this.isReady = true;
      this.onReady();
    },

    resetMouseHandlers: function() {},

    start: function() {
      if (!this.isReady) {
        return;
      }

      setTimeout(_.bind(function() {
        this.subview('actionView').render();
      }, this), this.actionDelay);
    }
  });

  return HtmlScreenView;
});
