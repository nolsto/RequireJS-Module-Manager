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
    (?:<!\[CDATA\[)?(?:\n?)?        # optional CDATA tag
    (?P<content>.+?)                # the template content itself
    (?=(?:(?:\n?)?\]\]>)?\s*        # begin lookahead to optional CDATA close
    <\/content>)                    # end lookahead on content tag close
""", re.VERBOSE | re.DOTALL)

snippet_unrelated_token_regex = re.compile(r"""
    (\${\d:                         # beginning of the token and group
    (?!                             # begin negative lookahead with:
    (?:\$MODULE_PATH_PLACEHOLDER)|  # path token,
    (?:\$MODULE_NAME_PLACEHOLDER)|  # or name token,
    (?:\$TM_SELECTED_TEXT)          # or selected text token.
    )})                             # end negative lookahead, token and group
""", re.VERBOSE | re.MULTILINE)

parse_snippet_regex = re.compile(r"""
    ^(?P<frag1>.+?)

    (?P<path_ind>(?<=[\n])\s\s*?)?  # whitespace if it exists before path
    (?P<quote>['"])                 # opening quote: single or double quote
    (?P<path>\${\d:                 # beginning of token and path group
    \$MODULE_PATH_PLACEHOLDER       # module path environment variable name
    })                              # end of token and group
    (?<!\\)                         # prevent ending token on escaped quote
    (?P=quote)                      # closing quote: same as captured type

    (?P<frag2>.+?)

    (?P<name_ind>(?<=[\n])\s\s*?)?  # whitespace if it exists before name
    (?P<name>\${\d:                 # beginning of token and name group
    \$MODULE_NAME_PLACEHOLDER       # module name environment variable name
    })                              # end of token and group

    (?P<frag3>.+?)

    (?P<text_ind>(?<=[\n])\s\s*?)?  # whitespace if it exists before text
    (?P<text>\${\d:                 # beginning of token and selectedtext group
    \$TM_SELECTED_TEXT              # selected text environment variable
    })                              # end of token and group

    (?P<frag4>.+)$
""", re.VERBOSE | re.DOTALL)


def get_content_from_snippet(snippet):
    match = snippet_content_regex.search(snippet)
    return match.group('content')

def remove_unrelated_tokens_in_snippet_content(string):
    return snippet_unrelated_token_regex.sub('', string)

def parse_snippet_content(string):
    match = parse_snippet_regex.search(string)
    return match.groupdict()
