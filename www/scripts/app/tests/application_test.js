define(function(require) {
  var Application = require('../application');

  describe('Application', function() {

    it('should be ok', function() {
      expect(this).to.be.ok;
    });

    it('should load module to test', function() {
      expect(Application).to.not.be.undefined;
    });
  });
});
