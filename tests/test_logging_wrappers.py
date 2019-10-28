import logging
import unittest
import pathlib
import shutil

from logging_wrappers import loggingWrappers


class getLogger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        output = pathlib.Path(__file__).parent
        cls.logger, cls.output = loggingWrappers.getLogger(output)
        cls.logger.debug('test')
        cls.logger.info('test')

    @classmethod
    def tearDownClass(cls):
        for handler in cls.logger.handlers:
            if type(handler) is logging.FileHandler:
                handler.close()
        shutil.rmtree(cls.output)

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
