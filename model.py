#----------------------------------------------------------
# Import
#----------------------------------------------------------
# Standard library
import re
import tempfile
import os

# Additional library
import requests
import flask
import markdown

# Original library
import lib.log
import lib.microcms
import lib.obj_cache

# Other module
import env


#----------------------------------------------------------
# INIT
#----------------------------------------------------------
# Get logger
_logger = lib.log.get_logger(__name__)

_double_nl_re = re.compile(r'(\r\n|\n|\r){2,}')
_single_nl_re = re.compile(r'(\r\n|\n|\r)')

# Set define
_tmp_dir = tempfile.gettempdir()


#----------------------------------------------------------
# INIT
#----------------------------------------------------------
def convert_markdown(text):
    extensions = ['nl2br', 'def_list', 'attr_list']
    text = markdown.Markdown(extensions=extensions).convert(text)
    return flask.Markup(text)

def convert_nl2br(text):
    text = _single_nl_re.sub('<br>', text)
    return flask.Markup(text)

def convert_nl2pbr(text, class_name=None):
    p_tag = '<p>' if class_name is None else f'<p class="{class_name}">'
    text = _double_nl_re.sub(f'</p>{p_tag}', text)
    text = f'{p_tag}{text}</p>'
    text = _single_nl_re.sub('<br>', text)
    return flask.Markup(text)



#----------------------------------------------------------
# MicroCMS
#----------------------------------------------------------
_microcms = lib.microcms.MicroCMS(service_id=env.MICROCMS_ID, api_key=env.MICROCMS_KEY)

@lib.obj_cache.activate( os.path.join(_tmp_dir, 'pages'), 10 )
def get_pages():
    item_list = _microcms.get_list(api_name=env.MICROCMS_API_PAGES, limit=100)
    return item_list

@lib.obj_cache.activate( os.path.join(_tmp_dir, 'config'), 10 )
def get_config():
    item = _microcms.get_item(api_name=env.MICROCMS_API_CONFIG)
    return item

@lib.obj_cache.activate( os.path.join(_tmp_dir, 'study'), 10 )
def get_study():
    item_list = _microcms.get_list(api_name=env.MICROCMS_API_STUDY, limit=100)
    return item_list


#----------------------------------------------------------
# for DEBUG
#----------------------------------------------------------
if __name__ == '__main__':
    pass
