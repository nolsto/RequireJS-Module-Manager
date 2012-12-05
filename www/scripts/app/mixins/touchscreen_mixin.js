define(function(require) {
  'use strict';

  var $ = require('jquery'),
      mediator = require('mediator'),
      Chaplin = require('chaplin');

  var TouchscreenMixin = {

    delegate: Chaplin.View.prototype.delegate,

    undelegate: Chaplin.View.prototype.undelegate,

    resetMouseHandlers: function() {
      this.undelegate();
      this.delegate('mousedown', this.mousedownHandler);
    },

    mousedownHandler: function (event) {
      mediator.publish('mousedown', {x: event.clientX, y: event.clientY});
      this.delegate('mousemove', this.mousemoveHandler);
      this.delegate('mouseleave', this.mouseleaveHandler);
      $(window).on('mouseup', this.mouseupHandler);
    },

    mousemoveHandler: function (event) {
      mediator.publish('mousemove', {x: event.clientX, y: event.clientY});
    },

    mouseleaveHandler: function (event) {
      mediator.publish('mouseleave', {x: event.clientX, y: event.clientY});
      this.resetMouseHandlers();
    },

    mouseupHandler: function (event) {
      mediator.publish('mouseup', {x: event.clientX, y: event.clientY});
      this.resetMouseHandlers();
      $(window).off('mouseup', this.mouseupHandler);
    }
  };

  return TouchscreenMixin;
});
