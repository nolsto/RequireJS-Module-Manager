define(function(require) {
  'use strict';

  var mediator = require('mediator');
  var Controller = require('controllers/base/controller');
  var PromptView = require('views/prompt_view');

  var NavigationController = Controller.extend({

    initialize: function() {
      this.view = new PromptView();
    }
  });

  return NavigationController;
});
