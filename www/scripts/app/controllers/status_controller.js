define(function(require) {
  'use strict';

  var mediator = require('mediator');
  var Controller = require('controllers/base/controller');
  var StatusView = require('views/status_view');

  var StatusController = Controller.extend({

    initialize: function() {
      this.view = new StatusView();
    }
  });

  return StatusController;
});
