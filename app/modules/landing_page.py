from flask import Blueprint, render_template, request, send_from_directory

bp = Blueprint('landing', __name__)


@bp.after_request
def add_cache_control(response):
    if request.path.endswith('index.html'):
        response.cache_control.no_cache = True
    return response


@bp.route('/', defaults={'path': ''} )

@bp.route('/<path:path>')
def catch_all(path):
    try:
        return send_from_directory('dist', path)
    except:
        return send_from_directory('dist', 'index.html')
    
def index():
    return send_from_directory('dist', 'index.html')

@bp.route('/<path:path>')
def static_file(path):
    return send_from_directory('dist', path)
