from sqlalchemy import func

from models import db

class MSTResult(db.Model):
    __tablename__ = 'mst_results'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('user_submissions.id'), nullable=False)
    kruskal = db.Column(db.JSON, nullable=False)  # Kruskal 算法结果 (JSON 格式)
    prim = db.Column(db.JSON, nullable=False)     # Prim 算法结果 (JSON 格式)
    created_at = db.Column(db.DateTime, default=func.now())  # 自动记录创建时间

    # MSTResult 模型用于存储最小生成树计算的结果，包括 Kruskal 和 Prim 算法的计算结果以及创建时间。
    # 每个 MSTResult 记录都与一个 UserSubmission 关联，确保每次用户提交后，系统可以为其计算并存储多个最小生成树的结果。
    # 这种设计使得应用程序能够有效地管理和查询用户的提交历史以及相应的计算结果。