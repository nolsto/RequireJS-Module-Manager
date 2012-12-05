define(function(require) {
  'use strict';

  var SwipeTriggerMixin = require('mixins/triggers/base/swipe_trigger_mixin');

  var SwipeLeftTriggerMixin = SwipeTriggerMixin.extend({
    cursor: 'w-resize',
    triggerEvent: 'swipe:left'
  });

  return SwipeLeftTriggerMixin;
});
