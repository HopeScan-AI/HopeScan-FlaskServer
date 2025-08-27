from flask import Blueprint, render_template, request, send_from_directory
        
bp = Blueprint('landing', __name__)

# @bp.get("/")
# def serve_landing_page():
#     role = request.args.get('role', 'user')
#     return render_template("landing-page.html", role=role)

@bp.after_request
def add_cache_control(response):
    if request.path.endswith('index.html'):
        response.cache_control.no_cache = True
    return response


@bp.route('/', defaults={'path': ''} )
# @bp.route('/cases')
# @bp.route('/dashboard/users')
# @bp.route('/dashboard/cases')
# @bp.route('/dashboard/providers')
# @bp.route('/dashboard/cases/:id')
# @bp.route('/dashboard/hope-images/all-images')
# @bp.route('/dashboard/hope-images/pending-diagnose')
# @bp.route('/dashboard/hope-images/images-results')
# @bp.route('/not-authorized')
# @bp.route('/dashboard/myDBA/show/:tableName')
# @bp.route('/dashboard/mydba')
# @bp.route('/diagnose')

@bp.route('/<path:path>')
def catch_all(path):
    try:
        # Try serving the requested file from 'dist' (static folder)
        return send_from_directory('dist', path)
    except:
        # If file is not found, serve index.html (for React routes)
        return send_from_directory('dist', 'index.html')
    
def index():
    return send_from_directory('dist', 'index.html')

@bp.route('/<path:path>')
def static_file(path):
    return send_from_directory('dist', path)
