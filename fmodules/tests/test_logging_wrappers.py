import unittest
import pathlib
import tempfile
import shutil
import logging

from logging_wrappers import loggingWrappers


class getLogger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent_dir = pathlib.Path(__file__).parent
        cls.temp_dir = pathlib.Path(tempfile.mkdtemp(dir=parent_dir))
        cls.logger_nomal, cls.log_file = loggingWrappers.getLogger(f'{__name__}_Nomal', cls.temp_dir)
        cls.logger_debug, _ = loggingWrappers.getLogger(f'{__name__}_Debug')

    @classmethod
    def tearDownClass(cls):
        for handler in cls.logger_nomal.handlers:
            if type(handler) is logging.FileHandler:
                handler.close()
        shutil.rmtree(cls.temp_dir)

    def test_nomal_mode_logger_outputs_level_info_or_higher_logs(self):
        with self.assertLogs(self.logger_nomal, 'INFO') as cm:
            self.logger_nomal.debug('debug')
            self.logger_nomal.info('info')
            self.logger_nomal.warning('warning')
            self.logger_nomal.error('error')
            self.logger_nomal.critical('critical')
        output = ' '.join(cm.output)
        self.assertEqual([
            output.count('DEBUG'),
            output.count('INFO'),
            output.count('WARNING'),
            output.count('ERROR'),
            output.count('CRITICAL'),
        ], [0, 1, 1, 1, 1])

    def test_debug_mode_logger_outputs_all_level_logs(self):
        with self.assertLogs(self.logger_debug, 'DEBUG') as cm:
            self.logger_debug.debug('debug')
            self.logger_debug.info('info')
            self.logger_debug.warning('warning')
            self.logger_debug.error('error')
            self.logger_debug.critical('critical')
        output = ' '.join(cm.output)
        self.assertEqual([
            output.count('DEBUG'),
            output.count('INFO'),
            output.count('WARNING'),
            output.count('ERROR'),
            output.count('CRITICAL'),
        ], [1, 1, 1, 1, 1])

    def test_generates_log_directory(self):
        self.assertTrue(self.log_file.exists())


if __name__ == '__main__':
    unittest.main()
