from flask import Blueprint, render_template, Response, abort
from models import db, WebsiteTemplate, Page

template_blueprint = Blueprint('template_blueprint', __name__)


@template_blueprint.route('/template/<template_name>')
def template(template_name):
    # Template retrieval logic
    return render_template(f'{template_name}.html')


@template_blueprint.route('/template_content/<int:template_id>/<page_name>')
def template_page_content(template_id, page_name):
    template = WebsiteTemplate.query.get(template_id)
    if template:
        page = Page.query.filter_by(template_id=template_id, page_name=page_name).first()
        if page:
            return page.html_content
        return "Page not found", 404
    return "Template not found", 404


@template_blueprint.route('/template_content/css/<int:template_id>/<string:page_name>')
def serve_css(template_id, page_name):
    page = Page.query.filter_by(template_id=template_id, page_name=page_name).first()
    if page:
        return Response(page.css_content, mimetype='text/css')
    return abort(404)


@template_blueprint.route('/template_content/js/<int:template_id>/<string:page_name>')
def serve_js(template_id, page_name):
    page = Page.query.filter_by(template_id=template_id, page_name=page_name).first()
    if page:
        return Response(page.js_content, mimetype='application/javascript')
    return abort(404)
