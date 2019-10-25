import unittest
import pathlib
from log import Log


def main():
    log_dir = pathlib.Path(__file__).parent
    logger = Log(True).getLogger(log_dir)
    logger.debug(f'test_debug')
    logger.info(f'test_info')


class LogTest(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
