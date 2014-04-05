import os
import re
from contextlib import contextmanager


# matches all strings enclosed in quotation marks
# string_pattern = r"""
#     (?P<quote>['"])                 # opening quote (single or double)
#     (?P<string>.+)?                 # lazy repeat--allows multiple captures
#     (?<!\\)(?P=quote)               # unescaped closing quote (of same type)
# """
string_pattern = r"""(?P<quote>['"])(?P<string>.+)?(?<!\\)(?P=quote)"""

multiline_comment_pattern = r'/\*(?:[^*]|\*[^/])*\*/'

singleline_comment_pattern = r'//.*$'

# matches //single-line or */multiple-line*/ javascript comments
comment_pattern = r'({multiline_comment_pattern})|({singleline_comment_pattern})'.format(**locals())
# comment_regex = re.compile(comment_pattern, re.VERBOSE + re.MULTILINE)

noninterpreted_pattern = r"""
    (?:\s|(?:{comment_pattern}))
""".format(**locals())

pragma_pattern = r"""
    ^//>>                           # comment and pragma start
    (?P<type>include|exclude)       # include or exclude
    (?P<action>Start|End)\s*?       # start or end
    \(\s*?{string_pattern}\s*?      # pragma's key
    (,.+?)?\);$                     # optional second parameter
""".format(**locals())

define_pattern = r'\bdefine(\s|{comment_pattern})*\('.format(**locals())
# define_regex = re.compile(define_pattern, re.MULTILINE)

array_pattern = r'\[(\s|{comment_pattern})*.*?\]'.format(**locals())

function_pattern = r'(?:\s|{comment_pattern})*?function\s*\('.format(**locals())

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
#     ^{noninterpreted_pattern}     # beginning of line + whitespace
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
# """.format(**locals()), re.MULTILINE | re.VERBOSE)

# define_mods_regex = re.compile(r"""

# """, re.VERBOSE|re.MULTILINE)


@contextmanager
def chdir(dirname=None):
    curdir = os.getcwd()
    os.chdir(dirname)
    try:
        yield
    finally:
        os.chdir(curdir)


def is_accessible_file(filepath, mode=os.R_OK):
    return os.path.isfile(filepath) and os.access(filepath, mode)


def which(program):
    mode = os.X_OK
    filepath, filename = os.path.split(program)

    if filepath:
        if is_accessible_file(program, mode):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_accessible_file(exe_file, mode):
                return exe_file
    return None
