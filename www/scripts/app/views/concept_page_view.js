define(function(require) {
  'use strict';

  var template = require('views/templates/concept');
  var PageView = require('views/base/page_view');
  var mediator = require('mediator');

  var ConceptPageView = PageView.extend({

    template: template,

    className: 'concept-page',

    initialize: function() {
      PageView.prototype.initialize.apply(this, arguments);
      mediator.publish('!changePrompt');
    },

    afterRender: function() {
      PageView.prototype.afterRender.apply(this, arguments);
      mediator.publish('!resizePageContainer');
    }
  });

  return ConceptPageView;
});
