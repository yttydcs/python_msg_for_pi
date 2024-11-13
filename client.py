import requests
import socket
import time
import netifaces

# 服务器的IP和端口
SERVER_URL = "http://127.0.0.1:56666/update_ip"
DEVICE_ID = "raspberry_pi_1"  # 为每个树莓派设置唯一ID，便于识别

headers = {
    "Authorization": "password"
}

def get_public_ip():
    try:
        # 通过外部服务获取公网IP
        response = requests.get('https://api.ipify.org')
        return response.text
    except requests.RequestException as e:
        print("获取公网IP失败:", e)
        return None


def get_all_private_ips():
    private_ips = []
    # 获取所有网络接口的IP地址
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        # 获取IPv4地址
        if netifaces.AF_INET in addresses:
            for link in addresses[netifaces.AF_INET]:
                ip_addr = link.get("addr")
                if ip_addr:
                    private_ips.append(ip_addr)
    return private_ips


def send_ip_to_server():
    public_ip = get_public_ip()
    private_ips = get_all_private_ips()

    if public_ip and private_ips:
        payload = {
            "device_id": DEVICE_ID,
            "public_ip": public_ip,
            "private_ips": private_ips  # 将所有内网IP以列表形式提交
        }
        try:
            # 将IP地址发送到服务器
            response = requests.post(SERVER_URL, json=payload, headers=headers)
            if response.status_code == 200:
                print("IP地址已成功发送到服务器")
            else:
                print("发送失败，状态码:", response.status_code)
        except requests.RequestException as e:
            print("发送IP地址到服务器时出现错误:", e)


# 定时任务，每隔5分钟更新一次
if __name__ == "__main__":
    while True:
        send_ip_to_server()
        time.sleep(10)  # 每5分钟发送一次
