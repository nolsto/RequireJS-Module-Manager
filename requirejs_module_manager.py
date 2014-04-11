import json
import os
import re
import sys
from subprocess import PIPE, Popen

import sublime
from sublime_plugin import WindowCommand

import utils
from collections import DependencyCollection, ModuleCollection


# contants
PLUGIN_FOLDER = os.path.dirname(os.path.realpath(__file__))
PLUGIN_NAME = 'RequireJS Module Manager'
SETTINGS_FILENAME = PLUGIN_NAME + '.sublime-settings'
SETTING_NAMES = ('node_command', 'rjs_path', 'requirejs_config',
                 'quote_style', 'ignore', 'leading_comma')

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


class Settings(object):
    """docstring for Settings"""

    def __init__(self, window_settings):
        self.window_settings = window_settings

    def __getattr__(self, attr):
        global package_settings

        return self.window_settings.get(attr) or package_settings.get(attr)


class RequireJSModuleDependencyCommand(WindowCommand):
    """docstring for RequireJSModuleDependencyCommand"""

    def setup(self):
        global windows_settings

        # find first folder in the project
        try:
            folder = self.window.folders()[0]
        except IndexError as e:
            message = 'Command must be run in a project with at least one folder.'
            print '%s: %s' % (PLUGIN_NAME, message)
            raise

        view_settings = self.window.active_view().settings()
        try:
            window_settings = windows_settings[self.window.id()]
        except KeyError, e:
            window_settings = SettingsAdapter(view_settings, folder)
            windows_settings[self.window.id()] = window_settings
        else:
            window_settings.folder = folder
            window_settings.settings = view_settings

        self.folder = folder
        self.settings = Settings(window_settings)

    def findDeps(self):
        view = self.window.active_view()
        contents = view.substr(sublime.Region(0, view.size()))
        selection = view.sel()[0]

        script = os.path.join(PLUGIN_FOLDER, 'js/get_dependencies.js')
        cmd = (self.settings.node_command, script, self.settings.rjs_path, contents,
               '%d,%d' % (selection.begin(), selection.end()))
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()

        if stderr:
            print '%s: %s' % (PLUGIN_NAME, stderr)
            raise Exception()

        try:
            result = json.loads(stdout)
            self.deps = DependencyCollection(**result)
        except Exception, e:
            message = 'Unable to extract any dependencies.'
            print '%s: %s' % (PLUGIN_NAME, message)
            raise


class AddRequirejsModuleDependencyCommand(RequireJSModuleDependencyCommand):
    """docstring for AddRequirejsModuleDependencyCommand"""

    def run(self):
        self.setup()
        self.findDeps()

        print self.deps.collection
        if self.deps.id:
            self.handle_id_input(self.deps.id)
        else:
            if type(self.settings.requirejs_config) is unicode:
                script = os.path.join(PLUGIN_FOLDER, 'js/get_requirejs_config.js')
                cmd = (self.settings.node_command, script,
                       self.settings.rjs_path, self.settings.requirejs_config)
                proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
                stdout, stderr = proc.communicate()
                if stderr:
                    message = 'no requirejs config object found in %s' % self.settings.requirejs_config
                    print '%s: %s' % (PLUGIN_NAME, message)
                    return
                requirejs_config = json.loads(stdout)
            else:
                requirejs_config = self.settings.requirejs_config

            # create module collection
            self.module_collection = ModuleCollection(self.folder, requirejs_config)
            self.request_id(0)

    def request_id(self, preindex):
        items = ['Input module ID or path...'] + self.module_collection.ids
        self.window.show_quick_panel(items, self.handle_id_panel_response,
                                     sublime.MONOSPACE_FONT, preindex)

    def request_varname(self, prefill):
        self.window.show_input_panel('Module variable name:', prefill,
                                     self.handle_varname_input, None, None)

    def handle_id_panel_response(self, index):
        if index is -1:
            return
        if index is 0:
            prefill = ''
            if self.deps.var:
                ids = self.deps.ids
                collection = self.deps.collection
                var = self.deps.var
                prefill = next((val for val in ids if collection[val] == var), None)
            self.window.show_input_panel('Module ID or path:', prefill,
                                         self.handle_id_input, None, None)
            return
        module_id = self.module_collection.ids[index - 1]
        self.handle_id_input(module_id)

    def handle_id_input(self, module_id):
        prefill = None

        if module_id in self.deps.collection:
            prefill = self.deps.collection[module_id]

        if not prefill:
            (basename, ext) = os.path.splitext(os.path.basename(module_id))
            prefill = basename

        if not self.deps.var:
            self.request_varname(prefill)

        # self.deps.id = module_id


    def handle_varname_input(self, module_varname):
        ids = self.deps.ids
        collection = self.deps.collection
        module_id = next((val for val in ids if collection[val] == module_varname), None)

        if module_id:
            # find index
            pass
        else:
            pass

        if not self.deps.id:
            self.request_id(0)

        # self.deps.id = module_id


class RemoveRequirejsModuleDependencyCommand(RequireJSModuleDependencyCommand):
    """docstring for RemoveRequirejsModuleDependencyCommand"""

    def run(self):
        self.setup()

        # self.window.show_quick_panel(items, self.handle_id_panel_response,
        #                              sublime.MONOSPACE_FONT, 0)

    def handle_id_panel_response(self, index):
        pass


if sys.version_info < (3,):
    plugin_loaded()
