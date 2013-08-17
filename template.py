import re

# fragments = {'frag1': 'define([',
#              'path_ind': None,
#              'quote': "'",
#              'path': '${2:$MODULE_PATH_PLACEHOLDER}',
#              'frag2': '], function(',
#              'name_ind': None,
#              'name': '${3:$MODULE_NAME_PLACEHOLDER}',
#              'frag3': ') {\n',
#              'text_ind': '    ',
#              'text': '${0:$TM_SELECTED_TEXT}',
#              'frag4': '\n});'}

parse_define_regex = re.compile(r"""
    ^[^\S\n]*                     # beginning of line + whitespace
    define\s*\(\s*                # define invocation
    \[\s*                         # module arrary opening bracket
    (?P<mods>((?P<quote>['"])     # the captured opening quote: ' or "
    .+                            # the module item
    (?<!\\)(?P=quote)(?:,\s*)?)+) # closing quote from above that is not preceded by backslash
    \s*\],\s*                     # closing bracket
    function\s*\(\s*              # function definition
    (?P<args>(                    # function args opening paren
    [a-zA-Z_$][0-9a-zA-Z_$]*      # the module argument name
    (?:,\s*)?)+)                  # function args closing paren
    \s*\)\s*{\s*                  # function block begin
    (?P<script>.+)?               # everything in-between
    \s*}\s*\)                     # end function definition
""", re.MULTILINE | re.VERBOSE)


class Template:
    """docstring for Template"""

    def __init__(self, fragments):
        self._fragments = fragments

    def is_found_in(self, script):
        # f = self._fragments
        # pattern = (f['frag1'], f['path_ind'], )
        # [re.escape(f) for f in self._fragments if ]
        return parse_define_regex.search(script)

    def validate(self):
        # match = define_template_regex.search(self.string)
        # print '<Match: %r, groups=%r>' % (match.group(), match.groups())
        # print match.group('quote')
        # print match.group('mods')
        # print match.group('args')
        # print match.groups()
        # return match is not None
        return True

