import unittest

from template import Template
from util import get_content_from_snippet, \
                 remove_unrelated_tokens_in_snippet_content, \
                 parse_snippet_content


class TemplatesTest(unittest.TestCase):

    def setUp(self):
        pass


    def test_finds_content(self):
        snippet = """<snippet>
    <content><![CDATA[
define(${1:}['${2:$MODULE_PATH_PLACEHOLDER}'], function(${3:$MODULE_NAME_PLACEHOLDER}) {
    ${0:$TM_SELECTED_TEXT}
});
]]></content>
    <tabTrigger>define</tabTrigger>
    <scope>source.js</scope>
    <description>define (AMD single line)</description>
</snippet>"""

        snippet_content = """define(${1:}['${2:$MODULE_PATH_PLACEHOLDER}'], function(${3:$MODULE_NAME_PLACEHOLDER}) {
    ${0:$TM_SELECTED_TEXT}
});"""

        self.assertEqual(get_content_from_snippet(snippet), snippet_content)


    def test_removes_unrelated_tokens(self):
        snippet_content = """define(${1:}['${2:$MODULE_PATH_PLACEHOLDER}'], function(${3:$MODULE_NAME_PLACEHOLDER}) {
    ${0:$TM_SELECTED_TEXT}
});"""
        content = """define(['${2:$MODULE_PATH_PLACEHOLDER}'], function(${3:$MODULE_NAME_PLACEHOLDER}) {
    ${0:$TM_SELECTED_TEXT}
});"""

        self.assertEqual(remove_unrelated_tokens_in_snippet_content(snippet_content), content)


    def test_replaces_tokens(self):
        snippet_content = """define(['${2:$MODULE_PATH_PLACEHOLDER}'], function(${3:$MODULE_NAME_PLACEHOLDER}) {
    ${0:$TM_SELECTED_TEXT}
});"""
        content = {'frag1': 'define([',
                   'path_ind': None,
                   'quote': "'",
                   'path': '${2:$MODULE_PATH_PLACEHOLDER}',
                   'frag2': '], function(',
                   'name_ind': None,
                   'name': '${3:$MODULE_NAME_PLACEHOLDER}',
                   'frag3': ') {\n',
                   'text_ind': '    ',
                   'text': '${0:$TM_SELECTED_TEXT}',
                   'frag4': '\n});'}

        self.assertDictEqual(parse_snippet_content(snippet_content), content)


    def test_replaces_tokens_2(self):
        snippet_content = """define([ '${2:$MODULE_PATH_PLACEHOLDER}' ], function( ${3:$MODULE_NAME_PLACEHOLDER} ) {
    ${0:$TM_SELECTED_TEXT}
});"""
        content = {'frag1': 'define([ ',
                   'path_ind': None,
                   'quote': "'",
                   'path': '${2:$MODULE_PATH_PLACEHOLDER}',
                   'frag2': ' ], function( ',
                   'name_ind': None,
                   'name': '${3:$MODULE_NAME_PLACEHOLDER}',
                   'frag3': ' ) {\n',
                   'text_ind': '    ',
                   'text': '${0:$TM_SELECTED_TEXT}',
                   'frag4': '\n});'}

        self.assertDictEqual(parse_snippet_content(snippet_content), content)


    def test_replaces_tokens_3(self):
        snippet_content = """define([
    '${2:$MODULE_PATH_PLACEHOLDER}'
], function(
    ${3:$MODULE_NAME_PLACEHOLDER}
) {
    ${0:$TM_SELECTED_TEXT}
});"""
        content = {'frag1': 'define([\n',
                   'path_ind': '    ',
                   'quote': "'",
                   'path': '${2:$MODULE_PATH_PLACEHOLDER}',
                   'frag2': '\n], function(\n',
                   'name_ind': '    ',
                   'name': '${3:$MODULE_NAME_PLACEHOLDER}',
                   'frag3': '\n) {\n',
                   'text_ind': '    ',
                   'text': '${0:$TM_SELECTED_TEXT}',
                   'frag4': '\n});'}

        self.assertDictEqual(parse_snippet_content(snippet_content), content)


    def test_replaces_tokens_4(self):
        snippet_content = """define (
[
    '${2:$MODULE_PATH_PLACEHOLDER}'
],
function (
    ${3:$MODULE_NAME_PLACEHOLDER}
)
{
    ${0:$TM_SELECTED_TEXT}
}
);"""
        content = {'frag1': 'define (\n[\n',
                   'path_ind': '    ',
                   'quote': "'",
                   'path': '${2:$MODULE_PATH_PLACEHOLDER}',
                   'frag2': '\n],\nfunction (\n',
                   'name_ind': '    ',
                   'name': '${3:$MODULE_NAME_PLACEHOLDER}',
                   'frag3': '\n)\n{\n',
                   'text_ind': '    ',
                   'text': '${0:$TM_SELECTED_TEXT}',
                   'frag4': '\n}\n);'}

        self.assertDictEqual(parse_snippet_content(snippet_content), content)

    def test_is_found_in_script(self):
        fragments = {'frag1': 'define([',
                     'path_ind': None,
                     'quote': "'",
                     'path': '${2:$MODULE_PATH_PLACEHOLDER}',
                     'frag2': '], function(',
                     'name_ind': None,
                     'name': '${3:$MODULE_NAME_PLACEHOLDER}',
                     'frag3': ') {\n',
                     'text_ind': '    ',
                     'text': '${0:$TM_SELECTED_TEXT}',
                     'frag4': '\n});'}
        script = """
define(['path/to/module'], function(module) {
    // rest of the code here
    module.doSomething();
});
"""
        template = Template(fragments)

        self.assertTrue(template.is_found_in(script))


    def test_split_args_template_is_valid(self):
        pass


    def test_stacked_template_is_valid(self):
        pass


    def test_commonjs_template_is_valid(self):
        pass


if __name__ == '__main__':
    unittest.main()
