import logging.config
from django.conf import settings

logger = logging.getLogger('django')
logging.config.dictConfig(settings.LOGGING) # logging配置