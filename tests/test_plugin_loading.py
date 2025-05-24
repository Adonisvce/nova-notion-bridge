import unittest
from logic_engine.executor import LogicExecutor

class TestPluginLoading(unittest.TestCase):
    def test_plugins_load(self):
        executor = LogicExecutor()
        self.assertTrue(len(executor.plugins) > 0, "No plugins were loaded.")

if __name__ == '__main__':
    unittest.main()
