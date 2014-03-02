var requirejs = require('./tests/cases/tools/r.js')
  , fs = require('fs');

requirejs.tools.useLib(function (require) {
  require(['parse'], function (parse) {
    var out = {}
      , fileName = process.argv[2]
      , contents = fs.readFileSync(fileName, 'utf8');

    out = parse(fileName, fileName, contents);
    console.log('parse', '\n' + JSON.stringify(out), '\n');

    out = parse.usesAmdOrRequireJs(fileName, contents);
    console.log('parse.usesAmdOrRequireJs', '\n' + JSON.stringify(out), '\n');

    out = parse.usesCommonJs(fileName, contents);
    console.log('parse.usesCommonJs', '\n' + JSON.stringify(out), '\n');

    out = parse.findDependencies(fileName, contents);
    console.log('parse.findDependencies', '\n' + JSON.stringify(out, null, '  '), '\n');

    out = parse.getAnonDeps(fileName, contents);
    console.log('parse.getAnonDeps', '\n' + JSON.stringify(out, null, '  '), '\n');

    out = parse.findCjsDependencies(fileName, contents);
    console.log('parse.findCjsDependencies', '\n' + JSON.stringify(out, null, '  '), '\n');

    fileName = './tests/cases/www/js/app.js';
    contents = fs.readFileSync(fileName, 'utf8');
    out = parse.findConfig(contents);
    console.log('parse.findConfig', '\n' + JSON.stringify(out, null, '  '), '\n');
  });
});
