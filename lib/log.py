import sys
import logging

def init(debug=False):
    logging.getLogger('').handlers.clear()

    disp_handler = logging.StreamHandler(sys.stdout)
    format_str = '[%(module)s.%(funcName)s] %(levelname)s: %(message)s'
    if debug:
        format_str = '[%(module)s.%(funcName)s(ln:%(lineno)d)] %(levelname)s: %(message)s'
    disp_handler.setFormatter( logging.Formatter(format_str) )
    disp_handler.setLevel( logging.DEBUG if debug else logging.INFO )

    logging.getLogger('').addHandler(disp_handler)
    1

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    return logger
