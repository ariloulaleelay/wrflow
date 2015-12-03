import unittest
from wrflow.config import default_config

class TestConfig(unittest.TestCase):

    def test_config(self):
        config = default_config()
        self.assertEqual(config.wrflow.test.boolean_value_true.as_bool, True)
        self.assertEqual(config.wrflow.test.boolean_value_false.as_bool, False)

if __name__ == '__main__':
    unittest.main()
