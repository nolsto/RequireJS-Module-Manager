#!/usr/bin/env node

var args = process.argv.slice(2)
  , requirejs = require(args[0])
  , fs = require('fs');

requirejs.tools.useLib(function (require) {
  require(['parse'], function (parse) {
    var config = {}
      , filename = args[1]
      , contents = fs.readFileSync(filename, 'utf8');

    contents = fs.readFileSync(filename, 'utf8');
    config = parse.findConfig(contents).config;
    if (config === undefined) {
      process.exit(1);
    };

    console.log(JSON.stringify(config));
  });
});
