from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class WebsiteTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    is_base_template = db.Column(db.Boolean, default=False, nullable=False)
    pages = db.relationship('Page', backref='template', lazy='dynamic')


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('website_template.id'))
    page_name = db.Column(db.String(80))
    html_content = db.Column(db.Text, nullable=False)
    css_content = db.Column(db.Text, nullable=False)
    js_content = db.Column(db.Text)
