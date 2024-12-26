# routes/__init__.py
from flask import Blueprint
from .mst import mst_blueprint

def register_blueprints(app):
    """注册所有路由蓝图"""
    app.register_blueprint(mst_blueprint, url_prefix='/api')