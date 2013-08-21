###
# Commands
###
# Add Dependency
#   fuzzy select resource or choose to input
#   if resource selected, input variable name (leave blank for none)
#   if input selected, input resource, then input variable name as above
# Modify Dependency
#   fuzzy select resource
#   input new resource value (or leave as-is)
#   input new variable name (or leave as-is)
# Remove Dependency
#   fuzzy select path or variable name

import os
import re
from itertools import chain

import sublime, sublime_plugin

import util
from module_collection import ModuleCollection
from template import Template


settings_filename = 'RequireJS Module Manager.sublime-settings'

# matches characters enclosed in (included) square brackets or parenthesis
list_regex = re.compile(r"""
    (?P<array>^\[.*\]$)             # captured is an array in square brackets
    |                               # or,
    (?P<args>^\(.*\)$)              # captured is argument(s) in parenthesis
""", re.VERBOSE | re.DOTALL)

# matches all strings enclosed in quotation marks
string_regex = re.compile(r"""
    (?P<quote>['"])                 # opening quote (single or double)
    .*?                             # lazy repeat--allows multiple captures
    (?<!\\)(?P=quote)               # unescaped closing quote (same as above)
""", re.VERBOSE)


class AddRequirejsModuleDependencyCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.packages_path = sublime.packages_path()

        # Active view (area that contains the text buffer)
        self.view = self.window.active_view()

        # First folder in the project
        self.folder = self.window.folders()[0]

        # Load the settings file for this plugin
        self.settings = sublime.load_settings(settings_filename)

        self.requirejs_config = self.get_setting('requirejs_config')

        self.module_collection = ModuleCollection(self.folder,
                                                  self.requirejs_config)

        self.define_snippet = self.get_setting('define_template')

        # Absolute path to define snippet file
        # Need it to open & parse
        self.define_snippet_path = os.path.join(self.packages_path, '..',
                                                self.define_snippet)

        self.mappings = {}
        self.items = ['> Input path to module...'] + self.module_collection.ids
        self.names = []

        self.capture()


    def get_setting(self, prop):
        """Load the property

        First attempts to lookup property in the project settings.
        If it doesn't exist, fall back to this plugin's settings property.
        """
        return self.view.settings().get(prop, self.settings.get(prop))


    def capture(self):
        # get cursor position or span of selection
        original_region = self.view.sel()[0]
        # get the contents of the selection
        selection = self.view.substr(original_region)

        while True:
            match = list_regex.search(selection)
            if match:
                # the selection is either an array or an arguments list
                # pass it on and then stop looping
                self.extract(**match.groupdict())
                break

            # expand the selection's scope
            self.view.run_command('expand_selection', {'to': 'brackets'})
            # get the contents of the new selection
            new_selection = self.view.substr(self.view.sel()[0])

            if new_selection == selection:
                # if the new selection is the same as the old one,
                # we've selected the whole text buffer and need to stop looping
                break

            # set the selection to the selection with increased scope and loop
            selection = new_selection


    def extract(self, array, args):
        print array, args

        if array:
            # TODO:
            # Look for `define(` to left of the array (should allow for an
            #   optional module name argument).
            # Look for `), function(...)` to right of the array
            # Parse strings in array and generate list
            # Split arguments on commas and generate list
            # Create dictionary of key-value pairs with arguments and array items
            # Quick response panel with added items above

            self.window.show_quick_panel(self.items,
                                         self.handle_path_panel_response,
                                         sublime.MONOSPACE_FONT, 0)
        elif args:
            # TODO:
            # Look for `require` to left of the args
            # parse arguments and exit if the returned is not a single string
            # look for `var = ` to left of `require`
            # Create key-value pair with variable name and argument string
            # show quick response panel with added items above
            pass


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
