from flask import Blueprint, request, jsonify
from utils.mst_algorithm import calculate_mst_kruskal, calculate_mst_prim
from functools import wraps
import logging
from models import db, UserSubmission, MSTResult
from utils.mst_print import print_mst_tree_prim, print_mst_tree_kruskal

# 创建蓝图
mst_blueprint = Blueprint('mst', __name__)

# 设置日志记录
logger = logging.getLogger(__name__)

def validate_input(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            data = request.get_json()

            if not data or 'towns' not in data or 'roads' not in data:
                return jsonify({'error': '无效的输入数据'}), 400

            towns = data['towns']
            roads = data['roads']

            if towns < 8:
                return jsonify({'error': '城镇数目必须大于等于8'}), 400
            if len(roads) < 16:
                return jsonify({'error': '道路数目必须大于等于16'}), 400

            for road in roads:
                if 'start' not in road or 'end' not in road or 'length' not in road:
                    return jsonify({'error': '道路信息不完整'}), 400
                if road['start'] < 1 or road['start'] > towns or road['end'] < 1 or road['end'] > towns:
                    return jsonify({'error': f'城镇编号必须在1到{towns}之间'}), 400
                if road['length'] <= 0:
                    return jsonify({'error': '道路长度必须为正数'}), 400

            logger.info("输入验证通过")
            return f(towns, roads, *args, **kwargs)

        except Exception as e:
            logger.error(f"输入验证失败: {str(e)}")
            return jsonify({'error': str(e)}), 500

    return decorated_function

@mst_blueprint.route('/calculate-mst', methods=['POST'])
@validate_input
def calculate_minimum_spanning_tree(towns, roads):
    try:
        # 记录开始计算的时间
        logger.info("开始计算最小生成树")

        # 创建 UserSubmission 记录
        submission = UserSubmission(towns=towns, roads=roads)
        db.session.add(submission)
        db.session.flush()  # 获取自动生成的 submission.id

        # 计算破圈法 (Kruskal) 的最小生成树
        kruskal_result = calculate_mst_kruskal(towns, roads)
        logger.info("Kruskal 算法计算完成")
        # 打印 Kruskal 最小生成树
        #print("Kruskal 最小生成树 (树形结构):")
        print_mst_tree_kruskal(kruskal_result)

        # 计算避圈法 (Prim) 的最小生成树
        prim_result = calculate_mst_prim(towns, roads)
        logger.info("Prim 算法计算完成")
        # 打印 Prim 最小生成树
        #print("Prim 最小生成树 (树形结构):")
        print_mst_tree_prim(prim_result)

        # 创建 MSTResult 记录
        mst_result = MSTResult(
            submission_id=submission.id,
            kruskal=kruskal_result,
            prim=prim_result
        )
        db.session.add(mst_result)

        # 提交事务
        db.session.commit()

        # 返回两种算法的结果
        result = {
            'id': submission.id,
            'kruskal': kruskal_result,
            'prim': prim_result
        }

        logger.info("最小生成树计算完成并返回结果")
        return jsonify(result), 200

    except Exception as e:
        db.session.rollback()  # 回滚事务
        logger.error(f"最小生成树计算失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@mst_blueprint.route('/history', methods=['GET'])
def get_history():
    try:
        # 查询所有提交的历史记录
        submissions = UserSubmission.query.all()

        history = []
        for submission in submissions:
            mst_result = MSTResult.query.filter_by(submission_id=submission.id).first()
            if mst_result:
                history.append({
                    'id': submission.id,
                    'towns': submission.towns,
                    'roads': submission.roads,
                    'kruskal': mst_result.kruskal,
                    'prim': mst_result.prim,
                    'created_at': mst_result.created_at.isoformat()  # 将 create_at 转换为 ISO 格式字符串
                })

        logger.info("历史记录查询完成")
        return jsonify(history), 200

    except Exception as e:
        logger.error(f"历史记录查询失败: {str(e)}")
        return jsonify({'error': str(e)}), 500