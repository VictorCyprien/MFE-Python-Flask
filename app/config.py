from environs import Env


class Config:

    def __init__(self):
        env = Env()

        self.SERVICE_NAME = 'MFE Python-Flask'
        self.LOGGER_LEVEL = env.str("LOGGER_LEVEL", "INFO")

        # FLASK
        self.FLASK_ENV = env.str('FLASK_ENV', 'dev')
        self.JSON_SORT_KEYS = True

        # MONGODB
        self.MONGODB_URI = env.str('MONGODB_URI', 'mongodb://localhost:27017')
        self.MONGODB_DATABASE = env.str('MONGODB_DATABASE', 'mfe-python-flask')
        self.MONGODB_CONNECT = False

        # PASSWORD CUSTOM SALT
        self.SECURITY_PASSWORD_SALT = env.str('SECURITY_PASSWORD_SALT', "672B2BB59D2E432E8F3FB10E23B8AECC")


    @property
    def mongodb_settings(self):
        return {
            'host': f'{self.MONGODB_URI}/{self.MONGODB_DATABASE}',
            'db': self.MONGODB_DATABASE,
            'connect': self.MONGODB_CONNECT,
        }

    @property
    def logger_config(self):
        return {
            'version': 1,
            'formatters': {
                'color_formatter': {
                    '()': 'colorlog.ColoredFormatter',
                    'format': "%(log_color)s%(asctime)s | %(levelname)-8s | %(message)s"
                }
            },
            'handlers': {
                'console': {
                    'class': 'colorlog.StreamHandler',
                    'level': self.LOGGER_LEVEL,
                    'formatter': 'color_formatter'
                },
            },
            'loggers': {
                'console': {
                    'level': self.LOGGER_LEVEL,
                    'propagate': False,
                    'handlers': ['console']
                }
            }
        }

    @property
    def json(self):
        return {key: self.__getattribute__(key) for key in self.__dir__() if not key.startswith('_') and key.isupper()}

    def validate(self):
        if not self.MONGODB_URI:
            raise ValueError("Mongo URI is not defined")


config = Config()
