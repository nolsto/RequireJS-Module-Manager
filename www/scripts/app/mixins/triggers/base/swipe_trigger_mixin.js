define(function(require) {
  'use strict';

  var _ = require('underscore'),
      TriggerMixin = require('mixins/triggers/base/trigger_mixin');

  var SwipeTriggerMixin = TriggerMixin.extend({
    cursor: 'move',

    triggerEvent: 'swipe',

    addTrigger: function() {
      TriggerMixin.prototype.addTrigger.apply(this, arguments);

      var t = this.triggerEvent.split(':');
      var baseEvent = t[0];
      var direction = t[1];

      this.delegate(baseEvent, _.bind(function (event) {
        var ev = event.originalEvent;

        if (ev.target === this.el && event.direction === direction) {
          this.onTrigger();
        }
      }, this));
    }
  });

  return SwipeTriggerMixin;
});
