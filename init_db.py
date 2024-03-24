from main import create_app, db

app, _ = create_app()

from models import WebsiteTemplate, Page, TemplateCategory


# Read template files
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Define your templates and their pages
templates_data = [
    {
        "name": "Ecommerce Template 1",
        "is_base_template": True,
        "category": "ecommerce",
        "pages": [
            {
                "page_name": "Home",
                "html_content": read_file("template_files/ecommerce/plain-one/html/home.html"),
                "css_content": read_file("template_files/ecommerce/plain-one/css/home_styles.css"),
                "js_content": read_file("template_files/ecommerce/plain-one/js/script.js"),
            },
            {
                "page_name": "About",
                "html_content": read_file("template_files/ecommerce/plain-one/html/about.html"),
                "css_content": read_file("template_files/ecommerce/plain-one/css/about_styles.css"),
                "js_content": read_file("template_files/ecommerce/plain-one/js/script.js"),
            },
            {
                "page_name": "Product",
                "html_content": read_file("template_files/ecommerce/plain-one/html/products.html"),
                "css_content": read_file("template_files/ecommerce/plain-one/css/about_styles.css"),
                "js_content": read_file("template_files/ecommerce/plain-one/js/script.js"),
            },
            {
                "page_name": "Contact",
                "html_content": read_file("template_files/ecommerce/plain-one/html/contact.html"),
                "css_content": read_file("template_files/ecommerce/plain-one/css/contact_styles.css"),
                "js_content": read_file("template_files/ecommerce/plain-one/js/script.js"),
            }
            # Add more pages as needed
        ],
    },
    {
        "name": "Ecommerce Template 2",
        "is_base_template": True,
        "category": "ecommerce",
        "pages": [
            {
                "page_name": "Home",
                "html_content": read_file("template_files/ecommerce/plain-two/html/home.html"),
                "css_content": read_file("template_files/ecommerce/plain-two/css/home_styles.css"),
                "js_content": read_file("template_files/ecommerce/plain-two/js/script.js"),
            },
            {
                "page_name": "About",
                "html_content": read_file("template_files/ecommerce/plain-two/html/about.html"),
                "css_content": read_file("template_files/ecommerce/plain-two/css/about_styles.css"),
                "js_content": read_file("template_files/ecommerce/plain-two/js/script.js"),
            },
            {
                "page_name": "Product",
                "html_content": read_file("template_files/ecommerce/plain-two/html/product.html"),
                "css_content": read_file("template_files/ecommerce/plain-two/css/product_styles.css"),
                "js_content": read_file("template_files/ecommerce/plain-two/js/script.js"),
            },
            {
                "page_name": "Contact",
                "html_content": read_file("template_files/ecommerce/plain-two/html/contact.html"),
                "css_content": read_file("template_files/ecommerce/plain-two/css/contact_styles.css"),
                "js_content": read_file("template_files/ecommerce/plain-two/js/script.js"),
            }
            # Add more pages as needed
        ],
    },
    {
        "name": "Events Template 1",
        "is_base_template": True,
        "category": "events",
        "pages": [
            {
                "page_name": "Home",
                "html_content": read_file("template_files/events/plain-one/html/home.html"),
                "css_content": read_file("template_files/events/plain-one/css/home_styles.css"),
                "js_content": None
            }
            # Add more pages as needed
        ],
    },
    {
        "name": "Portfolio Template 1",
        "is_base_template": True,
        "category": "portfolio",
        "pages": [
            {
                "page_name": "Home",
                "html_content": read_file("template_files/personal_portfolio/plain-one/html/home.html"),
                "css_content": read_file("template_files/personal_portfolio/plain-one/css/home_styles.css"),
                "js_content": None
            }
            # Add more pages as needed
        ],
    },
    # Add more templates as needed
]


def add_categories_to_database():
    # List of unique category names you expect
    categories = ['ecommerce', 'events', 'portfolio']

    for category_name in categories:
        existing_category = TemplateCategory.query.filter_by(name=category_name).first()
        if not existing_category:
            new_category = TemplateCategory(name=category_name)
            db.session.add(new_category)
    db.session.commit()


def add_templates_to_database():
    for template_data in templates_data:
        # Fetch the category instance based on the category name
        category = TemplateCategory.query.filter_by(name=template_data["category"]).first()
        if not category:
            print(f"Category {template_data['category']} not found.")
            continue  # or handle the error as needed

        template = WebsiteTemplate(
            name=template_data["name"],
            is_base_template=template_data["is_base_template"],
            category=category
        )
        db.session.add(template)
        db.session.flush()  # This will assign an ID to template without committing the transaction

        for page_data in template_data["pages"]:
            page = Page(
                template_id=template.id,
                page_name=page_data["page_name"],
                html_content=page_data["html_content"],
                css_content=page_data["css_content"],
                js_content=page_data["js_content"],
            )
            db.session.add(page)

    db.session.commit()


with app.app_context():
    add_categories_to_database()
    add_templates_to_database()
