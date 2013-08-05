import unittest

from template import Template
from template import parse_define_regex


class TemplatesTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_flattens_strings_list(self):
        string_list = [
            "define([",
            "    '{{module}}'",
            "], function(",
            "    {{name}}",
            ") {",
            "    {{script}}",
            "});"
        ]
        template = Template(string_list)
        template_string = "define([\n    '{{module}}'\n], function(\n    {{name}}\n) {\n    {{script}}\n});"

        self.assertEqual(template_string, template.string)

    # def test_single_line_template_is_valid(self):
    #     string_list = [
    #         r"define(['module_a', '/path/to/mo\'dule_b', '!text/module_c.hbs'], function(name_a, name_b) {",
    #         "    script",
    #         "});"
    #     ]
    #     template = Template(string_list)

    #     self.assertTrue(template.validate())

    def test_single_line_template_is_valid(self):
        string_list = [
            "define(['{{module}}'], function({{name}}) {",
            "    {{script}}",
            "});"
        ]
        template = Template(string_list)

        self.assertTrue(template.validate())

    def test_split_args_template_is_valid(self):
        string_list = [
            "define(",
            "    ['{{module}}'],",
            "    function({{name}}) {",
            "        {{script}}",
            "    }",
            ");"
        ]
        template = Template(string_list)

        self.assertTrue(template.validate())

    def test_stacked_template_is_valid(self):
        string_list = [
            "define([",
            "    '{{module}}'",
            "], function(",
            "    {{name}}",
            ") {",
            "    {{script}}",
            "});"
        ]
        template = Template(string_list)

        self.assertTrue(template.validate())

    # def test_commonjs_template_is_valid(self):
    #     string_list = [
    #         "define(function (require) {",
    #         "    var {{name}} = require('{{module}}');",
    #         "",
    #         "    {{script}}",
    #         "});"
    #     ]
    #     template = Template(string_list)

    #     self.assertTrue(template.validate())

    def test_parses_string_input(self):
        string_buffer = """define ([ "module_a", "path/to/module_b", "./module_c", "!text/module_d.hbs" ],
                    function (moduleA, _moduleB, $moduleC, moduleD) {

                    });
        """
        # print string_buffer
        # parse_define_regex.match(string_buffer)
        self.assertIsNotNone(parse_define_regex.match(string_buffer))


if __name__ == '__main__':
    unittest.main()
