---
pubDatetime: 2024-01-12 10:56:52
title: bili总结助手-Gemini
slug: bili总结助手-Gemini
tags:
  - "工具"
---

需求： 我们看B站视频发现视频很长又想看精彩点，或者想知道总结，这时我们就可以利用 [IndieKKY/bilibili-subtitle](https://github.com/IndieKKY/bilibili-subtitle) 来实现  或者直接用我封装免费的 [bilibili_subTitle免费插件](https://www.lanzv.com/i39tq1mt4tab)

# 一. 注册部署Gemmi

1. Gemini Pro的api key获取地址：https://makersuite.google.com/app/apikey (需开美国vpn)
2. 在cloudflare worker 部署转化为openapi请求 需替换apikey 
   ```js
    export default {
    async fetch(request, env) {
    let api_key = ""
    if (request.method === 'OPTIONS') {
    // 处理预检请求
    const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, HEAD, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Max-Age': '86400', // 一天，可根据需要调整
    'Access-Control-Allow-Headers': '*',
    }
    
            // 返回200 OK，同时包含CORS相关头部信息
            return new Response(null, { status: 204, headers })
          } 
          
          const url = new URL("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent");
          url.host = 'generativelanguage.googleapis.com';
          const requestBody = await request.clone().text();
          let jsonData = JSON.parse(requestBody);
          let messages = jsonData.messages
          let gemini_request_data = {
              "contents": [
                  {
                      "parts": [{"text": messages[0]["content"]}]
                  }
              ]
          }
          const modifiedBody = JSON.stringify(gemini_request_data);
          let newHeaders = new Headers(request.headers);
          newHeaders.delete('Authorization'); 
          const modifiedRequest = new Request(request, {
              method: request.method,
              headers: {
                'Content-Type': 'application/json'
                    },
              body: modifiedBody,
          });
          return await fetch(new Request(url + "?key="+api_key, modifiedRequest)).then(response => response.json())
              .then((geminiResponse) => {
                  const data = geminiResponse.candidates[0].content.parts[0].text.replace('```json', '').replace('```', '');
    
                  // 构造新的响应数据
                  const response_data = {
                      id: '79fb180d21694513',  // 实际情况下应从Gemini API响应中获取
                      object: 'chat.completion.chunk',
                      created: 3705525,  // 实际情况下应从Gemini API响应中获取
                      model: 'yi-34b-chat',  // 实际情况下应从Gemini API响应中获取
                      choices: [{
                          delta: { role: 'assistant', content: '' },
                          index: 0,
                          finish_reason: 'stop',
                          message: { content: data }
                      }],
                      content: data,
                      usage: { completion_tokens: 27, prompt_tokens: 14, total_tokens: 41 },
                      lastOne: true
                  };
                  try {
                      // 将数据转换为 JSON 字符串
                      const jsonData = JSON.stringify(response_data);
    
                      // 创建并返回一个新的 Response 对象，内容为 JSON 数据
                      return new Response(jsonData, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*', // 允许任何源发起请求，也可以指定具体的源地址
                            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', // 允许的HTTP方法
                            'Access-Control-Allow-Headers': '*', // 允许的请求头，也可以指定具体的请求头
                          }
                      });
                  } catch (error) {
                      // 处理错误
                      console.error('Error processing JSON:', error);
                      return new Response('Internal Server Error', { status: 500 });
                  }
          }).catch(error => Promise.reject(error));
    }
    } 
    ```
   另外可以参考zhile  可将Gemmi 部署为国内访问 [link](https://zhile.io/2023/12/24/gemini-pro-proxy.html#more-587)

# 二. 安装bisubTitle

Edge 下载链接 [SubTitle](https://microsoftedge.microsoft.com/addons/detail/lignnlhlpiefmcjkdkmfjdckhlaiajan)
    插件设置中填写 服务器为cloud worker 地址， apikey 随便填 然后就可以点击生成了

