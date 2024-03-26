from flask import Blueprint, render_template, Response, make_response,jsonify
from models import UserTemplate, UserTemplatePage

template_blueprint = Blueprint('template_blueprint', __name__)


@template_blueprint.route('/template/<template_name>')
def template(template_name):
    # Template retrieval logic
    return render_template(f'{template_name}.html')


@template_blueprint.route('/template_preview/html/<int:user_template_id>/<page_name>')
def template_preview_html(user_template_id, page_name):
    # Fetch the user template from the database
    user_template = UserTemplate.query.get(user_template_id)
    if user_template:
        page = UserTemplatePage.query.filter_by(user_template_id=user_template_id, page_name=page_name).first()
        if page:
            html_content = page.modified_html

            # Dynamically insert the user_template_id and page_name into the script and link tags
            html_content = html_content.replace("{{user_template_id}}", str(user_template_id))
            html_content = html_content.replace("{{page_name}}", page_name)

            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/html'

            return response
        return "Page not found", 404
    return "Template not found", 404


@template_blueprint.route('/template_preview/css/<int:user_template_id>/<page_name>')
def template_preview_css(user_template_id, page_name):
    # Fetch the user template from the database
    user_template = UserTemplate.query.get(user_template_id)
    if user_template:
        page = UserTemplatePage.query.filter_by(user_template_id=user_template_id, page_name=page_name).first()
        if page:
            return Response(page.modified_css, mimetype='text/css')
        return "Page not found", 404
    return "Template not found", 404


@template_blueprint.route('/template_preview/js/<int:user_template_id>/<page_name>')
def template_preview_js(user_template_id, page_name):
    # Fetch the user template from the database
    user_template = UserTemplate.query.get(user_template_id)
    if user_template:
        page = UserTemplatePage.query.filter_by(user_template_id=user_template_id, page_name=page_name).first()
        if page:
            return Response(page.modified_js, mimetype='application/javascript')
        return "Page not found", 404
    return "Template not found", 404


@template_blueprint.route('/template_customize/html/<int:user_template_id>/<page_name>')
def template_customize_html(user_template_id, page_name):
    # Fetch the user template from the database
    page = UserTemplatePage.query.filter_by(
        user_template_id=user_template_id,
        page_name=page_name
    ).first()
    if page:
        page = UserTemplatePage.query.filter_by(user_template_id=user_template_id, page_name=page_name).first()
        if page:
            html_content = page.modified_html

            # Dynamically insert the user_template_id and page_name into the script and link tags
            html_content = html_content.replace("{{user_template_id}}", str(user_template_id))
            html_content = html_content.replace("{{page_name}}", page_name)

            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/html'

            return response
        else:
            # If the page is not found, return a 404 response
            return jsonify({'error': 'Page not found'}), 404
    return "Template not found", 404


@template_blueprint.route('/template_preview/css/<int:user_template_id>/<page_name>')
def template_customize_css(user_template_id, page_name):
    # Fetch the user template from the database
    user_template = UserTemplate.query.get(user_template_id)
    if user_template:
        page = UserTemplatePage.query.filter_by(user_template_id=user_template_id, page_name=page_name).first()
        if page:
            return Response(page.modified_css, mimetype='text/css')
        return "Page not found", 404
    return "Template not found", 404


@template_blueprint.route('/template_preview/js/<int:user_template_id>/<page_name>')
def template_customize_js(user_template_id, page_name):
    # Fetch the user template from the database
    user_template = UserTemplate.query.get(user_template_id)
    if user_template:
        page = UserTemplatePage.query.filter_by(user_template_id=user_template_id, page_name=page_name).first()
        if page:
            return Response(page.modified_js, mimetype='application/javascript')
        return "Page not found", 404
    return "Template not found", 404

