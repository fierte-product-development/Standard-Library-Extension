import unittest
import pathlib

from subprocess_wrappers import subprocessWrappers
import pathlib_extensions  # noqa


class mkdir_hidden(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sdir = pathlib.Path(__file__).parent / 'test'
        cls.edir = cls.sdir.mkdir_hidden()

    @classmethod
    def tearDownClass(cls):
        cls.edir.rmdir()

    def test_first_character_of_directory_name_is_a_dot(self):
        edir = self.sdir.parent / f'.{self.sdir.name}'
        self.assertEqual(self.edir, edir)

    def test_directory_attribute_has_hidden_if_windows(self):
        if type(self.edir) == pathlib.WindowsPath:
            cp = subprocessWrappers.run('attrib', str(self.edir), shell=True)
            is_hidden = 'H' in cp.stdout.split()
        else:
            is_hidden = True
        self.assertTrue(is_hidden)


if __name__ == '__main__':
    unittest.main()
