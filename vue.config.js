module.exports = {
  devServer: {
    host: '127.0.0.1',  // 指定主机为 127.0.0.1
    port: 8000,        // 指定端口为 8000
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',  // 后端 API 地址
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''  // 去掉 /api 前缀
        }
      }
    }
  }
};