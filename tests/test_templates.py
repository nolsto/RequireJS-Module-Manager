import unittest

from template import get_content_from_snippet, \
                     replace_tokens_in_snippet_content, \
                     Template


class TemplatesTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_finds_content(self):
        snippet = """<snippet>
    <content><![CDATA[
define(${1:}['${2:$TM_MODULE_PATH_PLACEHOLDER}'], function(${3:$TM_MODULE_NAME_PLACEHOLDER}) {
    ${0:$TM_SELECTED_TEXT}
});
]]></content>
    <tabTrigger>define</tabTrigger>
    <scope>source.js</scope>
    <description>define (AMD single line)</description>
</snippet>"""

        snippet_content = """define(${1:}['${2:$TM_MODULE_PATH_PLACEHOLDER}'], function(${3:$TM_MODULE_NAME_PLACEHOLDER}) {
    ${0:$TM_SELECTED_TEXT}
});"""

        self.assertEqual(get_content_from_snippet(snippet), snippet_content)

    def test_replaces_tokens(self):
        snippet_content = """define(${1:}['${2:$TM_MODULE_PATH_PLACEHOLDER}'], function(${3:$TM_MODULE_NAME_PLACEHOLDER}) {
    ${0:$TM_SELECTED_TEXT}
});"""
        content = """define(${1:}[{{module}}], function(${3:$TM_MODULE_NAME_PLACEHOLDER}) {
    ${0:$TM_SELECTED_TEXT}
});"""

        self.assertEqual(replace_tokens_in_snippet_content(snippet_content), content)

    # def test_single_line_template_is_valid(self):
    #     string_list = [
    #         r"define(['module_a', '/path/to/mo\'dule_b', '!text/module_c.hbs'], function(name_a, name_b) {",
    #         "    script",
    #         "});"
    #     ]
    #     template = Template(string_list)

    #     self.assertTrue(template.validate())

    def test_single_line_template_is_valid(self):
        string = """
define(${1:}['${2:$TM_MODULE_PATH_PLACEHOLDER}'], function(${3:$TM_MODULE_NAME_PLACEHOLDER}) {
    ${0:$TM_SELECTED_TEXT}
});
"""
        template = Template(string)

        self.assertTrue(template.validate())

    def test_split_args_template_is_valid(self):
        # string_list = [
        #     "define(",
        #     "    ['{{module}}'],",
        #     "    function({{name}}) {",
        #     "        {{script}}",
        #     "    }",
        #     ");"
        # ]
        # template = Template(string_list)

        # self.assertTrue(template.validate())
        pass

    def test_stacked_template_is_valid(self):
        # string_list = [
        #     "define([",
        #     "    '{{module}}'",
        #     "], function(",
        #     "    {{name}}",
        #     ") {",
        #     "    {{script}}",
        #     "});"
        # ]
        # template = Template(string_list)

        # self.assertTrue(template.validate())
        pass

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

    # def test_parses_string_input(self):
    #     string_buffer = """define ([ "module_a", "path/to/module_b", "./module_c", "!text/module_d.hbs" ],
    #                 function (moduleA, _moduleB, $moduleC, moduleD) {

    #                 });
    #     """
    #     # print string_buffer
    #     # parse_define_regex.match(string_buffer)
    #     self.assertIsNotNone(parse_define_regex.match(string_buffer))


if __name__ == '__main__':
    unittest.main()
