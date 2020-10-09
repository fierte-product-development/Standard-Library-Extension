import unittest
import pathlib
import tempfile
import shutil

from ..subprocess_wrappers import subprocessWrappers
from .. import pathlib_extensions  # noqa


class mkdir_hidden(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent_dir = pathlib.Path(__file__).parent
        cls.temp_dir = pathlib.Path(tempfile.mkdtemp(dir=parent_dir))
        cls.sdir = cls.temp_dir / "test"
        cls.edir = cls.sdir.mkdir_hidden()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)

    def test_first_character_of_directory_name_is_a_dot(self):
        edir = self.sdir.parent / f".{self.sdir.name}"
        self.assertEqual(self.edir, edir)

    def test_directory_attribute_has_hidden_if_windows(self):
        if type(self.edir) == pathlib.WindowsPath:
            cp = subprocessWrappers.run("attrib", str(self.edir), shell=True)
            is_hidden = "H" in cp.stdout.split()
        else:
            is_hidden = True
        self.assertTrue(is_hidden)


if __name__ == "__main__":
    unittest.main()
