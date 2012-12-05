define(function(require) {
  'use strict';

  var _ = require('underscore');
  var Chaplin = require('chaplin');
  var mediator = require('mediator');

  var Dispatcher = Chaplin.Dispatcher.extend({

    controllerLoaded: function(controllerName, action, params, ControllerConstructor) {
      var currentControllerName = this.currentControllerName || null;
      var currentController = this.currentController || null;

      if (currentController) {
        mediator.publish('beforeControllerDispose', currentController);
        currentController.subscribeEvent('controllerLoaded', function() {
          // Dispose the current controller with a timeout
          // to prevent it from disappearing too quickly.
          var callback = _.bind(function() {
            this.dispose(params, controllerName);
          }, this);
          setTimeout(callback, 100);
        });
      }

      var controller = new ControllerConstructor(params, currentControllerName);
      controller[action](params, currentControllerName);

      if (controller.redirected) {
        return;
      }

      this.previousControllerName = currentControllerName;
      this.currentControllerName = controllerName;
      this.currentController = controller;
      this.currentAction = action;
      this.currentParams = params;

      this.adjustURL(controller, params);

      mediator.publish('startupController', {
        previousControllerName: this.previousControllerName,
        controller: this.currentController,
        controllerName: this.currentControllerName,
        params: this.currentParams
      });
    }
  });

  return Dispatcher;
});
