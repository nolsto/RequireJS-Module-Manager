define(function(require) {
  'use strict';

  var mediator = require('mediator');
  var Controller = require('controllers/base/controller');
  var Concept = require('models/concept');

  var ConceptController = Controller.extend({

    initialize: function(data) {
      this.model = new Concept(data);
      mediator.concept = this.model;
    }
  });

  return ConceptController;
});
