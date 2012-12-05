define([
  'underscore',
  'chaplin',
  'views/base/view'
], function(_, Chaplin, View) {
  'use strict';

  var PageView = View.extend({

    container: '#page-container',

    autoRender: true,

    renderedSubviews: false,

    initialize: function() {
      View.prototype.initialize.apply(this, arguments);

      if (this.model || this.collection) {
        var rendered = false;
        this.modelBind('change', _.bind(function() {
          if (!rendered) {
            this.render();
          }
          rendered = true;
        }, this));
      }
    },

    renderSubviews: function() {},

    render: function() {
      View.prototype.render.apply(this, arguments);

      if (!this.renderedSubviews) {
        this.renderSubviews();
        this.renderedSubviews = true;
      }
    }
  });

  return PageView;
});
