import unittest
import os.path
from module_collection import ModuleCollection


class ModuleCollectionTest(unittest.TestCase):

    def __basepath(self, config):
        return os.path.join(self.folder, config['appDir'], config['baseUrl'])

    def __pathto(self, config, relpath):
        path = os.path.join(self.__basepath(config), relpath)
        return os.path.normpath(path)

    def setUp(self):
        this_folder = os.path.split(os.path.realpath(__file__))[0]
        self.folder = os.path.normpath(os.path.join(this_folder, os.pardir))

    def test_module_collection_collects_baseUrl(self):
        config = {
            'appDir': 'tests/cases/www-lib-only',
            'baseUrl': 'js/lib',
            'paths': {}
        }
        module_collection = ModuleCollection(self.folder, config)

        self.assertItemsEqual(module_collection.items(), [
            ('backbone', self.__pathto(config, 'backbone.js')),
            ('jquery', self.__pathto(config, 'jquery.js')),
            ('require', self.__pathto(config, 'require.js')),
            ('underscore', self.__pathto(config, 'underscore.js'))])

        self.assertItemsEqual(module_collection.ids(), [
            'backbone',
            'jquery',
            'require',
            'underscore'])

        self.assertItemsEqual(module_collection.resources(), [
            self.__pathto(config, 'backbone.js'),
            self.__pathto(config, 'jquery.js'),
            self.__pathto(config, 'require.js'),
            self.__pathto(config, 'underscore.js')])

    def test_module_collection_collects_paths(self):
        config = {
            'appDir': 'tests/cases/www-path-only',
            'baseUrl': 'js/lib',
            'paths': {
                'app': '../app',
            }
        }
        module_collection = ModuleCollection(self.folder, config)

        self.assertItemsEqual(module_collection.items(), [
            ('app/main', self.__pathto(config, '../app/main.js'))])

        self.assertItemsEqual(module_collection.ids(), ['app/main'])

        self.assertItemsEqual(module_collection.resources(), [
            self.__pathto(config, '../app/main.js')])

    def test_module_collection_collects_path_file(self):
        config = {
            'appDir': 'tests/cases/www-path-only',
            'baseUrl': 'js/lib',
            'paths': {
                'main': '../app/main.js'
            }
        }
        module_collection = ModuleCollection(self.folder, config)

        self.assertItemsEqual(module_collection.items(), [
            ('main', self.__pathto(config, '../app/main.js'))])

        self.assertItemsEqual(module_collection.ids(), ['main'])

        self.assertItemsEqual(module_collection.resources(), [
            self.__pathto(config, '../app/main.js')])

    def test_module_collection_collects_nonjs_with_ext(self):
        config = {
            'appDir': 'tests/cases/www-path-only-nonjs',
            'baseUrl': 'js/lib',
            'paths': {
                'templates': '../../templates'
            }
        }
        module_collection = ModuleCollection(self.folder, config)

        self.assertItemsEqual(module_collection.items(), [
            ('templates/index.hbs', self.__pathto(config, '../../templates/index.hbs'))])

        self.assertItemsEqual(module_collection.ids(), ['templates/index.hbs'])

        self.assertItemsEqual(module_collection.resources(), [
            self.__pathto(config, '../../templates/index.hbs')])

    def test_module_collection_collects_all(self):
        config = {
            'appDir': 'tests/cases/www',
            'baseUrl': 'js/lib',
            'paths': {
                'app': '../app',
                'util': '../util',
                'common': '../util/common',
                'print': '../util/common/print.js',
                'templates': '../../templates'
            }
        }
        module_collection = ModuleCollection(self.folder, config)

        self.assertItemsEqual(module_collection.items(), [
            ('backbone', self.__pathto(config, 'backbone.js')),
            ('jquery', self.__pathto(config, 'jquery.js')),
            ('require', self.__pathto(config, 'require.js')),
            ('underscore', self.__pathto(config, 'underscore.js')),
            ('app/main', self.__pathto(config, '../app/main.js')),
            ('util/main', self.__pathto(config, '../util/main.js')),
            ('util/common/print', self.__pathto(config, '../util/common/print.js')),
            ('common/print', self.__pathto(config, '../util/common/print.js')),
            ('print', self.__pathto(config, '../util/common/print.js')),
            ('templates/index.hbs', self.__pathto(config, '../../templates/index.hbs'))])

        self.assertItemsEqual(module_collection.ids(), [
            'backbone',
            'jquery',
            'require',
            'underscore',
            'app/main',
            'util/main',
            'util/common/print',
            'common/print',
            'print',
            'templates/index.hbs'])

        self.assertItemsEqual(module_collection.resources(), [
            self.__pathto(config, 'backbone.js'),
            self.__pathto(config, 'jquery.js'),
            self.__pathto(config, 'require.js'),
            self.__pathto(config, 'underscore.js'),
            self.__pathto(config, '../app/main.js'),
            self.__pathto(config, '../util/main.js'),
            self.__pathto(config, '../util/common/print.js'),
            self.__pathto(config, '../util/common/print.js'),
            self.__pathto(config, '../util/common/print.js'),
            self.__pathto(config, '../../templates/index.hbs')])


if __name__ == '__main__':
	unittest.main()
