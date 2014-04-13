#!/usr/bin/env node

var util = require('util')
  , options = {showHidden: false, depth: null};

var shared = require('shared')
  , escope = require('escope')
  , esrefactor = require('esrefactor')
  , args = process.argv.slice(2)
  , requirejs = require(args[0])
  , contents = args[1]
  , matchNode = JSON.parse(args[2])
  , depCollection = JSON.parse(args[3])
  , varChanges = JSON.parse(args[4]);

requirejs.tools.useLib(function (require) {
  require(['esprimaAdapter', 'parse'], function (esprima, parse) {
    var astRoot = esprima.parse(contents, {range: true, loc: true})
      , astContext = new esrefactor.Context(contents, astRoot)
      , scopeManager = escope.analyze(astRoot)
      , factoryNode
      , paramNames
      , varId;

    // console.log(util.inspect(matchNode, options));
    // console.log(util.inspect(depCollection, options));
    // console.log(util.inspect(varChanges, options));


    factoryNode = shared.getFactoryNode(matchNode);
    // paramNames = factoryNode.params.map(function (el) {
    //   return el.name
    // });

    var scope = scopeManager.acquire(factoryNode)
    console.log(util.inspect(scope, options));

    // varChanges.forEach(function (el, i) {
    //   var index = paramNames.indexOf(el[0])
    //     , range = factoryNode.params[index].range
    //     , id = astContext.identify(range[0])
    //     , renamedContent = astContext.rename(id, el[1]);

    //   console.log(renamedContent);
    // });

    // console.log(result);
    // console.log(util.inspect(id, options));
  });
});
