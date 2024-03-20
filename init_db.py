from main import create_app
from models import db, WebsiteTemplate, Page


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def init_db(app):
    with app.app_context():
        db.create_all()

        # Check if the database is empty
        if WebsiteTemplate.query.count() == 0:
            # Create the base template
            new_template = WebsiteTemplate(name='ecommerce', is_base_template=True)
            db.session.add(new_template)

            # Add pages to the template
            pages_info = [
                ('Home', 'templates/preview_templates/ecommerce/homepage.html', 'static/preview_static/ecommerce/styles.css', 'static/preview_static/ecommerce/script.js'),
                ('About', 'templates/preview_templates/ecommerce/about.html', 'static/preview_static/ecommerce/styles.css', 'static/preview_static/ecommerce/script.js'),
                ('Products', 'templates/preview_templates/ecommerce/products.html', 'static/preview_static/ecommerce/styles.css', 'static/preview_static/ecommerce/script.js'),
                ('Contact', 'templates/preview_templates/ecommerce/contact.html', 'static/preview_static/ecommerce/styles.css', 'static/preview_static/ecommerce/script.js'),
            ]

            for page_name, html_path, css_path, js_path in pages_info:
                html_content = read_file(html_path)
                css_content = read_file(css_path)
                js_content = read_file(js_path)

                new_page = Page(template=new_template, page_name=page_name, html_content=html_content, css_content=css_content, js_content=js_content)
                db.session.add(new_page)

            db.session.commit()


if __name__ == '__main__':
    app, socketio = create_app()  # Create an app context for database initialization
    init_db(app)  # Initialize the database with the app context
