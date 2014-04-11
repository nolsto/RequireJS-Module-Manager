import fnmatch
import json
import os
import re
from operator import itemgetter

import utils


EXCLUDES = fnmatch.translate('.*')


def strip_ext_if_js(filename):
    (root, ext) = os.path.splitext(filename)
    return root if ext == '.js' else filename


class DependencyCollection(object):

    def __init__(self, **kwargs):
        for key, val in kwargs.iteritems():
            setattr(self, key, val)

    # def __str__(self):
    #     return json.dumps('map': self.)

    @property
    def ids(self):
        return self.collection.keys()

    @property
    def vars(self):
        return self.collection.values()


class ModuleCollection(object):

    def __init__(self, folder, config={}):
        # folder should be the first folder listed in the project side bar.
        # config is the requirejs config json object

        paths = config.get('paths', {})
        appDir = config.get('appDir', os.curdir)
        baseUrl = config.get('baseUrl', os.curdir)
        basedir = os.path.normpath(os.path.join(folder, appDir, baseUrl))
        collection = []
        items = [(None, '.')] + paths.items()

        for key, val in items:
            collection += self.collect(basedir, val, key)

        collection.sort(key=itemgetter(0))
        self.collection = collection

    def collect(self, basedir, relpath, modname=''):
        with utils.chdir(basedir):
            if not os.path.isdir(relpath):
                filename = os.path.split(relpath)[1]
                stripped_filename = strip_ext_if_js(filename)
                abspath = os.path.normpath(os.path.join(basedir, relpath))
                return [(modname, abspath)]

            os.chdir(relpath)

            (modules, abspaths) = ([], [])

            for path, dirnames, filenames in os.walk('.'):
                dirnames[:] = [d for d in dirnames if not re.match(EXCLUDES, d)]
                filenames[:] = [f for f in filenames if not re.match(EXCLUDES, f)]

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

    @property
    def ids(self):
        return [i[0] for i in self.collection]

    @property
    def resources(self):
        return [i[1] for i in self.collection]
