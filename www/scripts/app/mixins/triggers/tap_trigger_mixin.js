define(function(require) {
  'use strict';

  var _ = require('underscore'),
      TriggerMixin = require('mixins/triggers/base/trigger_mixin');

  var TapTriggerMixin = TriggerMixin.extend({
    cursor: 'crosshair',

    triggerEvent: 'tap',

    addTrigger: function() {
      TriggerMixin.prototype.addTrigger.apply(this, arguments);

      this.delegate(this.triggerEvent, _.bind(function (event) {
        var ev = event.originalEvent;

        if (ev.target === this.el) {
          this.onTrigger();
        }
      }, this));
    }
  });

  return TapTriggerMixin;
});
