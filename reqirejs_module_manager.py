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

import sublime, sublime_plugin
import os
from itertools import chain

from module_collection import ModuleCollection
from template import Template


class AddRequirejsModuleDependencyCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.view = self.window.active_view()
        self.folder = self.window.folders()[0]
        self.settings = sublime.load_settings('RequireJS Module Manager.sublime-settings')
        self.requirejs_config = self.get_setting('requirejs_config')
        self.module_collection = ModuleCollection(self.folder,
                                                  self.requirejs_config)
        self.template = Template(self.get_setting('template'))

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

    def create_define_enclosure():
        edit = self.view.begin_edit()

        self.view.end_edit(edit)
