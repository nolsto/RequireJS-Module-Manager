import re


# matches all strings enclosed in quotation marks
string_pattern = r"""
    (?P<quote>['"])                 # opening quote (single or double)
    (?P<string>.+)?                 # lazy repeat--allows multiple captures
    (?<!\\)(?P=quote)               # unescaped closing quote (of same type)
"""

define_pattern = r"""
    [\s;]define\(                   # define invocation
    (?P<name>{string_pattern},)?    # optional explicit module name
    (?P<paths>{{paths}})            # path string that will be substituted
    ,function                       # function definition
    (?P<vars>\(.*\))                # function parameters
    {{                              # function block begin
    (?P<script>.+)?                 # everything in-between
    }}\)                            # end function definition
""".format(**locals())


# matches //single line or */multiple line*/ javascript comments
comment_pattern = r"""
    (/\*(?:[^*]|\*[^/])*\*/)|       # multi-line comment, or
    (//.*$)                         # single-line comment
"""
comment_regex = re.compile(comment_pattern, re.VERBOSE + re.MULTILINE)


nonstructural_pattern = r"""
    (?:\s|(?:{cmt}))*?
""".format(cmt=comment_pattern)


pragma_pattern = r"""
    ^//>>                           # comment and pragma start
    (?P<type>include|exclude)       # include or exclude
    (?P<action>Start|End)\s*?       # start or end
    \(\s*?{string_pattern}\s*?      # pragma's key
    (,.+?)?\);$                     # optional second parameter
""".format(**locals())


# path_regex = re.compile(r"""
#     (?P<pre>.*)?                    # content that exists before path string
#     (?P<paths>
#     {str}                #
#     ((?<=,){str})*?      #
#     )
#     (?P<post>.*)?                   # new line if it exists after path
# """.format(str=string_pattern), re.VERBOSE + re.DOTALL)



# matches a define function call with optional module name argument
# if it is at the end of the string.
# should be run after stripping js comments and whitespace
define_regex = re.compile(r'define\(((?P<name>%s),)?$' % (string_pattern), re.VERBOSE)

# matches a require function call.
# should be run after stripping js comments and whitespace
require_regex = re.compile(r'require\($')

# matches a define argument that is a function definition
# if it is at the beginning of the string.
# should be run after stripping js comments and whitespace
function_regex = re.compile(r'^,function\((?P<vars>.*?)\)')



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




def get_content_from_snippet(snippet):
    match = snippet_content_regex.search(snippet)
    return match.group('content')

def parse_snippet_content(string):
    match = parse_snippet_regex.search(string)
    return match.groupdict()
