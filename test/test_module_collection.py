import json
import os.path
import unittest

from requirejs_module_manager import ModuleCollection


def pathto(basedir, relpath):
    path = os.path.join(basedir, relpath)
    return os.path.normpath(path)


class ModuleCollectionTest(unittest.TestCase):

    def setUp(self):
        this_folder = os.path.split(os.path.realpath(__file__))[0]
        self.folder = os.path.normpath(os.path.join(this_folder, os.pardir))

    def test_module_collection_collects_baseUrl(self):
        config = json.loads("""{
            "appDir": "tests/cases/no-paths",
            "baseUrl": "js/lib",
            "paths": {}
        }""")

        basedir = os.path.join(self.folder, config['appDir'], config['baseUrl'])
        basedir = os.path.normpath(basedir)
        module_collection = ModuleCollection(self.folder, config)

        self.assertItemsEqual(module_collection.items, [
            ('a', pathto(basedir, 'a.js')),
            ('b', pathto(basedir, 'b.js')),
            ('c', pathto(basedir, 'c.js')),
        ])

        self.assertItemsEqual(module_collection.keys, ['a', 'b', 'c'])

        self.assertItemsEqual(module_collection.values, [
            pathto(basedir, 'a.js'),
            pathto(basedir, 'b.js'),
            pathto(basedir, 'c.js'),
        ])

    def test_module_collection_collects_paths(self):
        config = json.loads("""{
            "appDir": "tests/cases/paths-only",
            "baseUrl": "js/lib",
            "paths": {
                "app": "../app"
            }
        }""")

        module_collection = ModuleCollection(self.folder, config)

        self.assertItemsEqual(module_collection.items, [
            ('app/main', pathto(module_collection.basedir, '../app/main.js')),
        ])

        self.assertItemsEqual(module_collection.ids, ['app/main'])

        self.assertItemsEqual(module_collection.resources, [
            pathto(module_collection.basedir, '../app/main.js'),
        ])

    def test_module_collection_collects_path_module(self):
        config = json.loads("""{
            "appDir": "tests/cases/paths-only",
            "baseUrl": "js/lib",
            "paths": {
                "main": "../app/main.js"
            }
        }""")

        module_collection = ModuleCollection(self.folder, config)

        self.assertItemsEqual(module_collection.items, [
            ('main', pathto(module_collection.basedir, '../app/main.js')),
        ])

        self.assertItemsEqual(module_collection.ids, ['main'])

        self.assertItemsEqual(module_collection.resources, [
            pathto(module_collection.basedir, '../app/main.js'),
        ])

    def test_module_collection_collects_nonjs_with_ext(self):
        config = json.loads("""{
            "appDir": "tests/cases/path-only-with-nonjs",
            "baseUrl": "js/lib",
            "paths": {
                "hbs": "../../hbs"
            }
        }""")

        module_collection = ModuleCollection(self.folder, config)

        self.assertItemsEqual(module_collection.items, [
            ('hbs/a.hbs', pathto(module_collection.basedir, '../../hbs/a.hbs')),
        ])

        self.assertItemsEqual(module_collection.ids, ['hbs/a.hbs'])

        self.assertItemsEqual(module_collection.resources, [
            pathto(module_collection.basedir, '../../hbs/a.hbs'),
        ])

    def test_module_collection_collects_all(self):
        config = json.loads("""{
            "appDir": "tests/cases/www",
            "baseUrl": "js/lib",
            "paths": {
                "app": "../app",
                "util": "../util",
                "common": "../util/common",
                "d": "../util/common/d.js",
                "hbs": "../../hbs"
            }
        }""")

        module_collection = ModuleCollection(self.folder, config)

        self.assertItemsEqual(module_collection.items, [
            ('a', pathto(module_collection.basedir, 'a.js')),
            ('b', pathto(module_collection.basedir, 'b.js')),
            ('c', pathto(module_collection.basedir, 'c.js')),
            ('app/main', pathto(module_collection.basedir, '../app/main.js')),
            ('util/main', pathto(module_collection.basedir, '../util/main.js')),
            ('util/common/d', pathto(module_collection.basedir, '../util/common/d.js')),
            ('common/d', pathto(module_collection.basedir, '../util/common/d.js')),
            ('d', pathto(module_collection.basedir, '../util/common/d.js')),
            ('hbs/index.hbs', pathto(module_collection.basedir, '../../hbs/index.hbs')),
        ])

        self.assertItemsEqual(module_collection.ids, [
            'a',
            'b',
            'c',
            'app/main',
            'util/main',
            'util/common/d',
            'common/d',
            'd',
            'hbs/index.hbs',
        ])

        self.assertItemsEqual(module_collection.resources, [
            pathto(module_collection.basedir, 'a.js'),
            pathto(module_collection.basedir, 'b.js'),
            pathto(module_collection.basedir, 'c.js'),
            pathto(module_collection.basedir, '../app/main.js'),
            pathto(module_collection.basedir, '../util/main.js'),
            pathto(module_collection.basedir, '../util/common/d.js'),
            pathto(module_collection.basedir, '../util/common/d.js'),
            pathto(module_collection.basedir, '../util/common/d.js'),
            pathto(module_collection.basedir, '../../hbs/index.hbs'),
        ])


if __name__ == '__main__':
	unittest.main()
