define(function (require) {
    var util = require('./util');
    require('./foo');

    require(['./poo'], function (poo) {});

    console.log('Hello world');
});
