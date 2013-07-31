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

class AddRequireDependencyCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.folder = self.window.folders()[0]
        self.view = self.window.active_view()
        self.settings = sublime.load_settings(
            'RequireDependencyManager.sublime-settings')
        self.requirejs_config = self.get_setting('requirejs_config')
        self.module_collection = ModuleCollection(self.folder,
                                                  self.requirejs_config)
        self.window.show_quick_panel(self.module_collection.ids(),
                                     self.insert_link,
                                     sublime.MONOSPACE_FONT)

    def get_setting(self, prop, override=True):
        if not override:
            return self.view.settings().get(prop)
        return self.view.settings().get(prop, self.settings.get(prop))

    def insert_link(self, choice):
        if choice == -1: return
        search = 'poo'
        edit = self.view.begin_edit()
        self.window.run_command('show_overlay', {'overlay': 'goto', 'text': '@%s' % search})
        # self.view.run_command('insert_snippet',
        #                       {"name": "Packages/User/console-log.sublime-snippet"})
        # self.view.run_command('example')
        self.view.end_edit(edit)
