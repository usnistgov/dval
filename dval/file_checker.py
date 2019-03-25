# Contents subject to LICENSE.txt at project root

import logging
import os


class FileChecker(object):
    def __init__(self, path):
        self.path = path

    def _exists(self):
        if os.path.isfile(self.path):
            logging.debug("{} is a file.".format(self.path))
            return True
        else:
            logging.debug("{} is not a file.".format(self.path))
            return False

    def _readable(self):
        if os.access(self.path, os.R_OK):
            logging.debug("{} is readable.".format(self.path))
            return True
        else:
            logging.debug("{} is not readable.".format(self.path))
            return False

    def _executable(self):
        if os.access(self.path, os.X_OK):
            logging.debug("{} is executable.".format(self.path))
            return True
        else:
            logging.debug("{} is not executable.".format(self.path))
            return False

    def check_exists_read(self, variable_name=None):
        if not variable_name:
            variable_name = self.path

        message = "{}: {}".format(variable_name, self.path)
        if self._exists():
            if self._readable():
                logging.debug(message)
                return True
            else:
                message += " could not be read!"
                self._error(message)
        else:
            message += " is not a file!"
            self._error(message)

    def _error(self, message):
        logging.error(message)
        raise Exception
