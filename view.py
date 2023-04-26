#----------------------------------------------------------
# Import
#----------------------------------------------------------
# Standard library
import os

# Additional library
import flask
import sass

# Original library
import lib.log

# Other module
import env
import model


#----------------------------------------------------------
# Init
#----------------------------------------------------------
lib.log.init(debug=env.DEBUG)
_logger = lib.log.get_logger(__name__)

app = flask.Flask(__name__, template_folder='template', static_folder='static')

app.add_template_filter(model.convert_markdown, name='markdown')
app.add_template_filter(model.convert_nl2br, name='nl2br')
app.add_template_filter(model.convert_nl2pbr, name='nl2pbr')

#----------------------------------------------------------
# Set Globals and filter
#----------------------------------------------------------
@app.context_processor
def set_globals():
    ret = {
        'config': model.get_config(),
        'pages': model.get_pages(),
        'study': model.get_study(),
    }
    return ret


#----------------------------------------------------------
# Route
#----------------------------------------------------------
@app.route('/index.html', methods=['GET'])
def view_top():
    config = model.get_config()
    data = {
        'is_top': True,
        'config': {
            'bg_color': config['top']['bg_color'],
            'fg_color': config['top']['fg_color'],
            'footer_color': config['top']['footer_color'],
            'bg_img': config['top'].get('bg_img'),
        },
    }
    return flask.render_template('top.html', data=data)


@app.route('/<page_name>.html', methods=['GET'])
def view_page(page_name):
    data = [i for i in model.get_pages() if i['id'] == page_name][0]

    return flask.render_template('page.html', data=data)


@app.route('/study/<id>.html', methods=['GET'])
def view_study(id):
    config = model.get_config();
    data = [i for i in model.get_study() if i['id'] == id][0]
    data.update({
        'config': {
            'bg_color': config['study_archive']['bg_color'],
            'fg_color': config['study_archive']['fg_color'],
            'icon': config['study_archive']['icon'],
            'bg_img': config['study_archive'].get('bg_img'),
        }
    })
    return flask.render_template('study.html', data=data)


@app.route('/404.html', methods=['GET'])
def view_404():
    return flask.render_template('404.html')


@app.route('/style.css', methods=['GET'])
def view_style():
    css = sass.compile( string=flask.render_template('style.scss') )
    return flask.Response(css, mimetype='text/css')


#----------------------------------------------------------
# for Debug
#----------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
