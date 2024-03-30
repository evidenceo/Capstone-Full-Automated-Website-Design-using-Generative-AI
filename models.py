from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class TemplateCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    templates = db.relationship('WebsiteTemplate', backref='category', lazy='dynamic')


class WebsiteTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    is_base_template = db.Column(db.Boolean, default=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('template_category.id'))
    pages = db.relationship('Page', backref='template', lazy='dynamic')
    images = db.relationship('TemplateImage', backref='template', lazy=True)


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('website_template.id'))
    page_name = db.Column(db.String(80))
    html_content = db.Column(db.Text, nullable=False)
    css_content = db.Column(db.Text, nullable=False)
    js_content = db.Column(db.Text)


class TemplateImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('website_template.id'))
    image_path = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))

    def image_url(self):
        return url_for('static', filename=self.image_path)


class UserTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    original_template_id = db.Column(db.Integer, db.ForeignKey('website_template.id'))  # Link to the original template
    original_template = db.relationship('WebsiteTemplate', backref='user_templates')
    name = db.Column(db.String(255))  # Allow users to name their template
    status = db.Column(db.String(50))  # E.g., 'in progress', 'completed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User', backref='user_templates')
    pages = db.relationship('UserTemplatePage', backref='user_template', lazy='dynamic')


class UserTemplatePage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_template_id = db.Column(db.Integer, db.ForeignKey('user_template.id'))
    page_name = db.Column(db.String(80))
    modified_html = db.Column(db.Text)
    modified_css = db.Column(db.Text)
    modified_js = db.Column(db.Text)