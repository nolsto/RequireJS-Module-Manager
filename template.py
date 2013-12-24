import os
import re

from sublime import packages_path


snippet_content_regex = re.compile(r"""
    <content>\s*?                   # opening content tag
    <!\[CDATA\[\n                   # CDATA tag
    (?P<content>.+?)                # the template content itself
    (?=\n\]\]>\s*?                  # begin lookahead to CDATA tag close
    <\/content>)                    # end lookahead on content tag close
""", re.VERBOSE | re.DOTALL)


template_regex = re.compile(r"""
    ^(?P<frag1>.+?)

    \[
    (?P<path_newline>\n)?           # new line if it exists before paths
    (?P<path_indent>(?<=\n)\s\s*?)? # whitespace if it exists before path
    (?P<quote>['"])                 # opening quote: single or double quote
    (?P<path>\${\d:                 # beginning of token and path group
    \$PATH_PLACEHOLDER              # module path environment variable name
    })                              # end of token and group
    (?<!\\)                         # prevent ending token on escaped quote
    (?P=quote)                      # closing quote: same as captured type
    \]

    (?P<frag2>.+?)

    (?P<var_newline>\n)?            # new line if it exists before vars
    (?P<var_indent>(?<=\n)\s\s*?)?  # whitespace if it exists before vars
    (?P<var>\${\d:                  # beginning of token and vars group
    \$VAR_PLACEHOLDER               # module variable environment variable name
    })                              # end of token and group

    (?P<frag3>.+?)

    (?P<text_newline>\n)?           # new line if it exists before text
    (?P<text_indent>(?<=\n)\s\s*?)? # whitespace if it exists before text
    (?P<text>\${\d:                 # beginning of token and selectedtext group
    \$TM_SELECTED_TEXT              # selected text environment variable
    })                              # end of token and group

    (?P<frag4>.+)$
""", re.VERBOSE | re.DOTALL)


class Template:
    """docstring for Template"""

    def __init__(self, snippet_path):
        # folder is the first folder listed in the project side bar.
        # config is either the requirejs config json object,
        # or a path to a json file to be used as the requirejs config.
        folder = packages_path()
        snippet_file = os.path.join(folder, snippet_path)
        try:
            f = open(snippet_file)
            snippet = f.read()
        except IOError, e:
            raise Exception("'%s' snippet file does not exist" % (snippet_file))

        self.parse(snippet)


    def parse(self, snippet):
        content = snippet_content_regex.search(snippet).group('content')
        self.groups = template_regex.search(content).groupdict()
        # print self.groups
        # match = define_template_regex.search(self.string)
        # print '<Match: %r, groups=%r>' % (match.group(), match.groups())
        # print match.group('quote')
        # print match.group('mods')
        # print match.group('args')
        # print match.groups()
        # return match is not None
        return True

