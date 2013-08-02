import fnmatch
import json
import os
import re
from operator import itemgetter


def strip_ext_if_js(filename):
    (root, ext) = os.path.splitext(filename)
    if ext == '.js':
        return root
    return filename


class ModuleCollection:

    def __init__(self, folder, config={}):
        # folder is the first folder listed in the project side bar.
        # config is either the requirejs config json object,
        # or a path to a json file to be used as the requirejs config.
        if type(config) is unicode:
            config_file = os.path.join(folder, config)
            try:
                f = open(config_file)
                config = json.load(f)
                dirname = os.path.dirname(config_file)
            except IOError, e:
                raise Exception('file does not exist')
            except ValueError, e:
                raise Exception('content not in json format')
        else:
            dirname = folder

        self.basedir = os.path.normpath(os.path.join(dirname, config['appDir'],
                                        config['baseUrl']))

        self.collection = []
        items = [(None, '.')] + config['paths'].items()

        for k, v in items:
            self.collection = self.collection + self.collect(v, k)
        self.collection.sort(key=itemgetter(0))

    def collect(self, relpath, modname=''):
        os.chdir(self.basedir)

        if not os.path.isdir(relpath):
            filename = os.path.split(relpath)[1]
            stripped_filename = strip_ext_if_js(filename)
            abspath = os.path.normpath(os.path.join(self.basedir, relpath))
            return [(modname, abspath)]

        os.chdir(relpath)

        (modules, abspaths) = ([], [])
        exclude = fnmatch.translate('.*')

        for path, dirnames, filenames in os.walk('.'):
            dirnames[:] = [d for d in dirnames if not re.match(exclude, d)]
            filenames[:] = [f for f in filenames if not re.match(exclude, f)]

            for filename in filenames:
                stripped_filename = strip_ext_if_js(filename)
                module = os.path.normpath(os.path.join(path, stripped_filename))
                if modname:
                    module = os.path.join(modname, module)
                abspath = os.path.normpath(os.path.join(self.basedir,
                                                        relpath,
                                                        path,
                                                        filename))
                modules.append(module)
                abspaths.append(abspath)
        return zip(modules, abspaths)

    @property
    def items(self):
        return self.collection

    @property
    def ids(self):
        return [i[0] for i in self.collection]

    @property
    def resources(self):
        return [i[1] for i in self.collection]
