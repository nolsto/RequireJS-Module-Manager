import unittest

from template import Template


class TemplatesTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_flattens_strings_list(self):
        string_list = [
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
        ]
        template = Template(string_list)
        template_string = "define([\n    '{{module_a}}',\n    '{{module_b}}',\n    '{{module_c}}'\n], function(\n    {{name_a}},\n    {{name_b}}\n) {\n    {{script}}\n});"

        self.assertEqual(template_string, template.string)

    def test_single_line_template_passes_regex(self):
        string_list = [
            r"define(['module_a', '/path/to/mo\'dule_b', '!text/module_c.hbs'], function(name_a, name_b) {",
            "    script",
            "});"
        ]
        template = Template(string_list)

        self.assertTrue(template.validate())

    def test_split_args_template_passes_regex(self):
        string_list = [
            "define(",
            "    ['module_a', '/path/to/module_b', '!text/module_c.hbs'],",
            "    function(name_a, name_b) {",
            "        script",
            "    }",
            ");"
        ]
        template = Template(string_list)

        self.assertTrue(template.validate())

    def test_stacked_template_passes_regex(self):
        string_list = [
            "define([",
            "    'module_a',",
            "    '/path/to/module_b',",
            "    '!text/module_c.hbs'",
            "], function(",
            "    name_a,",
            "    name_b",
            ") {",
            "    script",
            "});"
        ]
        template = Template(string_list)

        self.assertTrue(template.validate())


if __name__ == '__main__':
    unittest.main()
