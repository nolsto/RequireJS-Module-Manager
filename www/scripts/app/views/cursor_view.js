define(function(require) {
  'use strict';

  var $ = require('jquery'),
      _ = require('underscore'),
      View = require('views/base/view');

  var CursorView = View.extend({

    autoRender: true,

    id: 'cursor',

    container: '.outer-container',

    fadeOutDuration: 200,

    canvas: null,

    ctx: null,

    style: {
      color: 'red',
      join: 'round',
      radius: 19,
      opacity: 0.5
    },

    initialize: function() {
      View.prototype.initialize.apply(this, arguments);

      _.bindAll(this, ['resize', 'reset']);

      this.subscribeEvent('mousedown', this.mousedownHandler);
      this.subscribeEvent('mousemove', this.mousemoveHandler);
      this.subscribeEvent('mouseleave', this.mouseupHandler);
      this.subscribeEvent('mouseup', this.mouseupHandler);
      this.subscribeEvent('resizeWindow', this.resize);
    },

    render: function() {
      View.prototype.render.apply(this, arguments);

      this.canvas = $('<canvas></canvas>').appendTo(this.el)[0];
      this.ctx = this.canvas.getContext('2d');
    },

    resize: function(dimensions) {
      if (!dimensions) {
        return;
      }
      this.$('canvas').attr(dimensions);
    },

    mousedownHandler: function(position) {
      this.reset();
      this.ctx.moveTo(position.x, position.y);
      this.drawCircle(position);
      this.ctx.beginPath();
      this.ctx.strokeStyle = this.style.color;
      this.ctx.lineJoin = this.style.join;
      this.ctx.lineCap = this.style.join;
      this.ctx.globalAlpha = 1.0;
      this.ctx.lineWidth = this.style.radius * 2;
    },

    mousemoveHandler: function(position) {
      this.ctx.globalAlpha = 0.15;
      this.ctx.lineTo(position.x, position.y);
      this.ctx.stroke();
    },

    mouseupHandler: function(position) {
      this.ctx.globalAlpha = 1.0;
      this.ctx.closePath();
      this.fadeOut();
    },

    drawCircle: function(position) {
      this.ctx.beginPath();
      this.ctx.fillStyle = this.style.color;
      this.ctx.arc(position.x, position.y, this.style.radius * 1.2,
        0, Math.PI * 2, true);
      this.ctx.closePath();
      this.ctx.fill();
    },

    fadeOut: function() {
      this.$el.animate({opacity: 0}, this.fadeOutDuration, this.reset);
    },

    reset: function() {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.$el.stop();
      this.$el.css('opacity', this.style.opacity);
    }
  });

  return CursorView;
});
