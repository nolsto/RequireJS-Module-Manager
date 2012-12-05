define(function(require) {
  'use strict';

  var template = require('text!templates/status.hbs');
  var View = require('views/base/view');

  var StatusView = View.extend({

    template: template,

    autoRender: true,

    id: 'status',

    container: '.outer-container',

    initialize: function() {
      View.prototype.initialize.apply(this, arguments);

      this.subscribeEvent('beforeControllerDispose', this.show);
      this.subscribeEvent('controllerLoaded', this.hide);
    },

    show: function() {
      this.$el.removeClass('invisible');
    },

    hide: function() {
      this.$el.addClass('invisible');
    }
  });

  return StatusView;
});
