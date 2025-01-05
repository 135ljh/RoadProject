<template>
  <div id="app">
    <!-- 页面标题和导航栏 -->
    <header class="header">
      <h1>道路畅通工程</h1>
      <p>欢迎来到道路畅通工程方案系统！</p>

      <!-- 控制历史记录显示/隐藏的按钮 -->
      <button @click="toggleHistory" class="toggle-history-btn">
        {{ showHistory ? '隐藏历史记录' : '显示历史记录' }}
      </button>
    </header>

    <!-- 主内容区域 -->
    <main class="main-content">
      <router-view></router-view>
      
      <!-- 提交道路方案表单 -->
      <section class="road-form">
        <h2>提交道路方案</h2>
        <form @submit.prevent="handleSubmit">
          <!-- 城镇数目输入 -->
          <div class="form-group">
            <label for="towns">城镇数目 (n >= 8):</label>
            <input type="number" id="towns" v-model.number="towns" min="8" required />
          </div>

          <!-- 道路数目输入 -->
          <div class="form-group">
            <label for="roads-count">道路数目 (m >= 16):</label>
            <input type="number" id="roads-count" v-model.number="roadsCount" min="16" required />
          </div>

          <!-- 动态添加道路信息 -->
          <div v-for="(road, index) in roads" :key="index" class="form-group">
            <label :for="'road-' + index">道路 {{ index + 1 }}:</label>
            <div class="road-inputs">
              <input type="number" :id="'start-' + index" v-model.number="road.start" placeholder="始点城镇编号" :min="1" :max="towns" required />
              <input type="number" :id="'end-' + index" v-model.number="road.end" placeholder="终点城镇编号" :min="1" :max="towns" required />
              <input type="number" :id="'length-' + index" v-model.number="road.length" placeholder="道路长度" min="1" required />
              <button type="button" @click="removeRoad(index)" class="remove-btn">删除</button>
            </div>
          </div>

          <!-- 添加更多道路按钮 -->
          <div class="form-group">
            <button type="button" @click="addRoad" class="add-road-btn">添加道路</button>
          </div>

          <!-- 提交按钮 -->
          <div class="form-group">
            <button type="submit" class="submit-btn">提交</button>
          </div>
        </form>
      </section>

      <!-- 结果显示区 -->
      <section v-if="result" class="result-section">
        <h2>最小生成树结果对比</h2>

        <!-- 破圈法 (Kruskal) 结果 -->
        <div class="algorithm-result">
          <h3>破圈法 (Kruskal)</h3>
          <p>需要建设的道路数目: {{ result.kruskal.newRoads.length }}</p>
          <ul>
            <li v-for="(road, index) in result.kruskal.newRoads" :key="index">
              道路 {{ index + 1 }}: 始点 {{ road.start }}, 终点 {{ road.end }}, 长度 {{ road.length }}
            </li>
          </ul>
        </div>

        <!-- 避圈法 (Prim) 结果 -->
        <div class="algorithm-result">
          <h3>避圈法 (Prim)</h3>
          <p>需要建设的道路数目: {{ result.prim.newRoads.length }}</p>
          <ul>
            <li v-for="(road, index) in result.prim.newRoads" :key="index">
              道路 {{ index + 1 }}: 始点 {{ road.start }}, 终点 {{ road.end }}, 长度 {{ road.length }}
            </li>
          </ul>
        </div>
      </section>

      <!-- 历史记录显示区 -->
      <section v-if="showHistory" class="history-section">
        <h2>历史记录</h2>
        <ul v-if="records.length > 0">
          <li v-for="(record) in records" :key="record.id" @click="viewDetails(record)">
            <p>提交时间: {{ formatDate(record.timestamp) }}</p>
            <p>城镇数目: {{ record.towns }}</p>
            <p>道路数目: {{ record.roads.length }}</p>
          </li>
        </ul>
        <p v-else>暂无历史记录。</p>

        <!-- 详情模态框 -->
        <div v-if="selectedRecord" class="modal">
          <div class="modal-content">
            <span class="close" @click="closeModal">&times;</span>
            <h2>详情</h2>
            <p>提交时间: {{ formatDate(selectedRecord.timestamp) }}</p>
            <p>城镇数目: {{ selectedRecord.towns }}</p>
            <p>道路数目: {{ selectedRecord.roads.length }}</p>
            <h3>原始道路信息</h3>
            <ul>
              <li v-for="(road, index) in selectedRecord.roads" :key="index">
                道路 {{ index + 1 }}: 始点 {{ road.start }}, 终点 {{ road.end }}, 长度 {{ road.length }}
              </li>
            </ul>
            <h3>破圈法 (Kruskal) 结果</h3>
            <ul>
              <li v-for="(road, index) in selectedRecord.kruskal.newRoads" :key="index">
                道路 {{ index + 1 }}: 始点 {{ road.start }}, 终点 {{ road.end }}, 长度 {{ road.length }}
              </li>
            </ul>
            <h3>避圈法 (Prim) 结果</h3>
            <ul>
              <li v-for="(road, index) in selectedRecord.prim.newRoads" :key="index">
                道路 {{ index + 1 }}: 始点 {{ road.start }}, 终点 {{ road.end }}, 长度 {{ road.length }}
              </li>
            </ul>
          </div>
        </div>
      </section>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <p>ljh 道路畅通工程</p>
    </footer>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      towns: 8,  // 默认城镇数目
      roadsCount: 16,  // 默认道路数目
      roads: [],  // 当前道路信息列表
      result: null,  // 最小生成树结果
      showHistory: false,  // 控制是否显示历史记录
      records: [], // 所有的历史记录
      selectedRecord: null, // 当前选择查看的记录
    };
  },
  methods: {
    toggleHistory() {
      this.showHistory = !this.showHistory;
      console.log('showHistory:', this.showHistory);  // 调试信息
    },

    addRoad() {
      this.roads.push({ start: '', end: '', length: '' });
    },

    removeRoad(index) {
      this.roads.splice(index, 1);
    },

    async handleSubmit() {
      try {
        // 检查输入是否合法
        if (!this.towns || this.towns < 8) {
          alert('城镇数目必须大于等于8');
          return;
        }
        if (!this.roadsCount || this.roadsCount < 16) {
          alert('道路数目必须大于等于16');
          return;
        }
        if (this.roads.length !== this.roadsCount) {
          alert('请输入正确的道路数目');
          return;
        }

        // 检查每条道路的合法性
        for (const road of this.roads) {
          if (!road.start || !road.end || !road.length) {
            alert('请确保所有道路信息都已填写完整');
            return;
          }
          if (road.start === road.end) {
            alert('始点和终点不能相同');
            return;
          }
          if (road.start < 1 || road.start > this.towns || road.end < 1 || road.end > this.towns) {
            alert('始点或终点城镇编号超出范围');
            return;
          }
        }

        // 构建要发送的数据
        const input = {
          towns: this.towns,
          roads: this.roads.map(road => ({
            start: road.start,
            end: road.end,
            length: road.length,
          })),
        };

        // 发送POST请求到后端API
        const response = await axios.post('http://127.0.0.1:5000/api/calculate-mst', input);

        // 处理后端返回的结果
        const result = response.data;

        // 保存新的历史记录
        const newRecord = {
          timestamp: new Date().toISOString(),
          towns: this.towns,
          roads: this.roads,
          kruskal: result.kruskal,
          prim: result.prim
        };
        this.records.unshift(newRecord);  // 将新记录添加到数组开头

        // 显示结果
        this.result = result;

        // 清空表单
        this.towns = 8;
        this.roadsCount = 16;
        this.roads = [];

        alert('道路方案已成功提交并计算完成！');
      } catch (error) {
        console.error('提交失败:', error);
        alert('提交失败，请检查输入数据或网络连接。');
      }
    },

    viewDetails(record) {
      console.log('查看的记录:', record);  // 调试信息
      this.selectedRecord = record;
    },

    closeModal() {
      this.selectedRecord = null;
    },

    formatDate(dateString) {
      if (!dateString) return '未知时间';  // 处理空或无效的时间戳
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },

    // 从后端获取历史记录
    async fetchRecords() {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/history');
    console.log('后端返回的历史记录:', response.data);  // 调试信息

    // 直接使用后端返回的 created_at 字段
    this.records = response.data.map(record => ({
      ...record,
      timestamp: record.created_at  
    }));

    console.log('加载完成后的 records:', this.records);  // 调试信息
  } catch (error) {
    console.error('获取历史记录失败:', error);
  }
}
  },
  created() {
    // 页面加载时获取历史记录
    this.fetchRecords();
  }
};
</script>

<style scoped>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  color: #333;
}

#app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.nav-links {
  margin-top: 10px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.nav-btn {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.nav-btn:hover {
  background-color: #0056b3;
}

.nav-btn.router-link-exact-active {
  background-color: #28a745;
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.road-info,
.road-form {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input[type="number"],
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.road-inputs {
  display: flex;
  gap: 10px;
  align-items: center;
}

.remove-btn {
  background-color: #dc3545;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.remove-btn:hover {
  background-color: #c82333;
}

.add-road-btn,
.submit-btn {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-road-btn:hover,
.submit-btn:hover {
  background-color: #218838;
}

.result-section {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.result-section h2 {
  margin-bottom: 10px;
}

.result-section ul {
  list-style-type: none;
  padding: 0;
}

.result-section li {
  margin-bottom: 5px;
}

.footer {
  text-align: center;
  margin-top: 20px;
  padding: 10px;
  background-color: #f9f9f9;
  border-top: 1px solid #ddd;
}

/* 新增的历史记录显示区样式 */
.history-section {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.history-section h2 {
  margin-bottom: 10px;
}

.history-section ul {
  list-style-type: none;
  padding: 0;
}

.history-section li {
  background-color: #e9ecef;
  margin-bottom: 10px;
  padding: 15px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.history-section li:hover {
  background-color: #d1d3d4;
}

.history-section p {
  margin: 5px 0;
}

/* 新增的详情模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* 确保模态框在其他内容之上 */
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 80%;
  max-height: 80%;
  overflow-y: auto;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.close {
  float: right;
  font-size: 28px;
  font-weight: bold;
  color: #aaa;
  cursor: pointer;
  transition: color 0.3s ease;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
}

.modal-content h2 {
  margin-bottom: 10px;
}

.modal-content p {
  margin: 5px 0;
}

.modal-content ul {
  list-style-type: none;
  padding: 0;
}

.modal-content li {
  margin-bottom: 5px;
}

/* 日期格式化样式 */
.date-format {
  font-style: italic;
  color: #6c757d;
}

/* 控制历史记录显示/隐藏的按钮样式 */
.toggle-history-btn {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 20px;
}

.toggle-history-btn:hover {
  background-color: #0056b3;
}

</style>