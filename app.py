from flask import Flask, jsonify
from flask_cors import CORS
from routes.mst import mst_blueprint  # 导入 mst 蓝图
from config import Config
from models import db, init_db

#创建并配置Flask应用实例
def create_app():
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(Config)

    # 允许跨域请求
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://127.0.0.1:8000"],  # 确保这是你前端的域名和端口
            "methods": ["POST", "OPTIONS"],  # 确保包含 OPTIONS 方法
            "allow_headers": ["Content-Type", "Authorization"],  # 确保允许的请求头
            "supports_credentials": True,  # 如果需要传递 cookies 或其他凭证
            "max_age": 3600  # 缓存预检请求结果 1 小时
        }
    })

    # 初始化数据库
    init_db(app)

    # 注册 mst 蓝图，并指定前缀 /api
    app.register_blueprint(mst_blueprint, url_prefix='/api')

    # 添加数据库管理命令
    @app.cli.command("init-db")
    def init_db_command():
        """初始化数据库并创建所有表"""
        db.create_all()
        print("数据库已初始化并创建所有表。")

    @app.cli.command("drop-db")
    def drop_db_command():
        """删除所有表"""
        db.drop_all()
        print("所有表已删除。")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) #启动

#这段代码构建了一个完整的 Flask 应用程序框架，具备以下功能：

#跨域支持：通过 flask-cors 插件，允许前端应用从不同的域名或端口访问 API。
#数据库管理：使用 SQLAlchemy 进行数据库操作，并提供了命令行工具来初始化和删除数据库。
#模块化设计：通过蓝图 (mst_blueprint) 将 MST 计算相关的路由和逻辑分离出来，使得代码更加清晰和易于维护。
#配置管理：通过 Config 类集中管理应用程序的配置参数，确保敏感信息不会硬编码在代码中。
#命令行工具：提供了 init-db 和 drop-db 两个命令行工具，方便开发者管理数据库。