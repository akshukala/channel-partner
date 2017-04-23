import os
import logging

from cpdservice.conf.environments import get_config

log_format = ' '.join([
    '[%(asctime)s]',
    '[%(process)d-%(thread)d]',
    '%(levelname)s',
    '-',
    '%(message)s'
])

formatter = logging.Formatter(log_format)

def setup_config_logger(app):
    app.secret_key = "11ca4c58-90ab-46c6-bf1c-d26e626f0d74"
    agro_env = os.environ.get('AGRO_ENV', 'development')
    config = get_config(agro_env)
    app.config.from_object(config)
    app.debug_log_format = log_format

    if not app.debug:
        logHandler = logging.StreamHandler()

        logHandler.setFormatter(formatter)
        logHandler.setLevel(logging.DEBUG)
        app.logger.addHandler(logHandler)
        app.logger.setLevel(logging.DEBUG)

    app.logger.info("Loaded environment: " + agro_env)
