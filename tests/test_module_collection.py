import json
import os.path
import unittest

from module_collection import ModuleCollection


def pathto(basedir, relpath):
    path = os.path.join(basedir, relpath)
    return os.path.normpath(path)


class ModuleCollectionTest(unittest.TestCase):

    def setUp(self):
        this_folder = os.path.split(os.path.realpath(__file__))[0]
        self.folder = os.path.normpath(os.path.join(this_folder, os.pardir))

    def test_module_collection_collects_baseUrl(self):
        config = json.loads("""{
            "appDir": "tests/cases/www-lib-only",
            "baseUrl": "js/lib",
            "paths": {}
        }""")

        module_collection = ModuleCollection(self.folder, config)

        self.assertItemsEqual(module_collection.items, [
            ('backbone', pathto(module_collection.basedir, 'backbone.js')),
            ('jquery', pathto(module_collection.basedir, 'jquery.js')),
            ('require', pathto(module_collection.basedir, 'require.js')),
            ('underscore', pathto(module_collection.basedir, 'underscore.js')),
        ])

        self.assertItemsEqual(module_collection.ids, [
            'backbone',
            'jquery',
            'require',
            'underscore',
        ])

        self.assertItemsEqual(module_collection.resources, [
            pathto(module_collection.basedir, 'backbone.js'),
            pathto(module_collection.basedir, 'jquery.js'),
            pathto(module_collection.basedir, 'require.js'),
            pathto(module_collection.basedir, 'underscore.js'),
        ])

    def test_module_collection_collects_paths(self):
        config = json.loads("""{
            "appDir": "tests/cases/www-path-only",
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
            "appDir": "tests/cases/www-path-only",
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
            "appDir": "tests/cases/www-path-only-nonjs",
            "baseUrl": "js/lib",
            "paths": {
                "templates": "../../templates"
            }
        }""")

        module_collection = ModuleCollection(self.folder, config)

        self.assertItemsEqual(module_collection.items, [
            ('templates/index.hbs', pathto(module_collection.basedir, '../../templates/index.hbs')),
        ])

        self.assertItemsEqual(module_collection.ids, ['templates/index.hbs'])

        self.assertItemsEqual(module_collection.resources, [
            pathto(module_collection.basedir, '../../templates/index.hbs'),
        ])

    def test_module_collection_collects_all(self):
        config = json.loads("""{
            "appDir": "tests/cases/www",
            "baseUrl": "js/lib",
            "paths": {
                "app": "../app",
                "util": "../util",
                "common": "../util/common",
                "print": "../util/common/print.js",
                "templates": "../../templates"
            }
        }""")

        module_collection = ModuleCollection(self.folder, config)

        self.assertItemsEqual(module_collection.items, [
            ('backbone', pathto(module_collection.basedir, 'backbone.js')),
            ('jquery', pathto(module_collection.basedir, 'jquery.js')),
            ('require', pathto(module_collection.basedir, 'require.js')),
            ('underscore', pathto(module_collection.basedir, 'underscore.js')),
            ('app/main', pathto(module_collection.basedir, '../app/main.js')),
            ('util/main', pathto(module_collection.basedir, '../util/main.js')),
            ('util/common/print', pathto(module_collection.basedir, '../util/common/print.js')),
            ('common/print', pathto(module_collection.basedir, '../util/common/print.js')),
            ('print', pathto(module_collection.basedir, '../util/common/print.js')),
            ('templates/index.hbs', pathto(module_collection.basedir, '../../templates/index.hbs')),
        ])

        self.assertItemsEqual(module_collection.ids, [
            'backbone',
            'jquery',
            'require',
            'underscore',
            'app/main',
            'util/main',
            'util/common/print',
            'common/print',
            'print',
            'templates/index.hbs',
        ])

        self.assertItemsEqual(module_collection.resources, [
            pathto(module_collection.basedir, 'backbone.js'),
            pathto(module_collection.basedir, 'jquery.js'),
            pathto(module_collection.basedir, 'require.js'),
            pathto(module_collection.basedir, 'underscore.js'),
            pathto(module_collection.basedir, '../app/main.js'),
            pathto(module_collection.basedir, '../util/main.js'),
            pathto(module_collection.basedir, '../util/common/print.js'),
            pathto(module_collection.basedir, '../util/common/print.js'),
            pathto(module_collection.basedir, '../util/common/print.js'),
            pathto(module_collection.basedir, '../../templates/index.hbs'),
        ])

    def test_module_collection_collects_all_from_json_config_file(self):
        config = u'./tests/cases/tools/build.json'

        module_collection = ModuleCollection(self.folder, config)

        self.assertItemsEqual(module_collection.items, [
            ('backbone', pathto(module_collection.basedir, 'backbone.js')),
            ('jquery', pathto(module_collection.basedir, 'jquery.js')),
            ('require', pathto(module_collection.basedir, 'require.js')),
            ('underscore', pathto(module_collection.basedir, 'underscore.js')),
            ('app/main', pathto(module_collection.basedir, '../app/main.js')),
            ('util/main', pathto(module_collection.basedir, '../util/main.js')),
            ('util/common/print', pathto(module_collection.basedir, '../util/common/print.js')),
            ('common/print', pathto(module_collection.basedir, '../util/common/print.js')),
            ('print', pathto(module_collection.basedir, '../util/common/print.js')),
            ('templates/index.hbs', pathto(module_collection.basedir, '../../templates/index.hbs')),
        ])

        self.assertItemsEqual(module_collection.ids, [
            'backbone',
            'jquery',
            'require',
            'underscore',
            'app/main',
            'util/main',
            'util/common/print',
            'common/print',
            'print',
            'templates/index.hbs',
        ])

        self.assertItemsEqual(module_collection.resources, [
            pathto(module_collection.basedir, 'backbone.js'),
            pathto(module_collection.basedir, 'jquery.js'),
            pathto(module_collection.basedir, 'require.js'),
            pathto(module_collection.basedir, 'underscore.js'),
            pathto(module_collection.basedir, '../app/main.js'),
            pathto(module_collection.basedir, '../util/main.js'),
            pathto(module_collection.basedir, '../util/common/print.js'),
            pathto(module_collection.basedir, '../util/common/print.js'),
            pathto(module_collection.basedir, '../util/common/print.js'),
            pathto(module_collection.basedir, '../../templates/index.hbs'),
        ])


if __name__ == '__main__':
	unittest.main()
