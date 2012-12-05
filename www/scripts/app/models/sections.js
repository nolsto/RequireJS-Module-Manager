define(function(require) {
  'use strict';

  var Collection = require('models/base/collection'),
      Section = require('models/section');

  var Sections = Collection.extend({
    model: Section
  });

  return Sections;
});
