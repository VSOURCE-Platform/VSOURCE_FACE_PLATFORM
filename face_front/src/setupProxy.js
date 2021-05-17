const proxy = require('http-proxy-middleware')
        module.exports = function(app){
        app.use(
            proxy('/app',{
                target:'https://www.baidu.com',//请求转发给谁
                changeOrigin:true, //控制服务器收到的响应头中host字段的值
                pathRewrite:{'^/app':''}//重写请求路径
            })
        )
    }