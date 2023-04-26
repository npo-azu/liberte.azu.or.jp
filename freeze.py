#----------------------------------------------------------
# Import
#----------------------------------------------------------
# Standard library

# Additional library
import flask_frozen

# Original library
import lib.log

# Other module
import view
import env
import model


#----------------------------------------------------------
# Init
#----------------------------------------------------------
lib.log.init(debug=env.DEBUG)
_logger = lib.log.get_logger(__name__)

_freezer = flask_frozen.Freezer(view.app)
view.app.config['FREEZER_RELATIVE_URLS'] = True


#----------------------------------------------------------
# URL generators
#----------------------------------------------------------
@_freezer.register_generator
def product_url_generator():
    for page_item in model.get_pages():
        yield 'view_page', {'page_name': page_item['id']}
    for study_item in model.get_study():
        yield 'view_study', {'id': study_item['id']}
    yield 'view_404', {}
    yield 'view_top', {}
    yield 'view_style', {}


#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main():
    _freezer.freeze()

if __name__ == '__main__':
    main()
