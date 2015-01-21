#!/usr/bin/env node

var fs = require('fs')
  , args = process.argv.slice(2)
  , requirejs = require(args[0])
  , filename = args[1];

requirejs.tools.useLib(function (require) {
  require(['parse'], function (parse) {
    var config = {}
      , contents = fs.readFileSync(filename, 'utf8');

    config = parse.findConfig(contents).config;
    if (config === undefined) {
      process.exit(1);
    };

    console.log(JSON.stringify(config));
  });
});
