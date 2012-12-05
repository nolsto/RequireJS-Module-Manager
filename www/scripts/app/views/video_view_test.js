define(function(require) {
  var VideoView = require('./video_view');

  describe('VideoView', function() {

    it('should load module to test', function() {
      expect(VideoView).to.not.be.undefined;
    });

    it('should load VideoJS as a dependency', function() {
      var view = new VideoView();
      expect(view.$el.html()).to.not.be.empty;
    });
  });
});
