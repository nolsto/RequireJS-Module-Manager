define(function(require) {
  'use strict';

  var $ = require('jquery'),
      Application = require('application');

  var initialize = function (attrs) {
    $(function() {
      $.getJSON('data/' + attrs.conceptDirectory + '.json', function (data) {
        var app = new Application(attrs, data);
        app.initialize();
      });
    });
  };

  return initialize;
});
