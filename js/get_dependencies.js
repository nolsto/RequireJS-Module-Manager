#!/usr/bin/env node

var shared = require('shared')
  , args = process.argv.slice(2)
  , requirejs = require(args[0])
  , contents = args[1]
  , selection = (args[2].split(',')).map(function (n) {
    return parseInt(n, 10);
  })
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

    depArrayNode = shared.getDepArrayNode(matchNode);
    factoryNode = shared.getFactoryNode(matchNode);
    depCollection = {};

    var id, param, element, i;
    for (i = 0; i < matchDeps.length; i++) {
      id = matchDeps[i];
      param = factoryNode && factoryNode.params[i];
      depCollection[id] = param ? param.name : null;

      if (selectedVar || selectedId) {
        continue;
      }

      // match selection to parameter
      if (param && shared.nodeContainsSelection(param, selection)) {
        selectedVar = param.name;
        continue;
      }

      // match selection to array element
      element = depArrayNode && depArrayNode.elements[i];
      if (element && shared.nodeContainsSelection(element, selection, true)) {
        selectedId = element.value;
      }
    };

    process.stdout.write(JSON.stringify({
      'collection': depCollection,
      'node': matchNode,
      'id': selectedId,
      'var': selectedVar
    }));
  });
});
