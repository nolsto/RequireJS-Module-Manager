define([
  'underscore',
  'chaplin',
  'backbone',
  'backbone-relational'
], function(_, Chaplin, Backbone) {
  'use strict';

  var attributes = [
    'initDeferred',
    'getAttributes',
    'serializeAttributes',
    'serialize',
    'disposed',
    'dispose'
  ];
  var Model = Backbone.RelationalModel.extend();

  _.extend(Model.prototype, Chaplin.EventBroker);

  _.each(attributes, function(attr) {
    Model.prototype[attr] = Chaplin.Model.prototype[attr];
  });

  return Model;
});
