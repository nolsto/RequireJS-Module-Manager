define(function(require) {
  'use strict';

  var _ = require('underscore'),
      template = require('views/templates/target'),
      View = require('views/base/view'),
      mediator = require('mediator');

  var TargetView = View.extend({

    template: template,

    autoRender: true,

    className: 'target',

    fadeInDuration: 600,

    fadeOutDuration: 1000,

    initialize: function() {
      View.prototype.initialize.apply(this, arguments);

      _.bindAll(this, ['fadeIn', 'fadeOut']);

      var width = this.model.get('parent').get('parent').getWidth();
      var height = this.model.get('parent').get('parent').getHeight();
      this.t = Math.round((parseFloat(this.model.get('t'))) * height);
      this.r = Math.round((parseFloat(this.model.get('r'))) * width);
      this.b = Math.round((parseFloat(this.model.get('b'))) * height);
      this.l = Math.round((parseFloat(this.model.get('l'))) * width);
      this.w = width - this.l - this.r;
      this.h = height - this.t - this.b;
      this.width = width + 4; // compensate for two-pixel offset
      this.height = height + 4; // compensate for two-pixel offset
    },

    render: function() {
      View.prototype.render.apply(this, arguments);
      this.resetOverlay();
    },

    afterRender: function() {
      View.prototype.afterRender.apply(this, arguments);

      this.$el.css('cursor', 'auto');
      this.fadeIn();
    },

    resetOverlay: function() {
      this.$el.css('opacity', 0);
      this.$('.trapezoid.top').css({width: this.width});
      this.$('.trapezoid.right').css({height: this.height, left: this.width});
      this.$('.trapezoid.bottom').css({width: this.width, top: this.height});
      this.$('.trapezoid.left').css({height: this.height});
    },

    fadeIn: function() {
      var extra = 2; // prevents gaps between shapes from showing

      this.$el.animate({opacity: 1}, this.fadeInDuration, this.fadeOut);
      this.$('.trapezoid.top').animate({
        'border-top-width': this.t + extra,
        'border-left-width': this.l,
        'border-right-width': this.r,
        'width': this.w
      }, this.fadeInDuration);

      this.$('.trapezoid.right').animate({
        'border-right-width': this.r + extra,
        'border-top-width': this.t,
        'border-bottom-width': this.b,
        'height': this.h,
        'left': this.l + this.w - extra
      }, this.fadeInDuration);

      this.$('.trapezoid.bottom').animate({
        'border-bottom-width': this.b + extra,
        'border-left-width': this.l,
        'border-right-width': this.r,
        'width': this.w,
        'top': this.t + this.h - extra
      }, this.fadeInDuration);

      this.$('.trapezoid.left').animate({
        'border-left-width': this.l + extra,
        'border-top-width': this.t,
        'border-bottom-width': this.b,
        'height': this.h
      }, this.fadeInDuration);

      setTimeout(_.bind(function() {
        this.trigger('complete');
      }, this), this.fadeInDuration);
    },

    fadeOut: function() {
      setTimeout(_.bind(function() {
        this.$el.animate({opacity: 0}, this.fadeInDuration);
      }, this), this.fadeOutDuration);
    }
  });

  return TargetView;
});
