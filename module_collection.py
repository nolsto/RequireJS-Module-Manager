import os
import fnmatch
import re

class ModuleCollection:

    def __init__(self, folder, config):
        # folder is the first folder listed in the project side bar.
        # config is either the requirejs config json object,
        # or a path to a json file to be used as the requirejs config.
        self.base_dir = os.path.join(folder, config['appDir'],
                                     config['baseUrl'])

        self.collection = []
        items = [(None, '.')] + config['paths'].items()

        for k, v in items:
            self.collection = self.collection + self.collect(v, k)

    def __strip_ext_if_js(self, filename):
        (root, ext) = os.path.splitext(filename)
        if ext == '.js':
            return root
        return filename

    def collect(self, relpath, modname=''):
        os.chdir(self.base_dir)

        if not os.path.isdir(relpath):
            filename = os.path.split(relpath)[1]
            stripped_filename = self.__strip_ext_if_js(filename)
            abspath = os.path.normpath(os.path.join(self.base_dir, relpath))
            return [(modname, abspath)]

        os.chdir(relpath)

        (modules, abspaths) = ([], [])
        exclude = fnmatch.translate('.*')

        for path, dirnames, filenames in os.walk('.'):
            dirnames[:] = [d for d in dirnames if not re.match(exclude, d)]
            filenames[:] = [f for f in filenames if not re.match(exclude, f)]

            for filename in filenames:
                stripped_filename = self.__strip_ext_if_js(filename)
                module = os.path.normpath(os.path.join(path,
                                                       stripped_filename))
                if type(modname) is str:
                    module = os.path.join(modname, module)
                abspath = os.path.normpath(os.path.join(self.base_dir,
                                                        relpath,
                                                        path,
                                                        filename))
                modules.append(module)
                abspaths.append(abspath)
        return zip(modules, abspaths)

    def items(self):
        return self.collection

    def ids(self):
        # return [k for k, v in enumerate(self.collection)]
        return [i[0] for i in self.collection]

    def resources(self):
        return [i[1] for i in self.collection]
