from models import db

class UserSubmission(db.Model):
    __tablename__ = 'user_submissions'

    id = db.Column(db.Integer, primary_key=True)
    towns = db.Column(db.Integer, nullable=False)  # 城镇数目
    roads = db.Column(db.JSON, nullable=False)     # 道路信息 (JSON 格式)

    # 关联 MSTResult
    mst_results = db.relationship('MSTResult', backref='submission', lazy=True)

    # UserSubmission 模型用于存储用户的最小生成树计算请求，包括城镇数目和道路信息。
    # 它与 MSTResult 模型通过外键关联，确保每次用户提交后，系统可以为其计算并存储多个最小生成树的结果。
    # 这种设计使得应用程序能够有效地管理和查询用户的提交历史以及相应的计算结果。