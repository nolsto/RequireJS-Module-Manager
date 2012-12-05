define(function(require) {
  'use strict';

  var _ = require('underscore'),
      Handlebars = require('handlebars'),
      template = require('text!templates/navigation.hbs'),
      PageView = require('views/base/page_view'),
      mediator = require('mediator');

  var NavigationView = PageView.extend({

    template: Handlebars.compile(template),

    id: 'navigation',

    container: '.outer-container',

    isActive: false,

    initialize: function() {
      console.log(this.template);
      PageView.prototype.initialize.apply(this, arguments);

      this.delegate('click', '.menu-item > a', this.select);
      this.delegate('click', 'a.toggle', this.toggle);
      this.subscribeEvent('controllerLoaded', this.update);
    },

    afterRender: function() {
      PageView.prototype.afterRender.apply(this, arguments);
      if (!this.isActive) {
        this.$el.css('left', -this.$el.innerWidth());
      }
    },

    select: function(event) {
      if (this.isActive) {
        this.collapse();
      } else {
        this.expand();
      }
    },

    toggle: function(event) {
      if (this.isActive) {
        this.collapse();
      } else {
        this.expand();
      }
      return false;
    },

    expand: function() {
      this.$('a.toggle').addClass('active');
      this.$el.animate({'left': 0}, 'fast', 'linear', _.bind(function() {
        this.isActive = true;
      }, this));
    },

    collapse: function() {
      this.$('a.toggle').removeClass('active');
      var width = this.$el.innerWidth();
      this.$el.animate({'left': -width}, 'fast', 'linear', _.bind(function() {
        this.isActive = false;
      }, this));
    },

    update: function() {
      var id = mediator.currentSlide.get('sid');
      this.$('.menu-item').removeClass('current');
      this.$('.item-' + id).addClass('current');
    }
  });

  return NavigationView;
});
