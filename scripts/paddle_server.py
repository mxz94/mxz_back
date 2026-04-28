import os
import logging
from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import numpy as np
import cv2

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 初始化 PaddleOCR (第一次运行会自动下载模型)
# use_angle_cls=True: 自动纠正文字方向
# lang='ch': 支持中英文识别
ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'code': 400, 'msg': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'code': 400, 'msg': 'No file selected'}), 400

    try:
        # 读取图片
        img_array = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'code': 400, 'msg': 'Invalid image file'}), 400

        # 执行 OCR
        result = ocr.ocr(img, cls=True)
        
        # 解析结果
        texts = []
        if result and result[0]:
            for line in result[0]:
                # line[1][0] 是文本内容, line[1][1] 是置信度
                texts.append({
                    'text': line[1][0],
                    'confidence': float(line[1][1])
                })
        
        logger.info(f"OCR Success: Found {len(texts)} lines")
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': texts
        })

    except Exception as e:
        logger.error(f"OCR Error: {str(e)}")
        return jsonify({'code': 500, 'msg': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    # 运行服务，默认端口 5000
    print("PaddleOCR Service is starting on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
