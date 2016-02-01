from unittest import TestCase


class StatsTestCase(TestCase):
    def assert_renders_similar(self, item1, item2):
        self.assertEqual(item1.__repr__(), item2.__repr__())
