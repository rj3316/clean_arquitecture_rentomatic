import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Base configuration"""

class ConfigProduction(Config):
    """Production configuration"""

class ConfigDevelopment(Config):
    """Development configuration"""

class ConfigTesting(Config):
    """Testing configuration"""
    TESTING = True