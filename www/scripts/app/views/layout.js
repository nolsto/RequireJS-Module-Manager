define(function(require) {
  'use strict';

  var $ = require('jquery'),
      _ = require('underscore'),
      Chaplin = require('chaplin'),
      mediator = require('mediator');

  var Layout = Chaplin.Layout.extend({

    $pageContainer: $('#page-container'),

    hideOldView: function(controller) {
      // negate window scrolling to top and hiding of the old view
    },

    showNewView: function(context) {
      // negate making new view visible
    },

    initialize: function() {
      Chaplin.Layout.prototype.initialize.apply(this, arguments);

      _.bindAll(this, ['resizeHandler', 'resizePageContainer']);

      this.subscribeEvent('!resizePageContainer', this.resizePageContainer);
      $(window).on('resize', this.resizeHandler);
      $(window).trigger('resize');
    },

    resizeHandler: function(event) {
      this.$pageContainer.height($(window).height());

      mediator.publish('resizeWindow', {
        width: $(window).width(),
        height: $(window).height()
      });
    },

    resizePageContainer: function(newHeight) {
      if (newHeight) {
        this.$pageContainer.height(newHeight);
      }
      $(window).trigger('resize');
    },

    dispose: function() {
      Chaplin.Layout.prototype.dispose.apply(this, arguments);
      $(window).off('resize', this.resizeHandler);
    }
  });

  return Layout;
});
