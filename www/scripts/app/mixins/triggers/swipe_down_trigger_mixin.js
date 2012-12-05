define(function(require) {
  'use strict';

  var SwipeTriggerMixin = require('mixins/triggers/base/swipe_trigger_mixin');

  var SwipeDownTriggerMixin = SwipeTriggerMixin.extend({
    cursor: 's-resize',
    triggerEvent: 'swipe:down'
  });

  return SwipeDownTriggerMixin;
});
