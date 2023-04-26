#----------------------------------------------------------
# Import
#----------------------------------------------------------
# Standard library
import os
import time
import pickle
import hashlib
import json
import logging
import inspect

# Additional library


#----------------------------------------------------------
# Init
#----------------------------------------------------------
# Get logger
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

# Add funcname prefix
class PrefixLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg: str, kwargs: dict) -> (str, dict):
        return ('[%s] %s' % (self.extra['func_info'], msg), kwargs)


#----------------------------------------------------------
# Activeate decorator
#----------------------------------------------------------
def activate(cache_path, valid_seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func_info = '%s.%s %s %s' % (func.__module__, func.__name__, args, kwargs)
            logger = PrefixLoggerAdapter(_logger, dict(func_info=func_info))

            refresh  = kwargs.pop('obj_cache_refresh', False)
            arg_hash = hashlib.md5((json.dumps(args, sort_keys=True) + json.dumps(kwargs, sort_keys=True)).encode()).hexdigest()
            path     = cache_path + '-' + arg_hash
            cached   = os.path.isfile(path)
            expired  = time.time() - os.stat(path).st_ctime > valid_seconds if cached else None

            if refresh or not cached or expired:
                try:
                    obj = func(*args, **kwargs)
                    with open(path, 'wb') as fp:
                        pickle.dump(obj, fp)
                        logger.debug('\033[91mSave cache\033[0m to %s', path)
                except Exception as e:
                    if refresh or not cached:
                        raise e
                    else:
                        logger.exception(e)
                else:
                    return obj

            with open(path, 'rb') as fp:
                logger.debug('\033[94mLoad cache\033[0m from %s ( %s > %s )', path, valid_seconds, time.time() - os.stat(path).st_ctime)
                return pickle.load(fp)

        return wrapper
    return decorator


#----------------------------------------------------------
# for Debug
#----------------------------------------------------------
if __name__ == '__main__':
    pass
