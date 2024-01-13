export default {
    async fetch(request, env) {
        const url = new URL(request.url);
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
        const modifiedRequest = new Request(request, {
            method: request.method,
            headers: request.headers,
            body: modifiedBody,
        });
        await fetch(new Request(url, modifiedRequest)).then(response => response.json())
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
                        headers: { 'Content-Type': 'application/json' },
                    });
                } catch (error) {
                    // 处理错误
                    console.error('Error processing JSON:', error);
                    return new Response('Internal Server Error', { status: 500 });
                }
        }).catch(error => console.error('Error:', error) || Promise.reject(error));
    }
}