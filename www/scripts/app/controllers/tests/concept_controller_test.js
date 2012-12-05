define(function(require) {

  var ConceptController = require('../concept_controller');

  describe('ConceptController', function() {

    it('should be ok', function() {
      expect(this).to.not.be.undefined;
    });

    it('should load module to test', function() {
      // expect(ConceptController).to.be.ok;
      expect(ConceptController).to.not.be.undefined;
    });
  });
});
