define(function(require) {
  'use strict';

  var $ = require('jquery'),
      _ = require('underscore'),
      View = require('views/base/view');

  var PromptView = View.extend({

    autoRender: true,

    id: 'prompt',

    container: '.outer-container',

    initialize: function() {
      View.prototype.initialize.apply(this, arguments);
      this.subscribeEvent('!changePrompt', _.bind(this.changePromptHandler, this));
    },

    changePromptHandler: function(newPrompt) {
      newPrompt = newPrompt || '';
      $('<p>' + newPrompt + '</p>').appendTo(this.$el.empty()).fadeIn(300);
    }
  });

  return PromptView;
});
