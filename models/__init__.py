from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 初始化 SQLAlchemy 实例
db = SQLAlchemy()

# 初始化 Flask-Migrate 实例
migrate = Migrate()

def init_db(app):
    """初始化数据库并注册到 Flask 应用"""
    db.init_app(app)
    migrate.init_app(app, db)

# 导入所有模型类，以便它们可以被其他模块导入
from .user_submission import UserSubmission
from .mst_result import MSTResult

#这段代码的主要作用是：
#初始化数据库：通过 SQLAlchemy 实例 db，应用程序可以与数据库进行交互。
#管理数据库迁移：通过 Flask-Migrate 实例 migrate，应用程序可以方便地创建、应用和回滚数据库迁移，确保数据库结构与代码中的模型类保持同步。
#导入模型类：确保 Flask-Migrate 能够检测到模型类的变化，并生成相应的迁移脚本。