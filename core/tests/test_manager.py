import unittest

from core import Manager, Interface


class TestManager(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = Manager()

    def test_handler(self):
        @self.manager.handler()
        def handler_1():
            pass

        @self.manager.handler()
        def handler_1():
            pass

        self.manager.handlers


    def test_registry_handler(self):
        pass

    def test_command(self):
        pass

    def test_registry_command(self):
        pass
