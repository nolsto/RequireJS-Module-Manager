import os
import re
from itertools import chain

import sublime, sublime_plugin

from module_collection import ModuleCollection
from template import Template
from util import comment_regex, define_regex, function_regex


settings_filename = 'RequireJS Module Manager.sublime-settings'
# Load the settings file for this plugin
settings = sublime.load_settings(settings_filename)


class AddRequirejsModuleDependencyCommand(sublime_plugin.WindowCommand):

    def run(self):
        # Active view (area that contains the text buffer)
        self.view = self.window.active_view()

        # First folder in the project
        self.folder = self.window.folders()[0]

        self.requirejs_config = self.get_setting('requirejs_config')

        self.module_collection = ModuleCollection(self.folder,
                                                  self.requirejs_config)

        self.items = ['> Input path to module...'] + self.module_collection.ids

        self.capture()


    def get_setting(self, prop):
        """Load the property

        First attempts to lookup property in the project settings.
        If it doesn't exist, fall back to this plugin's settings property.
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
                # the selection is an array,
                # pass it to an extract method and then stop looping
                deps = self.extract_from_array(region)
                break

            (begin_paren, end_paren) = (
                self.view.score_selector(region.begin(), 'meta.brace.round'),
                self.view.score_selector(region.end() - 1, 'meta.brace.round')
            )
            if begin_paren and end_paren:
                # the selection is an arguments list,
                # pass it to an extract method and then stop looping
                deps = self.extract_from_args(region)
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
        deps.__repr__
        try:
            deps.__repr__
        except Exception, e:
            raise
        else:
            pass
        finally:
            # clear regions and add back the original
            # TODO: the cursor is still visually in the wrong place if no actions
            # are taken though
            self.view.sel().clear()
            self.view.sel().add(return_region)
            self.view.show(return_region)
            # pass

    def extract_from_array(self, region):
        if not self.contains_define_array(region):
            return

    def contains_define_array(self, region):
        string = self.view.substr(sublime.Region(0, region.begin()))
        string = self._simplify_js_string(string)

        if not define_regex.search(string):
            return False

        return True

    def contains_define_function(self, region):
        string = self.view.substr(sublime.Region(region.end(), self.view.size()))
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

        # self.window.show_quick_panel(self.items,
        #                              self.handle_path_panel_response,
        #                              sublime.MONOSPACE_FONT, 0)

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

