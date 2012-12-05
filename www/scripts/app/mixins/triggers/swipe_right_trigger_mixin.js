define(function(require) {
  'use strict';

  var SwipeTriggerMixin = require('mixins/triggers/base/swipe_trigger_mixin');

  var SwipeRightTriggerMixin = SwipeTriggerMixin.extend({
    cursor: 'e-resize',
    triggerEvent: 'swipe:right'
  });

  return SwipeRightTriggerMixin;
});
