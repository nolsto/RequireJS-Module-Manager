import re
from pprint import pprint

# define_regex = re.compile(r"""
#     ^define\s*\(\s*               # define invocation
#     \[\s*                         # module arrary opening bracket
#     (?P<mods>((?P<quote>['"])     # the captured opening quote: ' or "
#     .+                            # the module item
#     (?<!\\)(?P=quote)(?:,\s*)?)+) # closing quote from above that is not preceded by backslash
#     \s*\],\s*                     # closing bracket
#     function\s*\(\s*              # function definition
#     (?P<args>(                    # function args opening paren
#     [a-zA-Z_$][0-9a-zA-Z_$]*      # the module argument name
#     (?:,\s*)?)+)                  # function args closing paren
#     \s*\)\s*{\s*                  # function block begin
#     (?P<script>.+)?               # everything in-between
#     \s*}\s*\)                     # end function definition
# """, re.VERBOSE)

# comment_regex = re.compile(r"""
#     (^)?                # beginning of line
#     [^\S\n]*            # match any whitespace character except newline
#     /(?:\*(.*?)\*/      # captures multiline comment content
#     [^\S\n]*            # match any whitespace character except newline
#     |
#     /[^\n]*             # matches single-line comment
#     )                   # end comment content capture
#     ($)?                # end of line
# """, re.DOTALL | re.MULTILINE | re.VERBOSE)

# define_template_regex = re.compile(r"""
#     ^define\s*\(\s*               # define invocation
#     \[\s*                         # module arrary opening bracket
#     (?P<mods>((?P<quote>['"])     # the captured opening quote: ' or "
#     {{module}}                    # the module item
#     (?<!\\)(?P=quote)(?:,\s*)?)+) # closing quote from above that is not preceded by backslash
#     \s*\],\s*                     # closing bracket
#     function\s*\(\s*              # function definition
#     (?P<args>(                    # function args opening paren
#     {{name}}                      # the module argument name
#     (?:,\s*)?)+)                  # function args closing paren
#     \s*\)\s*{\s*                  # function block begin
#     {{script}}                    # everything in-between
#     \s*}\s*\)                     # end function definition
# """, re.VERBOSE)

# parse_define_regex = re.compile(r"""
#     ^[^\S\n]*                     # beginning of line + whitespace
#     define\s*\(\s*                # define invocation
#     \[\s*                         # module arrary opening bracket
#     (?P<mods>((?P<quote>['"])     # the captured opening quote: ' or "
#     .+                            # the module item
#     (?<!\\)(?P=quote)(?:,\s*)?)+) # closing quote from above that is not preceded by backslash
#     \s*\],\s*                     # closing bracket
#     function\s*\(\s*              # function definition
#     (?P<args>(                    # function args opening paren
#     [a-zA-Z_$][0-9a-zA-Z_$]*      # the module argument name
#     (?:,\s*)?)+)                  # function args closing paren
#     \s*\)\s*{\s*                  # function block begin
#     (?P<script>.+)?               # everything in-between
#     \s*}\s*\)                     # end function definition
# """, re.MULTILINE | re.VERBOSE)

# define_mods_regex = re.compile(r"""

# """, re.VERBOSE|re.MULTILINE)


snippet_content_regex = re.compile(r"""
    <content>\s*                    # opening content tag
    (?:<!\[CDATA\[)?(?:\n|\r\n?)?   # optional CDATA tag
    (?P<content>.+?)                # the template content itself
    (?=(?:(?:\n|\r\n?)?\]\]>)?\s*   # begin lookahead to optional CDATA close
    <\/content>)                    # end lookahead on content tag close
""", re.VERBOSE | re.DOTALL)

snippet_module_name_token_pattern = r"""(?P<name>\${\d:\$TM_MODULE_NAME_PLACEHOLDER})"""

snippet_module_path_token_pattern = \
    r"""(?P<openquote>['"])(?P<path>\${\d:\$TM_MODULE_PATH_PLACEHOLDER})(?P<endquote>(?P=openquote))"""

snippet_selected_text_token_pattern = r"""(?P<selectedtext>\${\d:\$TM_SELECTED_TEXT})"""

def get_content_from_snippet(snippet):
    match = snippet_content_regex.search(snippet)
    return match.group('content')

def replace_tokens_in_snippet_content(string):
    # repl = {'path': '{{path}}', 'name': '{{name}}'}
    regex = re.compile("%s(.+)%s(.+)%s" % (
        snippet_module_path_token_pattern,
        snippet_module_name_token_pattern,
        snippet_selected_text_token_pattern
    ), re.DOTALL)
    match = regex.search(string)

    print match.string[:match.start('path')]
    print match.string[match.start('path'):match.end('path')]
    print match.string[match.end('path'):match.start('name')]
    print match.string[match.start('name'):match.end('name')]
    print match.string[match.end('name'):match.start('selectedtext')]
    print match.string[match.start('selectedtext'):match.end('selectedtext')]
    print match.string[match.end('selectedtext'):]

    # print match.start(), match.end()
    # pprint(regex.split(string))
    # print regex.split(string)
    # print (match.group('path'), match.group('name'))
    return
    # return regex.sub('{{module}}', string)


class Template:
    """docstring for Template"""

    def __init__(self, string):
        self.string = string

    @property
    def string(self):
        return self.string

    def validate(self):
        # match = define_template_regex.search(self.string)
        # print '<Match: %r, groups=%r>' % (match.group(), match.groups())
        # print match.group('quote')
        # print match.group('mods')
        # print match.group('args')
        # print match.groups()
        # return match is not None
        return True

    def parse(self, string_input):
        # match = parse_define_regex.search(string_input)
        # return match
        pass

