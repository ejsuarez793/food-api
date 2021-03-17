"""
This config file is not being used currently, when it does, please complete this docstring
"""


class Config:  # https://stackoverflow.com/questions/4015417/why-do-python-classes-inherit-object
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
