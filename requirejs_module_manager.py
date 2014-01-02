import os
import re
from itertools import izip_longest

from sublime import load_settings, MONOSPACE_FONT, Region
from sublime_plugin import WindowCommand

from module_collection import ModuleCollection
from template import Template
from util import comment_regex, define_regex, function_regex


settings_filename = 'RequireJS Module Manager.sublime-settings'
# Load the settings file for this plugin
settings = load_settings(settings_filename)


class AddRequirejsModuleDependencyCommand(WindowCommand):

    def run(self):
        # active view (area that contains the text buffer)
        self.view = self.window.active_view()

        try:
            # first folder in the project
            folder = self.window.folders()[0]
        except Exception as e:
            raise Exception('RequireJS Module Manager requires a project with at least one folder')

        # self.define_template = Template(self.get_setting('define_template'))

        self.module_collection = ModuleCollection(folder, self.get_setting('requirejs_config'))

        self.items = ['> Input module path...'] + self.module_collection.ids

        self.capture()


    def get_setting(self, prop):
        """Load the property

        First attempts to lookup property in the project settings.
        If it doesn't exist, fall back to plugin's settings property.
        """
        return self.view.settings().get(prop, settings.get(prop))


    def capture(self):
        # get cursor position or span of selection
        return_region = self.view.sel()[0]
        region = return_region

        while True:
            # find the syntax scope of the selected region
            (begin_bracket, end_bracket) = (
                self.view.score_selector(region.begin(), 'meta.brace.square'),
                self.view.score_selector(region.end() - 1, 'meta.brace.square')
            )
            if begin_bracket and end_bracket:
                # the selection is an array
                while True:
                    break

                break

            # expand the selection's scope
            self.view.run_command('expand_selection', {'to': 'brackets'})
            # get the new selected region
            new_region = self.view.sel()[0]

            if new_region == region:
                # if the new selection is the same as the old one,
                # there are no outer brackets and we need to stop looping
                break

            # set the region to the new region with increased scope and loop
            region = new_region

        # paths = comment_regex.sub('', self.view.substr(region))
        # print paths

        # string = self.view.substr(Region(0, region.begin()))
        # simple_string = self._simplify_js_string(string)
        # module_name = define_regex.search(simple_string).group('name')

        # string = self.view.substr(Region(region.begin() + 1, region.end() - 1))
        # deps_paths_string = self._simplify_js_string(string)
        # deps_paths = deps_paths_string.split(',')

        # string = self.view.substr(Region(region.end(), self.view.size()))
        # simple_string = self._simplify_js_string(string)
        # deps_vars_string = function_regex.search(simple_string).group('vars')
        # deps_vars = deps_vars_string.split(',')

        # deps_map = izip_longest(deps_paths, deps_vars)

        # out = u''
        # for (k, v) in deps_map:
        #     string = u'{path_newline}{path_indent}{k},'.format(**dict(self.define_template.groups, **locals()))
        #     out += string
        # out = '[%s]' % out
        # print out

        # {'frag1': 'define(${1:}[',
        #  'frag2': '\n], function(',
        #  'frag3': '\n) {',
        #  'frag4': '\n});',
        #  'path': '${2:$PATH_PLACEHOLDER}',
        #  'path_indent': '\t',
        #  'path_newline': '\n',
        #  'quote': "'",
        #  'text': '${0:$TM_SELECTED_TEXT}',
        #  'text_indent': '\t',
        #  'text_newline': '\n',
        #  'var': '${3:$VAR_PLACEHOLDER}',
        #  'var_indent': '\t',
        #  'var_newline': '\n'}



        try:
            pass
        except Exception, e:
            raise
        else:
            pass
        finally:
            # clear regions and add back the original
            # TODO: the cursor is still visually in the wrong place if no actions
            # are taken though
            # self.view.sel().clear()
            # self.view.sel().add(return_region)
            # self.view.show(return_region)
            pass


    def is_define_array(self, region):
        string = self.view.substr(Region(0, region.begin()))
        simple_string = self._simplify_js_string(string)

        if not define_regex.search(simple_string):
            return False

        return True


    def contains_define_function(self, region):
        string = self.view.substr(Region(region.end(), self.view.size()))
        string = self._simplify_js_string(string)

        if not function_regex.search(string):
            return False

        return True

        # self.view.run_command('move', {'by': 'subword_ends',
        #                                'forward': True,
        #                                'extend': True})
        # region = self.view.sel()[0]
        # selection = self.view.substr(region)

        # if selection != 'define':
        #     return False


        # self.window.show_quick_panel(self.items,
        #                              self.handle_path_panel_response,
        #                              sublime.MONOSPACE_FONT, 0)


    def extract_from_args(self, region):
        # TODO:
        # Look for `require` to left of the args
        # parse arguments and exit if the returned is not a single string
        # look for `var = ` to left of `require`
        # Create key-value pair with variable name and argument string
        # show quick response panel with added items above

        self.window.show_quick_panel(self.items,
                                     self.handle_path_panel_response,
                                     sublime.MONOSPACE_FONT, 0)

        return region

    def _simplify_js_string(self, string):
        return re.sub(r'\s', '', comment_regex.sub('', string))


    def _char_is_whitespace(self, point):
        if re.match(r'\s', self.view.substr(point)):
            return True


    def _scope_region(self, point, scope):
        if self.view.score_selector(point, scope):
            return self.view.extract_scope(point)


    def handle_path_panel_response(self, index):
        if index is -1:
            return
        if index is 0:
            self.window.show_input_panel('Path to module:', '',
                                         self.handle_id_or_resource_input,
                                         None, None)
            return
        module_id = self.module_collection.ids[index - 1]
        (module_varname, ext) = os.path.splitext(os.path.basename(module_id))
        self.handle_id_or_resource_input(module_id, module_varname)


    def handle_name_panel_response(self, index):
        if index is -1:
            return
        if index is 0:
            self.window.show_input_panel("Module's variable name:", '',
                                         self.handle_id_or_resource_input,
                                         None, None)
            return
        # module_id = self.module_collection.ids[index - 1]
        # (module_varname, ext) = os.path.splitext(os.path.basename(module_id))
        # self.handle_id_or_resource_input(module_id, module_varname)
        # search = 'poo'
        # edit = self.view.begin_edit()
        # self.window.run_command('show_overlay', {'overlay': 'goto',
        #                                          'text': '@%s' % search})
        # self.view.run_command('insert_snippet',
        #                       {"name": "Packages/User/console-log.sublime-snippet"})
        # self.view.run_command('example')
        # self.view.end_edit(edit)


    def handle_id_or_resource_input(self, input, varname=''):
        self.window.show_input_panel('Module variable name:', varname,
                                     self.handle_varname_input, None, None)
        print 'id/resource: ', input


    def handle_varname_input(self, input):
        print 'varname: ', input
        # self.create_define_enclosure()


    # def create_define_enclosure(self):
    #     edit = self.view.begin_edit()

    #     # TODO Find CDATA in snippet and parse it for input blocks
    #     f = open(self.define_snippet_path)
    #     snippet = f.read()
    #     f.close()

    #     snippet_content = util.get_content_from_snippet(snippet)
    #     snippet_content = util.remove_unrelated_tokens_in_snippet_content(snippet_content)
    #     template_fragments = util.parse_snippet_content(snippet_content)

    #     # self.view.run_command('insert_snippet',
    #     #                       {'name': self.define_snippet})
    #     self.view.end_edit(edit)


class RemoveRequirejsModuleDependencyCommand(WindowCommand):

    def run(self):
        pass
