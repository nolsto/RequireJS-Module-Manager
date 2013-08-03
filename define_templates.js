// AMD split resources and arguments on lines
define([
    'module_id',
    'path/to/other_module',
    'another_module_id'
], function(
    module,
    otherModule
) {
    {{script}}
});

// AMD split array and function on lines
define(
    ['module_id', 'path/to/other_module', 'another_module_id'],
    function(module, otherModule) {
        {{script}}
    }
);

// AMD single-line define
define(['module_id', 'path/to/other_module', 'another_module_id'], function(module, otherModule) {
    {{script}}
});

// CommonJS
define(function (require) {
    var module = require('module_id');
    var otherModule = require('path/to/other_module');
    require('another_module_id');

    {{script}}
});
