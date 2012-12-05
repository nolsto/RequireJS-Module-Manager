define(function(require) {
  'use strict';

  var $ = require('jquery'),
      _ = require('underscore'),
      mediator = require('mediator'),
      PageView = require('views/base/page_view'),
      TouchscreenMixin = require('mixins/touchscreen_mixin');

  var touchscreenFrames = ['iphone'];

  var ScreenView = PageView.extend({

    className: 'screen',

    isReady: false,

    initialize: function() {
      PageView.prototype.initialize.apply(this, arguments);

      _.bindAll(this, [
        'mousedownHandler',
        'mousemoveHandler',
        'mouseleaveHandler',
        'mouseupHandler'
      ]);
    },

    renderSubviews: function() {
      var mediaView = this.subview('mediaView');
      if (mediaView != null) {
        mediaView.on('loaded', function() {
          this.isReady = true;
          this.onReady();
        }, this);
        mediaView.render();
      }
    },

    afterRender: function() {
      PageView.prototype.afterRender.apply(this, arguments);

      $(this.container).addClass(this.model.getClassName()).css({
        width: this.model.getWidth(),
        height: this.model.getHeight()
      });
      this.addTouchscreen();
    },

    onReady: function() {
      this.trigger('ready');
    // },

    // addTouchscreen: function() {
    //   var hasTouchscreen = _.any(touchscreenFrames, function(name) {
    //     return this.model.get('frame').indexOf(name) !== -1;
    //   }, this);
    //   if (!hasTouchscreen) return;

    //   this.resetMouseHandlers();
    // },

    // resetMouseHandlers: function() {
    //   if (!this.disposed) this.undelegate();
    //   this.delegate('mousedown', this.mousedownHandler);
    // },

    // mousedownHandler: function(event) {
    //   mediator.publish('mousedown', {x: event.clientX, y: event.clientY});
    //   this.delegate('mousemove', this.mousemoveHandler);
    //   this.delegate('mouseleave', this.mouseleaveHandler);
    //   ($ window).on('mouseup', this.mouseupHandler);
    // },

    // mousemoveHandler: function(event) {
    //   mediator.publish('mousemove', {x: event.clientX, y: event.clientY});
    // },

    // mouseleaveHandler: function(event) {
    //   mediator.publish('mouseleave', {x: event.clientX, y: event.clientY});
    //   this.resetMouseHandlers();
    // },

    // mouseupHandler: function(event) {
    //   mediator.publish('mouseup', {x: event.clientX, y: event.clientY});
    //   this.resetMouseHandlers();
    //   ($ window).off('mouseup', this.mouseupHandler);
    }
  });

  return ScreenView;
});
