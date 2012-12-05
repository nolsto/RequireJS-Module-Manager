import sublime
import sublime_plugin
import os

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

class ExampleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "Hello, World!")

class AddDependencyCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.settings = sublime.load_settings(
            'RequireDependencyManager.sublime-settings')
        view = self.window.active_view()
        base_directory = view.settings().get('base_directory',
            self.settings.get('base_directory'))

        print base_directory
        print os.listdir(base_directory)

        for dirpath, dirnames, filenames in os.walk(base_directory):
            for filename in filenames:
                print filename
        # print os.path.splitext(os.path.basename(view.settings().get('syntax')))
        # self.window.show_quick_panel('Module Path:', '', self.insert_link,
        #     None, None)

    def insert_link(self, choice):
        if choice == -1: return
        print choice
