import logging
import os

from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)


class PortfolioSiteConfig(AppConfig):
    name = 'portfolio_site'
    verbose_name = 'Portfolio site application'

    def ready(self):
        if settings.DEBUG and os.environ.get('RUN_MAIN') == 'true':
            try:
                from portfolio_site.mock_mail_server import mock_server
                settings.EMAIL_HOST = 'localhost'
                settings.EMAIL_PORT = mock_server.port
            except ImportError as ex:
                logger.warn(f'Failed to start mock mail server due to missing package: {ex.name}')
