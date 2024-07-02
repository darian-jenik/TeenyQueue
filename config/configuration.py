# config/configuration.py
#
# This is my preferred way of handling configuration and logging.
# IF you don't like it then that's nice but don't message me.
#
# Don't forget to set the environment variable TQ_CONFIG_LOCATION to pick up your config.  Default is ./config.yaml
# Also, don't store passwords in the config file.
# Use environment variables names in the config file where the password should be. e.g.
# config:
#   postgres:
#     my_db_password: $MY_DB_PASSWORD

import os
import yaml
import string
import random
from datetime import datetime
from logging.config import dictConfig
import logging

from config.log_configuration import loggingConfig, LOG_FORMAT
from config.custom_logger import CustomLogger


class TQExceptionStop(Exception):
    def __init__(self, msg):
        try:
            msg = f'[{env.RUNID}] {msg}'
        except NameError:
            pass
        super().__init__(msg)


class TQEnvironment:

    _instance = None        # Singleton
    _initialized = False

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __getattr__(self, name):
        return_a_dict = ['databases', 'postgres', 'mongo', 'logging', 'config']
        if name in return_a_dict:
            if hasattr(self, 'log'):
                self.log.error(f"Attribute '{name}' not found in env.  Returning empty dict.")
            return {}
        else:
            if hasattr(self, 'log'):
                self.log.error(f"Attribute '{name}' not found in env.  Returning None.")
            return None

    def __init__(self, *args, **kwargs):

        if self.__class__._initialized:
            return
        else:
            super().__init__(*args, **kwargs)
            self.__class__._initialized = True

        self._raw_config = {}
        self.log_level = "INFO"
        self.RUNID = 'TEENYQUEUE'

        logging.setLoggerClass(CustomLogger)
        dictConfig(loggingConfig)
        self.log = logging.getLogger('root')

        self.log.info('Initializing environment.')

        self.get_config()

        self.DEBUG = self.startup.get('debug', False)

        self.setup_logging()

        self.log.debug(f'Running as UID: {str(os.getuid())} GID {str(os.getgid())}')

    def setup_logging(self) -> None:
        """
        The log-level logic in this is a bit messed up... \n
        Priority is: \n
            1. Environment variable TQ_LOG_LEVEL \n
            2. If the config file has a log level in the logging: section.\n
            3. If self.DEBUG is set. \n
            4. Default to INFO \n
        Also the local_log_dir is:
            1. local_log_dir in the config file section of logging: \n
            2. Defaults to .
        :return:
        """

        if os.environ.get('TQ_LOG_LEVEL', None):     # Priority is env vars
            self.log_level = os.environ.get('TQ_LOG_LEVEL', 'INFO').upper()

        else:
            log_level = 'INFO'
            if self.DEBUG:
                log_level = 'DEBUG'
            if self.logging.get('log_level', None):
                log_level = self.logging['log_level'].upper()

            logger = logging.getLogger('root')
            logger.setLevel(getattr(logging, log_level))
            for handler in logger.handlers:
                handler.setLevel(log_level)

        local_log_dir = self.logging.get('local_log_dir', '.')

        if os.path.isdir(local_log_dir) and os.access(local_log_dir, os.W_OK):

            log_file = str(os.path.join(local_log_dir, self.logging.get('log_filename', 'main.log')))

            file_handler = logging.FileHandler(log_file, 'w')

            file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

            logger = logging.getLogger('root')
            logger.addHandler(file_handler)

            CustomLogger._log_header = f'[{self.RUNID}]'
            self.log.debug(f'log_file: {log_file=} is now logging.')

    # ---------------------------------------------------------------------------------------------
    def get_config(self) -> None:
        """
        Find the config location:  First try the environment variable CD_CONFIG_LOCATION,
        if that fails, try the default location./config/config.yaml.
        - If a file is found then load it into self._raw_config
        - Create the env attributes
        - Get the RUNID else create one with identify_run_id()
        - Get any environment variables for the config file with get_env_vars_for_config()
        :return: None
        """

        config_location = os.environ.get('TQ_CONFIG_LOCATION', './config.yaml')

        try:
            with open(config_location, 'r') as f:

                self._raw_config = yaml.safe_load(f)
                self.log.info(f'Found config file at {config_location}')

        except FileNotFoundError:
            self.log.critical(f'Could not find config file at {config_location}!')
            exit()  # No point continuing
        except Exception as e:
            self.log.critical(f'Exception reading config file at {config_location}! {e}')
            exit()  # No point continuing

        # Create attributes for the config headings.
        for key in self._raw_config.keys():
            setattr(self, key, self._raw_config[key])

        self.identify_run_id()
        self.get_env_vars_for_config(self._raw_config)

    def identify_run_id(self) -> None:
        """
        Look for the RUNID in the config file.
        - If a RUNID is found then insert our own module_name.
        - If RUNID is not found then generate a new one.
        - Add the RUNID to MongoHandler.RUNID
        :return: None
        """

        startup_config = self._raw_config.setdefault('startup', {})
        self.RUNID = startup_config.get('run_id', False)

        if not self.RUNID:
            self.log.debug('No run_id specified in config file.')
        else:
            self.log.info(f'Got run_id: {self.RUNID} from config file.')

        if isinstance(self.RUNID, str):
            run_id_list = self.RUNID.split('_')
            if len(run_id_list) >= 4:
                run_id_list[3] = startup_config.get('module_name', 'UNKNOWN')
            else:
                run_id_list.append(startup_config.get('module_name', 'UNKNOWN'))
            self.RUNID = '_'.join(run_id_list)
            self.log.info(f'Using run_id: {self.RUNID}')
        else:
            self.log.debug('Generating a new run_id...')
            self.RUNID = self.generate_new_run_id(startup_config)
            self.log.info(f'Using run_id: {self.RUNID}')

    @staticmethod
    def generate_new_run_id(startup_config: dict) -> str:
        alphabet = string.ascii_lowercase + string.digits
        current_time = datetime.now().strftime('%m%d%H%M%S')
        random_id = ''.join(random.choices(alphabet, k=8))
        module_name = startup_config.get('module_name', 'UNKNOWN')
        return f'{current_time}_{random_id}_{module_name}'

    def get_env_vars_for_config(self, config: dict, depth: int = 0) -> None:  # Keep config here as this is a recursive call.
        """
        Troll through the config for any variables that start with $
        - If a variable is found then replace the value with the value from the environment variable
        :param depth:
        :param config:
        :return:
        """
        env_cache = os.environ.copy()

        if depth > 5:
            raise TQExceptionStop('get_env_vars_for_config: Config depth exceeded 5!')

        for key, value in config.items():
            if isinstance(value, dict):
                self.get_env_vars_for_config(value, depth=depth + 1)
            elif isinstance(value, str) and value.startswith('$'):
                env_var = value[1:]
                if env_var in env_cache:
                    config[key] = env_cache[env_var]
                else:
                    # Ughh.. not sure if it is better to raise an exception here or just create a blank string.  For now..
                    raise TQExceptionStop(f'Environment variable ${env_var} not found')


env = TQEnvironment()


if __name__ == '__main__':
    exit()

# end
