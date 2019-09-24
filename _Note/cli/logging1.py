""r"""
https://docs.python.org/3/library/logging.html
https://docs.python.org/3/howto/logging.html#logging-basic-tutorial

debug(), info(), warning(), error() and critical()

"""

import logging

# logging.basicConfig()#level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

logging.debug('very detailed output for diagnostic purposes')
logging.info('Report events that occur during normal operation of a program (e.g. for status monitoring)')
logging.warning("warning message")

logger = logging.getLogger()
logger.info("first logger info message", )


text = "stnwfaei"
logging.debug("text = " + str(text))
logging.debug("text = " + text)


print("text = " + str(text))
