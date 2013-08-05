import json
import unittest

from mocks import SettingsMock


class SettingsMockTest(unittest.TestCase):

    def setUp(self):
        self.setting_a = {'attr': 'value'}
        self.setting_a_key = 'setting_a'

        self.settings = SettingsMock({
            'setting_a': self.setting_a,
            'setting_a_key': self.setting_a_key,
        })

    def test_get_setting(self):
        self.assertEqual(self.settings.get('setting_a'), self.setting_a)

    def test_get_setting_with_default(self):
        self.assertEqual(self.settings.get('foo', 'bar'), 'bar')

    def test_set_setting(self):
        self.settings.set('setting_a', {})
        self.assertEqual(self.settings.get('setting_a'), {})

    def test_setting_references_setting_key(self):
        key = self.settings.get('setting_a_key')
        self.assertEqual(self.settings.get(key), self.setting_a)


if __name__ == '__main__':
    unittest.main()
