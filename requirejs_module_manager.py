import json
import os
import re
import sys
from itertools import izip_longest
from subprocess import PIPE, Popen

import sublime
from sublime_plugin import WindowCommand

import utils
from module_collection import ModuleCollection
from template import Template


# contants
PLUGIN_FOLDER = os.path.dirname(os.path.realpath(__file__))
PLUGIN_NAME = 'RequireJS Module Manager'
SETTINGS_FILENAME = PLUGIN_NAME + '.sublime-settings'

# globals
settings = None
windows = None


# get id of window
# create new window entry if id not present
# if id present, remove event listener from window settings
# add event listener to view settings
# add view settings to window as settings


def plugin_loaded():
    global settings, windows

    windows = {}
    settings = sublime.load_settings(SETTINGS_FILENAME)
    settings.add_on_change('rjsmm', update_settings)


def update_settings():
    global settings

    # locate node binary file


    node_command_setting = settings.get('node_command')
    node_command = utils.which(node_command_setting)
    if not node_command:
        message = 'Node.js command or binary file cannot be found.'
        print '%s: %s' % (PLUGIN_NAME, message)
        return
    node_command = os.path.realpath(node_command)

    # locate r.js file
    rjs_path_setting = settings.get('r.js_path')
    rjs_path = utils.which(rjs_path_setting)
    if not rjs_path:
        if utils.is_accessible_file(rjs_path_setting):
            rjs_path = rjs_path_setting
        else:
            rjs_path = os.path.join(PLUGIN_FOLDER, 'lib/r.js')
    rjs_path = os.path.realpath(rjs_path)

    # windows[sublime.active_window().id()] = {'node_command': node_command,
    #                                          'rjs_path': rjs_path}


def get_node_command(setting):
    """Locate node binary file"""

    global settings

    setting = self.get_setting('node_command')
    command = utils.which(setting)
    if not command:
        command = utils.which(os.path.join(folder, setting))
        if not command:
            message = 'Node.js command or binary file cannot be found.'
            print message_fragment, message
            return
    return os.path.realpath(command)


# def update_node_command():
#     """Locate node binary file"""

#     node_command_setting = self.get_setting('node_command')
#     node_command = utils.which(node_command_setting)
#     if not node_command:
#         node_command = utils.which(os.path.join(folder, node_command_setting))
#         if not node_command:
#             message = 'Node.js command or binary file cannot be found.'
#             print message_fragment, message
#             return
#     node_command = os.path.realpath(node_command)


# def update_rjs_path():
#     """Locate r.js file"""

#     rjs_path_setting = self.get_setting('r.js_path')
#     rjs_path = utils.which(rjs_path_setting)
#     if not rjs_path:
#         if utils.is_accessible_file(rjs_path_setting):
#             rjs_path = rjs_path_setting
#         else:
#             rjs_path = os.path.join(folder, rjs_path_setting)
#             if not utils.is_accessible_file(rjs_path):
#                 message = 'r.js command or file path cannot be found.'
#                 print message_fragment, message
#                 return
#     rjs_path = os.path.realpath(rjs_path)


# def update_rjs_config():
#     pass


def say_hi():
    print 'hi'


class AddRequirejsModuleDependencyCommand(WindowCommand):

    def run(self):
        global windows

        window = self.window
        window_id = window.id()

        if not window_id in windows:
            windows[window_id] = window
        else:
            for view in windows[window_id].views():
                view.settings().clear_on_change('rjsmm')

        window.active_view().settings().add_on_change('rjsmm', self.say_hi)


        # def update_settings():
        #     print 'Update settings', last_active_view.id()

        # view = self.window.active_view()
        # settings = view.settings()

        # if last_active_view:
        #     last_active_view.settings().clear_on_change('poo')
        # else:
        #     last_active_view = view
        #     update_settings()

        # settings.add_on_change('poo', update_settings)

        # last_active_view = view

        # # find first folder in the project
        # try:
        #     folder = self.window.folders()[0]
        # except IndexError as e:
        #     message = 'Command must be run in a project with at least one folder.'
        #     print message_fragment + message
        #     return

        # # determine requirejs config object
        # rjs_config_setting = self.get_setting('requirejs_config')
        # if type(rjs_config_setting) is dict:
        #     rjs_config = rjs_config_setting
        # elif type(rjs_config_setting) is unicode:
        #     if utils.is_accessible_file(rjs_config_setting):
        #         rjs_config_fpath = rjs_config_setting
        #     else:
        #         rjs_config_fpath = os.path.join(folder, rjs_config_setting)
        #         if not utils.is_accessible_file(rjs_config_fpath):
        #             message = 'RequireJS config file path %s cannot be found'
        #             print message_fragment, message % rjs_config_setting
        #             return

        #     script = os.path.join(PLUGIN_FOLDER, 'scripts/parse_requirejs_config.js')
        #     cmd = [node, script, rjs, rjs_config_fpath]
        #     try:
        #         proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        #         stdout, stderr = proc.communicate()
        #         if stderr:
        #             message = 'no requirejs config object found in %s'
        #             print message_fragment, message % rjs_config_setting
        #             return
        #         rjs_config = json.loads(stdout)
        #     except Exception as e:
        #         raise
        # else:
        #     message = 'RequireJS config setting must be either a valid JSON object or file path'
        #     print message_fragment, message


        # # create module collection
        # self.module_collection = ModuleCollection(folder, rjs_config)
        # self.items = ['> Input module path...'] + self.module_collection.ids
        # print self.items

    def say_hi(self):
        print 'hi from %s, %s' % (self.window.id(), self.window.active_view())


    def get_setting(self, prop):
        """Load the property

        First attempts to lookup property in the project settings.
        If it doesn't exist, fall back to plugin's settings property.
        """
        return self.view.settings().get(prop, settings.get(prop))


    # self.window.show_quick_panel(self.items,
    #                              self.handle_path_panel_response,
    #                              sublime.MONOSPACE_FONT, 0)


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
        # (module_varname, ext) = path.splitext(path.basename(module_id))
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


if sys.version_info < (3,):
    plugin_loaded()

