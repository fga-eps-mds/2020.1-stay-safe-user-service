import logging
import os


def load_configuration():
    """
    Populates a dictionary with service settings. The settings are
    obtained through environment variables and, if it does not exist,
    of a constant value.
    """

    config = dict()
    config['debug'] = os.environ.get('DEBUG', True)
    config['host'] = os.environ.get('HOST', '0.0.0.0')
    config['port'] = int(os.environ.get('PORT', '8083'))

    return config

SECRET_KEY = os.environ.get('SECRET_KEY')

logging.basicConfig(
    format=('%(asctime)s,%(msecs)-3d - %(name)-12s - %(levelname)-8s => '
            '%(message)s'),
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)
