{
    "templates":
    {
        "define_stacked": [
            "define([",
            "    '{{module_a}}',",
            "    '{{module_b}}',",
            "    '{{module_c}}'",
            "], function(",
            "    {{name_a}},",
            "    {{name_b}}",
            ") {",
            "    {{script}}",
            "});"
        ],
        "define_split_args": [
            "define(",
            "    ['{{module_a}}', '{{module_b}}', '{{module_c}}'],",
            "    function({{name_a}}, {{name_b}}) {",
            "        {{script}}",
            "    }",
            ");"
        ],
        "define_single_line": [
            "define(['{{module_a}}', '{{module_b}}', '{{module_c}}'], function({{name_a}}, {{name_b}}) {",
            "    {{script}}",
            "});"
        ],
        "define_commonjs": [
            "define(function (require) {",
            "    var {{name_a}} = require('{{module_a}}');",
            "    var {{name_b}} = require('{{module_b}}');",
            "    require('{{module_c}}');",
            "",
            "    {{script}}",
            "});"
        ]
    }
}
