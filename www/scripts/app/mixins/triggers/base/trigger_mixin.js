define(function(require) {
  'use strict';

  var _ = require('backbone'),
      Backbone = require('backbone');

  var TriggerMixin = function() {};

  _.extend(TriggerMixin.prototype, {
    cursor: 'auto',

    addTrigger: function() {
      this.$el.css('cursor', this.cursor);
    }
  });

  TriggerMixin.extend = Backbone.Model.extend;

  return TriggerMixin;
});
