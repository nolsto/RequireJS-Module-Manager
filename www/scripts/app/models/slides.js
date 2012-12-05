define(function(require) {
  'use strict';

  var Collection = require('models/base/collection');
  var Slide = require('models/slide');

  var Slides = Collection.extend({
    model: Slide
  });

  return Slides;
});
