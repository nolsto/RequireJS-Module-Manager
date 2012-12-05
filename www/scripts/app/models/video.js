define(function(require) {
  'use strict';

  var Model = require('models/base/model');
  var mediator = require('mediator');

  var Video = Model.extend({

    initialize: function() {
      var basename = this.get('basename');
      var posterFilename = this.get('posterFilename');

      if (posterFilename != null) {
        this.set('posterSrc', mediator.imagePath + '/' + posterFilename);
      }
      this.set('sources', [
        {src: mediator.videoPath + '/' + basename + '.mp4', type: 'video/mp4'},
        {src: mediator.videoPath + '/' + basename + '.webm', type: 'video/webm'}
      ]);
    }
  });

  return Video;
});
