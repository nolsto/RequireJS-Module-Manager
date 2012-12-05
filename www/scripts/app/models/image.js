define(function(require) {
  'use strict';

  var Model = require('models/base/model');
  var mediator = require('mediator');

  var Image = Model.extend({

    initialize: function() {
      var filename = this.get('filename');
      this.set('src', mediator.imagePath + '/' + filename);
    }
  });

  return Image;
});
