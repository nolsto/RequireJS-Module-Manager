define(function(require) {
  var Action = require('./action');

  describe('Action', function() {

    it('should load module to test', function() {
      expect(Action).to.not.be.undefined;
    });

    it('should have relations', function() {
      var action = new Action();

      expect(action.relations).to.be.an.instanceof(Array);
    });

    // it('should have parent key', function() {
    //   var action = new Action();

    //   // expect(image.get('src')).to.equal('/path/to');
    // });
  });
});
