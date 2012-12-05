define(function(require) {
  'use strict';

  var _ = require('underscore'),
      View = require('views/base/view'),
      mediator = require('mediator');

  var ImageView = View.extend({

    tagName: 'img',

    className: 'media',

    attributes: function() {
      return {
        width: this.model.get('parent').getWidth(),
        height: this.model.get('parent').getHeight()
      };
    },

    initialize: function() {
      View.prototype.initialize.apply(this, arguments);

      this.delegate('load', _.bind(function() {
        this.trigger('loaded');
      }, this));
    },

    render: function() {
      View.prototype.render.apply(this, arguments);
      this.$el.attr('src', this.model.get('src'));
    }
  });

  return ImageView;
});
