define([
  'chaplin',
  'models/base/model'
], function(Chaplin, Model) {
  'use strict';

  var Collection = Chaplin.Collection.extend({
    model: Model,

    next: function(model) {
      var index = this.indexOf(model);
      this.at(this.indexOf(model) + 1);
    },

    previous: function(model) {
      var index = this.indexOf(model);
      this.at(this.indexOf(model) - 1);
    }
  });

  return Collection;
});
