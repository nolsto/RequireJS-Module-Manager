#!/usr/bin/env node

var util = require('util')
  , options = {showHidden: false, depth: null};

var shared = require('shared')
  , esrefactor = require('esrefactor')
  , args = process.argv.slice(2)
  , requirejs = require(args[0])
  , contents = args[1]
  , matchNode = JSON.parse(args[2])
  , depCollection = JSON.parse(args[3])
  , varChanges = JSON.parse(args[4])
  , leadingComma = Boolean(parseInt(args[5], 10));

requirejs.tools.useLib(function (require) {
  require(['esprimaAdapter', 'parse'], function (esprima, parse) {
    var astRoot = esprima.parse(contents, {range: true, loc: true});

    console.log(util.inspect(matchNode, options));
    console.log(util.inspect(depCollection, options));
    console.log(util.inspect(varChanges, options));
    console.log(util.inspect(leadingComma, options));

    // varChanges.forEach(function (el, i) {

    // });

    console.log(true);
  });
});
