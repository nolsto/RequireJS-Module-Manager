define(function(require) {
  'use strict';

  var _ = require('underscore'),
      mediator = require('mediator'),
      PageView = require('views/base/page_view'),
      TargetView = require('views/target_view');

  var ActionView = PageView.extend({

    id: 'action',

    autoRender: false,

    triggers: [],

    initialize: function() {
      PageView.prototype.initialize.apply(this, arguments);

      var triggerNames = this.model.get('trigger').split(' ');
      this.triggers = _.compact(_.map(triggerNames, function(name) {
        return this.getTrigger(name);
      }, this));
    },

    afterRender: function() {
      PageView.prototype.afterRender.apply(this, arguments);

      if (!this.model.get('visible')) {
        this.$el.css('opacity', 0);
      }
      this.$el.hammer(mediator.hammerDefaults);
    },

    renderSubviews: function() {
      if (this.model.has('prompt')) {
        mediator.publish('!changePrompt', this.model.get('prompt'));
      }
      if (this.model.has('target')) {
        this.subview('targetView', new TargetView({
          container: this.el,
          model: this.model.get('target')
        })).on('complete', this.addTriggers, this);
      } else {
        this.addTriggers();
      }
    },

    addTriggers: function() {
      _.each(this.triggers, function(trigger) {
        _.extend(this, new trigger());
        this.addTrigger();
      }, this);
    },

    onTrigger: function() {
      mediator.publish('!changePrompt');
      this.trigger('completed');
    },

    getTrigger: function(name) {
      var mixin;
      try {
        mixin = require('mixins/triggers/' + name + '_trigger_mixin');
      } catch (error) {
        console.log('WARNING No Mixin module found for action trigger: ' + name);
      }
      return mixin;
    }
  });

  return ActionView;
});
