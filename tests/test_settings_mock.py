import unittest
from mocks import SettingsMock


class SettingsMockTest(unittest.TestCase):

    def setUp(self):
        self.requirejs_config = {
            'appDir': 'tests/www',
            'baseUrl': 'js/lib',
            'paths': {
                'app': '../app',
                'util': '../util',
                'common': '../util/common',
                'print': '../util/common/print.js'
            }
        }
        self.settings = SettingsMock({
            'requirejs_config': self.requirejs_config
        })

    def test_get_setting(self):
        self.assertEqual(
            self.settings.get('requirejs_config'), self.requirejs_config)

    def test_get_setting_with_default(self):
        self.assertEqual(self.settings.get('foo', 'bar'), 'bar')

    def test_set_setting(self):
        self.settings.set('requirejs_config', {})
        self.assertEqual(self.settings.get('requirejs_config'), {})

if __name__ == '__main__':
    unittest.main()
