#!/usr/bin/env node

var shared = require('shared')
  , args = process.argv.slice(2)
  , requirejs = require(args[0])
  , contents = args[1]
  , selection = [parseInt(args[2], 10), parseInt(args[3], 10)]
  , selectionContents = contents.substring(selection[0], selection[1]);

requirejs.tools.useLib(function (require) {
  require(['esprimaAdapter', 'parse'], function (esprima, parse) {
    var astRoot = esprima.parse(contents, {range: true, loc: true})
      , pos = selection[0]
      , selectedId = null
      , selectedVar = null
      , matchDeps
      , matchNode
      , matchContents
      , depArrayNode
      , factoryNode
      , depCollection;

    parse.recurse(astRoot, function (callName, config, name, deps, node) {
      if (!matchNode || node.range[0] <= pos && node.range[1] >= pos) {
        matchDeps = deps || [];
        matchNode = node;
      }
      return true; // find nested dependencies
    });

    // extract the contents of the matched define/require node,
    // determine if it uses CommonJS, and exit if it does
    matchContents = parse.nodeToString(contents, matchNode).value;
    if (parse.usesCommonJs(null, matchContents)) {
      return process.stderr.write('Unable to manage dependencies for modules using a CommonJS wrapper.');
    }

    // extract the dependency array node, exit if it has duplicate elements
    depArrayNode = shared.getDepArrayNode(matchNode);
    if (depArrayNode && !shared.hasUniqueAttrValues(depArrayNode.elements, 'value')) {
      return process.stderr.write('Repeat module Ids in dependency array.')
    };

    // extract the factory function node, exit if it has duplicate parameters
    factoryNode = shared.getFactoryNode(matchNode);
    if (factoryNode && !shared.hasUniqueAttrValues(factoryNode.params, 'name')) {
      return process.stderr.write('Repeat variable names in factory function.')
    };

    depCollection = [];

    var id, param, varname, el, i;
    for (i = 0; i < matchDeps.length; i++) {
      id = matchDeps[i];
      param = factoryNode && factoryNode.params[i];
      varname = param ? param.name : null;
      depCollection.push([id, varname]);

      if (selectedVar || selectedId) {
        continue;
      }

      // match selection to parameter
      if (param && shared.nodeContainsSelection(param, selection)) {
        selectedVar = param.name;
        continue;
      }

      // match selection to array element
      el = depArrayNode && depArrayNode.elements[i];
      if (el && shared.nodeContainsSelection(el, selection, true)) {
        selectedId = el.value;
      }
    };

    return process.stdout.write(JSON.stringify({
      'node': matchNode,
      'collection': depCollection,
      'id': selectedId,
      'var': selectedVar
    }));
  });
});
