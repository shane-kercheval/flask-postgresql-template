import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "postgresql://localhost/example_site") #defaults to localhost


class SiteConfig:
    # these config values are used in the templates (e.g. open graph, twitter)
    SITE_NAME = "EXAMPLE SITE"
    SITE_DESCRIPTION = "EXAMPLE SITE DESCRIPTION"
    SITE_KEYWORDS = "EXAMPLE KEYWORDS"
    SITE_OWNER = "SHANE KERCHEVAL"

    SITE_IMAGE = "img/logo.png"
    SITE_IMAGE_WIDTH = 600
    SITE_IMAGE_HEIGHT = 315

    SITE_TWITTER_USERNAME = "ShaneKercheval"


class ProductionConfig(Config, SiteConfig):
    DEBUG = False
    #uncomment to include GTM script in html pages
    #GOOGLE_TAG_MANAGER_ID = "GTM-XXXXXX"


class DevelopmentConfig(Config, SiteConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True #prints out the created queries to the terminal
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(Config):
    TEST_DATABASE_STRING = "test.db"
    DEBUG = True
    SQLALCHEMY_ECHO = False #prints out the created queries to the terminal
    SQLALCHEMY_TRACK_MODIFICATIONS = True

