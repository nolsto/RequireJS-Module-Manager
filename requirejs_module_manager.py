import fnmatch
import json
import os
import re
import sys
from contextlib import contextmanager
from operator import itemgetter
from subprocess import PIPE, Popen

import sublime
from sublime_plugin import WindowCommand


# contants
PLUGIN_FOLDER = os.path.dirname(os.path.realpath(__file__))
PLUGIN_NAME = 'RequireJS Module Manager'
SETTINGS_FILENAME = PLUGIN_NAME + '.sublime-settings'
SETTING_NAMES = (
    'node_command',
    'rjs_path',
    'requirejs_config',
    'ignore',
    'sort_dependencies',
    'sort_order',
    'dependency_template',
    )

# globals
package_settings = None
windows_settings = None


@contextmanager
def chdir(dirname=None):
    curdir = os.getcwd()
    os.chdir(dirname)
    try:
        yield
    finally:
        os.chdir(curdir)


def is_accessible_file(filepath, mode=os.R_OK):
    return os.path.isfile(filepath) and os.access(filepath, mode)


def which(program):
    mode = os.X_OK
    filepath, filename = os.path.split(program)

    if filepath:
        if is_accessible_file(program, mode):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_accessible_file(exe_file, mode):
                return exe_file
    return None


def strip_ext_if_js(filename):
    (root, ext) = os.path.splitext(filename)
    return root if ext == '.js' else filename


def var_sort(key):
    return ' ' if key else '~'


def id_sort(key, sort_order):
    prefix = ' '
    length = len(sort_order)
    match = re.search('^(https?\:\/\/)?((?:\.)+?(?=/))?(/)?', key)
    if match.group(1):
        sort_by = 'remote'
    elif match.group(2):
        sort_by = 'relative'
    elif match.group(3):
        sort_by = 'absolute'
    else:
        sort_by = 'id'
    count = length - sort_order.index(sort_by) - 1
    return (prefix * count) + key


def plugin_loaded():
    global package_settings, windows_settings

    package_settings = SettingsAdapter(sublime.load_settings(SETTINGS_FILENAME))
    windows_settings = {}




class SettingsAdapter(object):

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
                    # adapt setting if its _adapt_ method is in this class
                    self.adapted_settings[name] = getattr(self, '_adapt_' + name)()
                except AttributeError, e:
                    pass
                self.prev_settings[name] = self._settings.get(name)

    def _adapt_node_command(self):
        """Locate node binary file"""

        with chdir(self.folder):
            setting = self._settings.get('node_command')
            result = which(setting)
            if not result:
                message = 'Node.js command or binary file %s cannot be found.' % setting
                print '%s: %s' % (PLUGIN_NAME, message)
                return None
            return os.path.realpath(result)

    def _adapt_rjs_path(self):
        """Locate r.js file"""

        with chdir(self.folder):
            setting = self._settings.get('rjs_path', '')
            result = which(setting)
            if not result:
                if is_accessible_file(setting):
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
            with chdir(self.folder):
                if is_accessible_file(setting):
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

    def _adapt_ignore(self):
        """Convert the string into a pattern"""

        setting = self._settings.get('ignore')
        patterns = setting.strip().split()
        pattern = re.compile('|'.join(fnmatch.translate(p) for p in patterns))
        return pattern


class Settings(object):

    def __init__(self, window_settings):
        self.window_settings = window_settings

    def __getattr__(self, attr):
        global package_settings

        window_setting = self.window_settings.get(attr)
        package_setting = package_settings.get(attr)
        return window_setting if window_setting != None else package_setting




class Collection(object):

    def __init__(self, collection):
        self._collection = collection

    def __str__(self):
        return json.dumps(self._collection)

    @property
    def items(self):
        return self._collection[:]

    @property
    def keys(self):
        return [k for k, v in self._collection]

    @property
    def values(self):
        return [v for k, v in self._collection]

    def append(self, *args, **kwargs):
        self._collection.append(*args, **kwargs)

    def sort(self, *args, **kwargs):
        self._collection.sort(*args, **kwargs)

    def keyof(self, value):
        return next((k for k, v in self._collection if v == value), None)

    def valueof(self, key):
        return next((v for k, v in self._collection if k == key), None)

    def filter_keys(self):
        c = self._collection
        result = []
        for i, el in enumerate(c):
            if el[0] not in [k for k, v in c[i+1:]]:
                result.append(el)
        self._collection = result

    def filter_values(self):
        # same as filter on keys except doesn't compare values of None
        c = self._collection
        result = []
        for i, el in enumerate(c):
            if el[1] == None or el[1] not in [v for k, v in c[i+1:]]:
                result.append(el)
        self._collection = result


class ModuleCollection(Collection):

    def __init__(self, folder, ignore, config={}):
        # folder should be the first folder listed in the project side bar.
        # config is the requirejs config json object

        paths = config.get('paths', {})
        appDir = config.get('appDir', os.curdir)
        baseUrl = config.get('baseUrl', os.curdir)
        basedir = os.path.normpath(os.path.join(folder, appDir, baseUrl))

        def collect(relpath, modname=''):
            # if the path is not a directory, return the item
            if not os.path.isdir(relpath):
                filename = os.path.split(relpath)[1]
                stripped_filename = strip_ext_if_js(filename)
                abspath = os.path.normpath(os.path.join(basedir, relpath))
                return [(modname, abspath)]

            os.chdir(relpath)

            (modules, abspaths) = ([], [])

            for path, dirnames, filenames in os.walk('.'):
                dirnames[:] = [d for d in dirnames if not re.match(ignore, d)]
                filenames[:] = [f for f in filenames if not re.match(ignore, f)]

                for filename in filenames:
                    stripped_filename = strip_ext_if_js(filename)
                    module = os.path.normpath(os.path.join(path, stripped_filename))
                    if modname:
                        module = os.path.join(modname, module)
                    abspath = os.path.normpath(os.path.join(basedir, relpath,
                                                            path, filename))
                    modules.append(module)
                    abspaths.append(abspath)
            return zip(modules, abspaths)

        collection = []
        items = [(None, '.')] + paths.items()

        for key, value in items:
            with chdir(basedir):
                collection += collect(value, key)

        self._collection = collection
        self.sort(key=itemgetter(0))




class RequireJSModuleDependencyCommand(WindowCommand):

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

    def extractDeps(self):
        view = self.window.active_view()
        contents = view.substr(sublime.Region(0, view.size()))
        selection = view.sel()[0]

        script = os.path.join(PLUGIN_FOLDER, 'js/extract_dependencies.js')
        cmd = (self.settings.node_command, script, self.settings.rjs_path,
               contents, str(selection.begin()), str(selection.end()))
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()
        if stderr:
            print '%s: %s' % (PLUGIN_NAME, stderr)
            raise Exception()

        try:
            result = json.loads(stdout)
            self.deps_node = result['node']
            self.deps = Collection(result['collection'])
            self.dep_id = result['id']
            self.dep_var = result['var']
        except Exception, e:
            message = 'Unable to extract any dependencies.'
            print '%s: %s' % (PLUGIN_NAME, message)
            raise

    def insertDeps(self):
        view = self.window.active_view()
        contents = view.substr(sublime.Region(0, view.size()))
        selection = view.sel()[0]

        script = os.path.join(PLUGIN_FOLDER, 'js/insert_dependencies.js')
        cmd = (self.settings.node_command, script, self.settings.rjs_path,
               contents, json.dumps(self.deps_node), str(self.deps),
               str(self.var_changes), self.settings.dependency_template)
        print '\n'.join(cmd)
        # print self.deps, self.var_changes
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()
        if stderr:
            print '%s: %s' % (PLUGIN_NAME, stderr)
            raise Exception()
        print stdout


class AddRequirejsModuleDependencyCommand(RequireJSModuleDependencyCommand):

    def modifyDeps(self):
        dep_id = self.dep_id
        dep_var = self.dep_var or None

        if [dep_id, dep_var] in self.deps.items:
            message = 'No modifications to dependencies.'
            print '%s: %s' % (PLUGIN_NAME, message)
            raise Exception()

        orig_items = self.deps.items

        self.deps.append([dep_id, dep_var])

        # remove all but the last item where id is repeated, repeat for var name
        self.deps.filter_keys()
        self.deps.filter_values()

        # sort items on id then on has/doesn't have var name
        if self.settings.sort_dependencies:
            # wrap the sort function to be called with the current sort order setting
            def with_setting(f):
                def wrapper(key):
                    return f(key, self.settings.sort_order)
                return wrapper
            id_sort_with_setting = with_setting(id_sort)

            self.deps.sort(key=lambda x: id_sort_with_setting(x[0]))

        self.deps.sort(key=lambda x: var_sort(x[1]))

        # get a collection of changed var names
        var_changes = [(v, self.deps.valueof(k)) for k, v in orig_items \
                       if self.deps.valueof(k) != v]
        var_changes = filter(lambda x: (x[0] != None and x[1] != None), var_changes)
        self.var_changes = Collection(var_changes)

        self.insertDeps()

    def run(self):
        self.setup()
        self.extractDeps()

        if self.dep_id:
            self.handle_id_input(self.dep_id)
            return

        if type(self.settings.requirejs_config) is unicode:
            script = os.path.join(PLUGIN_FOLDER, 'js/extract_requirejs_config.js')
            cmd = (self.settings.node_command, script,
                   self.settings.rjs_path, self.settings.requirejs_config)
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
            stdout, stderr = proc.communicate()
            if stderr:
                message = 'no requirejs config object found in %s' % \
                          self.settings.requirejs_config
                print '%s: %s' % (PLUGIN_NAME, message)
                raise Exception()
            requirejs_config = json.loads(stdout)
        else:
            requirejs_config = self.settings.requirejs_config

        # create module collection
        self.modules = ModuleCollection(self.folder, self.settings.ignore, requirejs_config)
        self.request_id()

    def request_id(self):
        preindex = -1
        if self.dep_var:
            dep_id = self.deps.keyof(self.dep_var)
            try:
                preindex = self.modules.keys.index(dep_id)
            except ValueError:
                pass
        preindex += 1

        items = [':Input module ID or path...'] + self.modules.keys
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
            if self.dep_var:
                prefill = self.deps.keyof(self.dep_var)
            self.window.show_input_panel('Module ID or path:', prefill,
                                         self.handle_id_input, None, None)
            return
        module_id = self.modules.keys[index - 1]
        self.handle_id_input(module_id)

    def handle_id_input(self, module_id):
        module_id = unicode(module_id).strip()
        if not module_id:
            return

        prefill = None

        if module_id in self.deps.keys:
            prefill = self.deps.valueof(module_id)

        if not prefill:
            (basename, ext) = os.path.splitext(os.path.basename(module_id))
            prefill = basename

        if not self.dep_var:
            self.request_varname(prefill)

        self.dep_id = module_id

        if self.dep_id and self.dep_var != None:
            self.modifyDeps()

    def handle_varname_input(self, module_var):
        self.dep_var = unicode(module_var).strip()

        if self.dep_id and self.dep_var != None:
            self.modifyDeps()


class RemoveRequirejsModuleDependencyCommand(RequireJSModuleDependencyCommand):

    def modifyDeps(self):
        dep_id = self.dep_id
        dep_var = self.deps.valueof(dep_id)
        deps = self.deps.items
        deps.remove([dep_id, dep_var])

        self.deps = Collection(deps)
        self.var_changes = Collection([])

        self.insertDeps()

    def run(self):
        self.setup()
        self.extractDeps()
        self.request_id()

    def request_id(self):
        if self.dep_id:
            dep_id = self.dep_id
        elif self.dep_var:
            dep_id = self.deps.keyof(self.dep_var)

        try:
            index = self.deps.keys.index(dep_id)
        except Exception:
            self.window.show_quick_panel(self.deps.keys,
                                         self.handle_id_panel_response,
                                         sublime.MONOSPACE_FONT)
        else:
            self.handle_id_panel_response(index)

    def handle_id_panel_response(self, index):
        if index is -1:
            return

        dep_id = self.deps.keys[index]
        self.dep_id = dep_id
        self.modifyDeps()




if sys.version_info < (3,):
    plugin_loaded()
