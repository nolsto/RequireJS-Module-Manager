define(function(require) {
  'use strict';

  var mediator = require('mediator');
  var Controller = require('controllers/base/controller');
  var CursorView = require('views/cursor_view');

  var CursorController = Controller.extend({

    initialize: function() {
      this.view = new CursorView();
    }
  });

  return CursorController;
});
