#!/usr/bin/env node

var util = require('util')
  , options = {showHidden: false, depth: null/*, colors: true*/};

var fs = require('fs')
  , estraverse = require('estraverse')
  , escope = require('escope')
  , args = process.argv.slice(2)
  , requirejs = require(args[0])
  , contents = args[1]
  , selection = (args[2].split(',')).map(function (n) {
    return parseInt(n, 10);
  });

requirejs.tools.useLib(function (require) {
  require(['esprimaAdapter', 'parse'], function (esprima, parse) {
    var astRoot = esprima.parse(contents, {range: true})
      , pos = selection[0]
      , selectionNode
      , selectionDeps
      , selectionFactoryNode;
      // , scopeManager
      // , scope;

    // patch method to prevent inclusion of "require", "exports" and "module"
    // in dependencies
    parse.getAnonDepsFromNode = function (node) {
      var deps = [];

      if (node) {
        this.findRequireDepNames(node, deps);
      }
      return deps;
    };

    parse.recurse(astRoot, function (callName, config, name, deps, node) {
      if (!selectionNode || node.range[0] <= pos && node.range[1] >= pos) {
        selectionNode = node;
        selectionDeps = deps;
        selectionFactoryNode = getFactoryNode(node)
      }
      return true; // find nested dependencies
    });

    // scopeManager = escope.analyze(astRoot);
    // scope = scopeManager.acquire(selectionFactoryNode);

    // deps = deps.filter(function (v, i, arr) {
    //   return arr.lastIndexOf(v) === i;
    // });
    // deps.sort();
    console.log(JSON.stringify(selectionDeps));
  });
});
