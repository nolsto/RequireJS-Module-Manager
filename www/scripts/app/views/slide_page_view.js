define(function(require) {
  'use strict';

  var $ = require('jquery'),
      _ = require('underscore'),
      PageView = require('views/base/page_view'),
      VideoScreenView = require('views/screens/video_screen_view'),
      ImageScreenView = require('views/screens/image_screen_view'),
      mediator = require('mediator'),
      template = require('views/templates/slide');

  var screenAttrs = ['imageScreen', 'videoScreen'];

  var SlidePageView = PageView.extend({

    template: template,

    className: 'slide-page',

    autoRender: true,

    screenView: null,

    initialize: function() {
      PageView.prototype.initialize.apply(this, arguments);

      _.bindAll(this, ['loadHandler', 'changePromptHandler']);

      this.delegate('click', '.previous-button', this.previousSlidePage);
      this.delegate('click', '.next-button', this.nextSlidePage);
      this.subscribeEvent('resizeWindow', this.resizeWindowHandler);

      mediator.publish('!changePrompt', this.model.get('prompt'));
      this.subscribeEvent('!changePrompt', this.changePromptHandler);
    },

    render: function() {
      PageView.prototype.render.apply(this, arguments);
      this.$el.addClass('visuallyhidden');
    },

    renderSubviews: function() {
      this.removeSubview(this.screenView);

      var screenModel = _.chain(screenAttrs)
        .map(function(attr) {
          return this.model.get(attr);
        }, this)
        .compact()
        .last()
        .value();
      if (screenModel != null) {
        this.screenView = this.subview('screenView',
          this.createScreenView(screenModel));
      }
    },

    afterRender: function() {
      PageView.prototype.afterRender.apply(this, arguments);

      if (this.screenView != null) {
        this.screenView.on('ready', function() {
          this.loadHandler();
          this.screenView.on('completed', this.nextSlidePage);
          this.screenView.start();
        }, this);
      } else {
        setTimeout(this.loadHandler, 100);
      }
    },

    createScreenView: function(model) {
      var module;
      switch (model.mediaType) {
        case 'image':
          module = ImageScreenView;
          break;
        case 'video':
          module = VideoScreenView;
          break;
        default:
          return;
      }
      return new module({
        container: this.$('.screen-container'),
        model: model
      });
    },

    loadHandler: function() {
      this.$el.removeClass('visuallyhidden');
      this.trigger('loaded');
      mediator.publish('!resizePageContainer', this.$el.outerHeight());
    },

    resizeWindowHandler: function(dimensions) {
      var tch = this.$('.text-container').outerHeight();
      var sch = this.$('.screen-container').outerHeight();
      var dy = (dimensions.height - sch) / 2 - tch;
      this.$('.screen-container').css('margin-top', dy);
    },

    changePromptHandler: function(newPrompt) {
      newPrompt = newPrompt || '';
      var $promptEl = $('<p>' + newPrompt + '</p>')
        .appendTo(this.$('.prompt-container').empty());
      $promptEl.fadeIn(300);
    },

    previousSlidePage: function() {
      mediator.publish('!previousController');
      return false;
    },

    nextSlidePage: function() {
      mediator.publish('!nextController');
      return false;
    }
  });

  return SlidePageView;
});
