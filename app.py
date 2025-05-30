from flask import Flask, render_template, jsonify
import requests
import re
import time

app = Flask(__name__)

def get_hebei_tv_url():
    """获取河北卫视直播源链接"""
    base_url = "https://tv.pull.hebtv.com/jishi/weishipindao.m3u8"
    timestamp = int(time.time())
    key = "be4add580d3a62dbd555d3a09305c015"
    return f"{base_url}?t={timestamp}&k={key}"

def extract_m3u8_from_page(url):
    """从网页中提取m3u8链接"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # 使用正则表达式查找m3u8链接
        m3u8_pattern = r'(https?://[^\s]+?\.m3u8[^\s]*?)["\']'
        matches = re.findall(m3u8_pattern, response.text)
        
        if matches:
            return matches[0]
        return None
    except Exception as e:
        print(f"提取m3u8链接出错: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/hebei')
def hebei_tv():
    url = get_hebei_tv_url()
    return jsonify({"url": url, "name": "河北卫视"})

@app.route('/api/extract')
def extract_m3u8():
    target_url = "https://example.com/live-tv-page"  # 替换为你想抓取的网页
    extracted_url = extract_m3u8_from_page(target_url)
    return jsonify({"original": target_url, "extracted": extracted_url})

if __name__ == '__main__':
    app.run(debug=True)
