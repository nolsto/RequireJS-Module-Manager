import json
import os
import re
import sys
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
SETTING_NAMES = ('node_command', 'rjs_path', 'requirejs_config',
                 'quote_style', 'leading_comma_lists', 'leading_comma_vars')

# globals
package_settings = None
windows_settings = None


def plugin_loaded():
    global package_settings, windows_settings

    package_settings = SettingsAdapter(sublime.load_settings(SETTINGS_FILENAME))
    windows_settings = {}


class SettingsAdapter(object):
    """docstring for SettingsAdapter"""

    def __init__(self, settings, folder=PLUGIN_FOLDER):
        self.folder = folder
        self.prev_settings = dict((name, None) for name in SETTING_NAMES)
        self.adapted_settings = {}
        self.settings = settings

    @property
    def settings(self):
        s = self._settings
        return dict((name, s.get(name)) for name in SETTING_NAMES if s.has(name))

    @settings.setter
    def settings(self, value):
        # TODO check for existence too. ST may have nullified it if view closed
        if hasattr(self, '_settings'):
            self._settings.clear_on_change('rjsmm')
        self._settings = value
        self._settings.add_on_change('rjsmm', self.update)
        self.update()

    def get(self, name):
        if name in self.adapted_settings:
            return self.adapted_settings[name]
        return self._settings.get(name)

    def update(self):
        """Update each setting if actual change occured on it"""

        for name in SETTING_NAMES:
            if self._settings.get(name) != self.prev_settings[name]:
                try:
                    # adapt setting if its adapt method is in this class
                    self.adapted_settings[name] = getattr(self, '_adapt_' + name)()
                except AttributeError, e:
                    pass
                self.prev_settings[name] = self._settings.get(name)
            print name, ':', self.get(name)

    def _adapt_node_command(self):
        """Locate node binary file"""

        with utils.chdir(self.folder):
            setting = self._settings.get('node_command')
            result = utils.which(setting)
            if not result:
                message = 'Node.js command or binary file %s cannot be found.' % setting
                print '%s: %s' % (PLUGIN_NAME, message)
                return None
            return os.path.realpath(result)

    def _adapt_rjs_path(self):
        """Locate r.js file"""

        with utils.chdir(self.folder):
            setting = self._settings.get('rjs_path', '')
            result = utils.which(setting)
            if not result:
                if utils.is_accessible_file(setting):
                    result = setting
                else:
                    message = 'r.js command or file path %s cannot be found.' % setting
                    print '%s: %s' % (PLUGIN_NAME, message)
                    return None
            return os.path.realpath(result)

    def _adapt_requirejs_config(self):
        """Determine requirejs config object"""

        setting = self._settings.get('requirejs_config')
        if type(setting) is dict:
            result = setting
            return result
        elif type(setting) is unicode:
            with utils.chdir(self.folder):
                if utils.is_accessible_file(setting):
                    result = setting
                else:
                    message = 'RequireJS config file path %s cannot be found' % setting
                    print '%s: %s' % (PLUGIN_NAME, message)
                    return None
                return os.path.realpath(result)
        else:
            message = 'RequireJS config setting must be either a valid JSON object or file path'
            print '%s: %s' % (PLUGIN_NAME, message)
            return None


class RequireJSModuleDependencyCommand(WindowCommand):
    """docstring for RequireJSModuleDependencyCommand"""


class AddRequirejsModuleDependencyCommand(RequireJSModuleDependencyCommand):

    def run(self):
        global package_settings, windows_settings

        # find first folder in the project
        try:
            folder = self.window.folders()[0]
        except IndexError as e:
            message = 'Command must be run in a project with at least one folder.'
            print '%s: %s' % (PLUGIN_NAME, message)
            return

        view_settings = self.window.active_view().settings()
        try:
            window_settings = windows_settings[self.window.id()]
        except KeyError, e:
            window_settings = SettingsAdapter(view_settings, folder)
            windows_settings[self.window.id()] = window_settings
        else:
            window_settings.folder = folder
            window_settings.settings = view_settings

        node_command = window_settings.get('node_command') or package_settings.get('node_command')
        rjs_path = window_settings.get('rjs_path') or package_settings.get('rjs_path')
        requirejs_config = window_settings.get('requirejs_config') or package_settings.get('requirejs_config')

        if not (node_command and rjs_path and requirejs_config):
            message = 'Missing necessary settings'
            print '%s: %s' % (PLUGIN_NAME, message)
            return

        if type(requirejs_config) is unicode:
            script = os.path.join(PLUGIN_FOLDER, 'js/parse_requirejs_config.js')
            cmd = [node_command, script, rjs_path, requirejs_config]
            try:
                proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
                stdout, stderr = proc.communicate()
                if stderr:
                    message = 'no requirejs config object found in %s' % requirejs_config
                    print '%s: %s' % (PLUGIN_NAME, message)
                    return
                requirejs_config = json.loads(stdout)
            except Exception as e:
                raise

        # create module collection
        self.module_collection = ModuleCollection(folder, requirejs_config)
        items = ['Input module path...'] + self.module_collection.ids

        self.window.show_quick_panel(items, self.handle_id_panel_response,
                                     sublime.MONOSPACE_FONT, 0)


    # def update_settings(self):
    #     """Update all project-specific settings"""

    #     self.update_node_command()
    #     self.update_rjs_path()
    #     self.update_rjs_config()


    # def update_node_command(self):
    #     """Locate node binary file"""

    #     setting = self.get_setting('node_command')
    #     command = utils.which(setting)
    #     if not command:
    #         command = utils.which(os.path.join(self.folder, setting))
    #         if not command:
    #             message = 'Node.js command or binary file cannot be found.'
    #             print '%s: %s' % (PLUGIN_NAME, message)
    #             return

    #     self.node_command = os.path.realpath(command)


    # def update_rjs_path(self):
    #     """Locate r.js file"""

    #     setting = self.get_setting('r.js_path')
    #     if not setting:
    #         path = os.path.join(PLUGIN_FOLDER, 'lib/r.js')
    #     else:
    #         path = utils.which(setting)
    #         if not path:
    #             if utils.is_accessible_file(setting):
    #                 path = setting
    #             else:
    #                 path = os.path.join(self.folder, setting)
    #                 if not utils.is_accessible_file(path):
    #                     message = 'r.js command or file path cannot be found.'
    #                     print '%s: %s' % (PLUGIN_NAME, message)
    #                     return

    #     self.rjs_path = os.path.realpath(path)


    # def update_rjs_config(self):
    #     """Determine requirejs config object"""

    #     setting = self.get_setting('requirejs_config')
    #     if type(setting) is dict:
    #         config = setting
    #     elif type(setting) is unicode:
    #         if utils.is_accessible_file(setting):
    #             filepath = setting
    #         else:
    #             filepath = os.path.join(self.folder, setting)
    #             if not utils.is_accessible_file(filepath):
    #                 message = 'RequireJS config file path %s cannot be found' % setting
    #                 print '%s: %s' % (PLUGIN_NAME, message)
    #                 return
    #         script = os.path.join(PLUGIN_FOLDER, 'scripts/parse_requirejs_config.js')
    #         cmd = [self.node_command, script, self.rjs_path, filepath]
    #         try:
    #             proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    #             stdout, stderr = proc.communicate()
    #             if stderr:
    #                 message = 'no requirejs config object found in %s' % setting
    #                 print '%s: %s' % (PLUGIN_NAME, message)
    #                 return
    #             config = json.loads(stdout)
    #         except Exception as e:
    #             raise
    #     else:
    #         message = 'RequireJS config setting must be either a valid JSON object or file path'
    #         print '%s: %s' % (PLUGIN_NAME, message)

    #     self.rjs_config = config


    # def get_setting(self, prop):
    #     """Load the property

    #     First attempts to lookup property in the project settings.
    #     If it doesn't exist, fall back to plugin's settings property.
    #     """

    #     global settings
    #     return self.view.settings().get(prop, settings.get(prop))


    def handle_id_panel_response(self, index):
        print index
        if index is -1:
            return
        if index is 0:
            self.window.show_input_panel('Module id or path:', '',
                                         self.handle_id_input, None, None)
            return
        module_id = self.module_collection.ids[index - 1]
        self.handle_id_input(module_id)


    def handle_id_input(self, inputstr):
        (module_varname, ext) = os.path.splitext(os.path.basename(inputstr))
        self.window.show_input_panel('Module variable name:', module_varname,
                                     self.handle_varname_input, None, None)
        print 'id: ', inputstr


    def handle_varname_input(self, inputstr):
        print 'varname: ', inputstr
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


class RemoveRequirejsModuleDependencyCommand(RequireJSModuleDependencyCommand):

    def run(self):
        pass


if sys.version_info < (3,):
    plugin_loaded()

