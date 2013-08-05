import re


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

comment_regex = re.compile(r"""
    (^)?                # beginning of line
    [^\S\n]*            # match any whitespace character except newline
    /(?:\*(.*?)\*/      # captures multiline comment content
    [^\S\n]*            # match any whitespace character except newline
    |
    /[^\n]*             # matches single-line comment
    )                   # end comment content capture
    ($)?                # end of line
""", re.DOTALL | re.MULTILINE | re.VERBOSE)

define_template_regex = re.compile(r"""
    ^define\s*\(\s*               # define invocation
    \[\s*                         # module arrary opening bracket
    (?P<mods>((?P<quote>['"])     # the captured opening quote: ' or "
    {{module}}                    # the module item
    (?<!\\)(?P=quote)(?:,\s*)?)+) # closing quote from above that is not preceded by backslash
    \s*\],\s*                     # closing bracket
    function\s*\(\s*              # function definition
    (?P<args>(                    # function args opening paren
    {{name}}                      # the module argument name
    (?:,\s*)?)+)                  # function args closing paren
    \s*\)\s*{\s*                  # function block begin
    {{script}}                    # everything in-between
    \s*}\s*\)                     # end function definition
""", re.VERBOSE)

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

# define_mods_regex = re.compile(r"""

# """, re.VERBOSE|re.MULTILINE)


def flatten(string_list):
    return '\n'.join(string_list)


class Template:
    """docstring for Template"""

    def __init__(self, string_list):
        self.string = flatten(string_list)

    @property
    def string(self):
        return self.string

    def validate(self):
        match = define_template_regex.search(self.string)
        # print '<Match: %r, groups=%r>' % (match.group(), match.groups())
        # print match.group('quote')
        # print match.group('mods')
        # print match.group('args')
        # print match.groups()
        return match is not None

    def parse(self, string_input):
        match = parse_define_regex.search(string_input)
        return match

