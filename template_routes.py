import os.path

from flask import Blueprint, render_template, Response, make_response, jsonify, request, current_app, url_for, send_file
from models import UserTemplate, UserTemplatePage
from werkzeug.utils import secure_filename
from flask_login import current_user
from zipfile import ZipFile
from classes import DBUtils

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


@template_blueprint.route('/template_customize/css/<int:user_template_id>/<page_name>')
def template_customize_css(user_template_id, page_name):
    # Fetch the user template from the database
    user_template = UserTemplate.query.get(user_template_id)
    if user_template:
        page = UserTemplatePage.query.filter_by(user_template_id=user_template_id, page_name=page_name).first()
        if page:
            return Response(page.modified_css, mimetype='text/css')
        return "Page not found", 404
    return "Template not found", 404


@template_blueprint.route('/template_customize/js/<int:user_template_id>/<page_name>')
def template_customize_js(user_template_id, page_name):
    # Fetch the user template from the database
    user_template = UserTemplate.query.get(user_template_id)
    if user_template:
        page = UserTemplatePage.query.filter_by(user_template_id=user_template_id, page_name=page_name).first()
        if page:
            return Response(page.modified_js, mimetype='application/javascript')
        return "Page not found", 404
    return "Template not found", 404


@template_blueprint.route('/template/pages/<int:user_template_id>')
def get_template_pages(user_template_id):
    # Fetch the user template from the database
    user_template = UserTemplate.query.get(user_template_id)
    if user_template:
        # Fetch all the pages in db
        pages = UserTemplatePage.query.filter_by(user_template_id=user_template_id).all()

        # Extract the page names in a list
        available_pages = [page.page_name for page in pages]

        # Return the list of page names in JSON
        return jsonify(available_pages)
    else:
        return jsonify({'error': 'Template not found'}), 404


@template_blueprint.route('/file-upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error='No file part'), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error='No selected file'), 400
    if file:
        user_id = current_user.get_id()
        user_template_id = request.form.get('user_template_id')
        user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id), str(user_template_id))
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        filename = secure_filename(file.filename)
        file_path = os.path.join(user_folder, filename)
        file.save(file_path)

        file_relative_path = url_for('static', filename=f'uploads/{user_id}/{user_template_id}/{filename}', _external=True)
        return jsonify(success=True, message="File uploaded successfully", link=file_relative_path)


@template_blueprint.route('/save_page/<int:user_template_id>/<page_name>', methods=['POST'])
def save_page(user_template_id, page_name):
    if not request.json or 'html' not in request.json:
        return jsonify({'error': 'Invalid request'}), 400

    updated_html = request.json['html']

    try:
        # Use DBUtils to update the page content
        DBUtils.update_template_in_db(user_template_id, page_name, updated_html, 'html')
        return jsonify({'success': True, 'message': 'Page updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@template_blueprint.route('/download_template/<int:user_template_id>')
def download_template(user_template_id):
    user_template = UserTemplate.query.get_or_404(user_template_id)
    if user_template.user_id != current_user.id:
        return jsonify(error="Unauthorized access"), 403

    # Create a temporary zip file
    temp_dir = os.path.join('temp', str(user_template_id))
    os.makedirs(temp_dir, exist_ok=True)
    zip_path = os.path.join(temp_dir, 'template.zip')

    with ZipFile(zip_path, 'w') as zipf:
        # For each page in the template, create an HTML file and add it to the zip
        for page in user_template.pages:
            html_path = os.path.join(temp_dir, f"{page.page_name}.html")
            with open(html_path, 'w') as file:
                file.write(page.modified_html)
            zipf.write(html_path, arcname=f"{page.page_name}.html")
            css_path = os.path.join(temp_dir, f"{page.page_name}.css")
            with open(css_path, 'w') as file:
                file.write(page.modified_css)
            zipf.write(css_path, arcname=f"{page.page_name}.css")

    return send_file(zip_path, as_attachment=True, download_name=f"{user_template.name}.zip")

