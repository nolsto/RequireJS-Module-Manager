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
  , depTemplate = args[5]
  , commentPattern = /\s*\/\/.*$/mg
  , multiCommentPattern = /\s*\/\*(?:[^*]|\*[^\/])*\*\//mg;

function sanitizeSep (str) {
  var result = str.replace(multiCommentPattern, '');
  return result.replace(commentPattern, '');
}

function sliceFrom (begin, end) {
  var str = depTemplate.slice(begin, end);
  // TODO add indentation to beginning of line
  // return str.replace(/\n/g, '\n    ');
  return str;
}

requirejs.tools.useLib(function (require) {
  require(['esprimaAdapter', 'parse'], function (esprima, parse) {
    var resultContents = contents
      , depArrayNode
      , factoryNode
      , paramNames
      , template;

    function parseDepTemplate () {
      var ast = esprima.parse(depTemplate, {range: true, loc: true, raw: true})
        , indent = matchNode.loc.start.column
        , result = {array: {}, func: {}}
        , childProp
        , errorMsg = 'Dependency template must contain an array argument with ' +
                     'two elements and a function argument with two parameters';

      parse.traverse(ast, function (node) {
        if (!result['sep'] && node.type === 'SequenceExpression') {
          childProp = 'expressions';
          try {
            result.prefix = sliceFrom(1, node[childProp][0].range[0]);
            result.suffix = sliceFrom(node[childProp][1].range[1], -1);
            result.sep = sliceFrom(node[childProp][0].range[1], node[childProp][1].range[0]);
          } catch (e) {
            throw errorMsg;
          }
        } else if (!result['sep'] && node.type === 'CallExpression') {
          childProp = 'arguments';
          try {
            result.prefix = sliceFrom(1, node[childProp][0].range[0]);
            result.suffix = sliceFrom(node[childProp][1].range[1], -1);
            result.sep = sliceFrom(node[childProp][0].range[1], node[childProp][1].range[0]);
          } catch (e) {
            throw errorMsg;
          }
        } else if (!result['node'] && node.type === 'Literal') {
          result.quote = node.raw[0];
        } else if (!result.array['sep'] && node.type === 'ArrayExpression') {
          childProp = 'elements';
          try {
            result.array.prefix = sliceFrom(node.range[0], node[childProp][0].range[0]);
            result.array.suffix = sliceFrom(node[childProp][1].range[1], node.range[1]);
            result.array.sep = sliceFrom(node[childProp][0].range[1], node[childProp][1].range[0]);
          } catch (e) {
            throw errorMsg;
          }
        } else if (!result.func['sep'] && node.type === 'FunctionExpression') {
          childProp = 'params';
          try {
            result.func.prefix = sliceFrom(node.range[0], node[childProp][0].range[0]);
            result.func.suffix = sliceFrom(node[childProp][1].range[1], node.range[1]);
            result.func.sep = sliceFrom(node[childProp][0].range[1], node[childProp][1].range[0]);
          } catch (e) {
            throw errorMsg;
          }
        }
        return !(result['prefix'] && result['suffix'] && result['quote'] &&
          result.array['prefix'] && result.array['suffix'] && result.array['sep'] &&
          result.func['prefix'] && result.func['suffix'] && result.func['sep']);
      });

      return result;
    }

    factoryNode = shared.getFactoryNode(matchNode);
    if (factoryNode) {
      paramNames = factoryNode.params.map(function (el) {
        return el.name
      });

      // replace changed variable names
      varChanges.forEach(function (el) {
        var index = paramNames.indexOf(el[0])
          , range = factoryNode.params[index].range
          , astRoot = esprima.parse(resultContents, {range: true, loc: true})
          , astContext = new esrefactor.Context(resultContents, astRoot)
          , id = astContext.identify(range[0]);

        // there's no actual references, only the declaration in the params
        if (!id.references.length) {
          return;
        }

        // this will always be the param and we don't want to replace that.
        // point it to the first reference instead and get rid of the declaration
        id.identifier.range = id.references[0].range;
        delete id.declaration;

        resultContents = astContext.rename(id, el[1]);
      });
    } else {
      template = parseDepTemplate();
      console.log(template);
      console.log(matchNode.loc.start.line);

      if (true) {};
    }

    // if there is no factory function present,
    //   parse template for argument separator
    //   generate string of arguments
    //   splice string into copy of function template
    // if there's only one argument in the factory function,
    //   parse template for argument separator
    //   generate string of arguments
    //   get range of the argument
    //   splice string into the contents, replacing the argument


    console.log(depTemplate);
    // console.log(resultContents);
    // console.log(result.slice(0, set[i][0]));

    // console.log(util.inspect(matchNode, options));
    // console.log(util.inspect(depCollection, options));
    // console.log(util.inspect(varChanges, options));

    // depArrayNode = shared.getDepArrayNode(matchNode);

    // var i;
    // for (i = 0; i < varChanges.length; i++) {
    //   Things[i]
    // };


    // console.log(result);
    // console.log(util.inspect(id, options));
  });
});
