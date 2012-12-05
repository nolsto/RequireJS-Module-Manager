define(function(require) {
  'use strict';

  var SwipeTriggerMixin = require('mixins/triggers/base/swipe_trigger_mixin');

  var SwipeUpTriggerMixin = SwipeTriggerMixin.extend({
    cursor: 'n-resize',
    triggerEvent: 'swipe:up'
  });

  return SwipeUpTriggerMixin;
});
