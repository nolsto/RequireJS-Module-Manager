import sublime, sublime_plugin
import os
from itertools import chain

from module_collection import ModuleCollection

###
# Commands
###
# Add Dependency
#   input path
#   input variable name (leave blank for none)
# Modify Dependency
#   fuzzy select path or variable name
#   input new value
#   if variable name modified, input new path,
#   if path modified, input new variable name
# Remove Dependency
#   fuzzy select path or variable name
###
# Settings
###
# Arrange alphabetically and optionally by depth
# Style preferences:
# var ModuleA = require('path/to/module_a'),
#     ModuleB = require('path/to/module_b');
# var ModuleA = require('path/to/module_a')
#   , ModuleB = require('path/to/module_b');

class AddRequirejsModuleDependencyCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.folder = self.window.folders()[0]
        self.view = self.window.active_view()
        self.settings = sublime.load_settings(
            'RequireJS Module Manager.sublime-settings'
        )
        self.requirejs_config = self.get_setting('requirejs_config')
        self.module_collection = ModuleCollection(self.folder,
                                                  self.requirejs_config)
        items = ['> Input path to module...'] + self.module_collection.ids
        self.window.show_quick_panel(items, self.handle_quick_panel_response,
                                     sublime.MONOSPACE_FONT, 0)

    def get_setting(self, prop, override=True):
        if not override:
            return self.view.settings().get(prop)
        return self.view.settings().get(prop, self.settings.get(prop))

    def handle_quick_panel_response(self, index):
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
