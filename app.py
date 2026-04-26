from flask import Flask
from flask_cors import CORS
import config


from api.upload import upload_bp
from api.login import login_bp
from api.registerUser import registerUser_bp
from api.history import history_bp
from api.result import result_bp
def create_app():
    """
    Flask 应用工厂函数
    便于后期扩展、测试和部署
    """
    app = Flask(__name__)

    # 解决微信小程序跨域问题
    CORS(app)

    # 基础配置

    # 注册蓝图
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    app.register_blueprint(login_bp, url_prefix='/api/login')
    app.register_blueprint(registerUser_bp, url_prefix='/api/registerUser')
    app.register_blueprint(history_bp, url_prefix='/api/history')
    app.register_blueprint(result_bp, url_prefix='/api/result')
    # 健康检查接口（测试服务是否启动）
    @app.route('/')
    def index():
        return {
            "code": 200,
            "msg": "Backend Running"
        }

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
