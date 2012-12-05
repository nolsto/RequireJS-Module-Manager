define(function(require) {
  var Image = require('./image');

  describe('Image', function() {

    it('should load module to test', function() {
      expect(Image).to.not.be.undefined;
    });

    it('should set and get', function() {
      var image = new Image();

      image.set('src', '/path/to');
      expect(image.get('src')).to.equal('/path/to');
    });
  });
});
