from flask import Flask, request, jsonify, render_template, send_from_directory
import time

SERVER_PORT = 56666
API_SECRET_KEY = "password"  # 用你自己设置的密钥

app = Flask(__name__, static_folder="static")

# 用于存储客户端信息
devices = {}

# 验证密钥的函数
def check_api_key():
    api_key = request.headers.get("Authorization")
    if api_key != API_SECRET_KEY:
        return False
    return True


@app.route("/update_ip", methods=["POST"])
def update_ip():
    if not check_api_key():
        return jsonify({"error": "Unauthorized, Invalid API Key"}), 403

    data = request.get_json()
    device_id = data.get("device_id")
    public_ip = data.get("public_ip")
    private_ips = data.get("private_ips")

    if not device_id or not public_ip or not private_ips:
        return jsonify({"error": "缺少必要字段"}), 400

    # 更新设备信息
    devices[device_id] = {
        "public_ip": public_ip,
        "private_ips": private_ips,
        "last_update": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    }
    print(f"收到 {device_id} 的IP信息: 公网IP: {public_ip}, 内网IP: {private_ips}")
    return jsonify({"status": "success"}), 200


@app.route("/devices", methods=["GET"])
def get_devices():
    # 返回所有设备的IP信息
    return jsonify(devices), 200

# 更新根路径到 /index.html
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# 为 /index.html 设置路由（如果直接请求文件）
@app.route("/index.html")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=SERVER_PORT)  # 将端口替换为你希望的端口
