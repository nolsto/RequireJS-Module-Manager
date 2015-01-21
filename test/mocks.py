class SettingsMock:

    def __init__(self, settings):
        self.settings = settings

    def get(self, name, default=None):
        if name not in self.settings:
            return default
        else:
            return self.settings[name]

    def set(self, name, val):
        self.settings[name] = val
