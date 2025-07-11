import json
import sys

import yaml
import requests
import subprocess
import logging
import telnetlib

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def load_yaml_config(file_path):
    """加载YAML配置文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"加载{file_path}YAML文件失败: {e}")
        return None


def load_json_config(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.warning(f"{file_path}路径加载文件失败或者序列化失败: {e}")
        return None


def execute_ping(ip, count=4):
    """执行ping命令"""
    try:
        result = subprocess.run(['ping', '-c', str(count), ip],
                                capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            logging.info(f"Ping {ip} 成功: {result.stdout.strip()}")
            return True
        else:
            logging.error(f"Ping {ip} 失败: {result.stderr.strip()}")
            return False
    except Exception as e:
        logging.error(f"Ping执行异常: {e}")
    return False


def execute_telnet(ip, port):
    """执行Telnet命令"""
    try:
        # 使用telnetlib进行更可靠的连接检查
        tn = telnetlib.Telnet(ip, port, timeout=5)
        tn.close()
        logging.info(f"Telnet {ip}:{port} 连接成功")
        return True
    except Exception as e:
        logging.error(f"Telnet {ip}:{port} 连接失败: {e}")
    return False


def send_http_request(url, data=None):
    """发送HTTP请求"""
    try:
        headers = {'Content-Type': 'application/json'}  # 根据实际需求调整
        response = requests.post(url, json=data, headers=headers, timeout=5)
        response.raise_for_status()  # 自动抛出HTTP错误
        logging.info(f"response : {response.text}")
        return response
    except requests.RequestException as e:
        logging.error(f"HTTP请求失败: {e}")
        return None


# def process_test_case(case_config, validation_rules):
#     """处理单个测试用例"""
#
#     # 如果URL无效，尝试拼接IP和端口
#     ip = case_config.get('ip')
#     port = case_config.get('port')
#     if ip and port:
#         url = f" http://{ip}:{port}/{case_config.get('api', '')}"
#
#     data = case_config.get('data')
#     if data == None:
#         # 如果data是文件路径且use=0，跳过发送数据
#         response = send_http_request(url)
#     else:
#         response = send_http_request(url, data)
#         return True
#     return False


def run_tests(yaml_path):
    yaml_config = load_yaml_config(yaml_path)
    if yaml_config is None:
        logging.error("yaml config is none")
        return False
    yaml_config = yaml_config.get("test")
    if yaml_config is None:
        logging.error("yaml config test is none")
        return False
    """执行所有测试用例"""

    for case_config in yaml_config:
        curlUse = case_config.get('curl_use')
        if curlUse is None or curlUse != 1:
            logging.info(f"curl use is none or use != 1")
            continue

        data = case_config.get('data')
        if data is None:
            logging.warning("data is none")
        else:
            data = load_json_config(data)
        if data is None or len(data) == 0:
            data = {}
        ip = case_config.get('ip')
        port = case_config.get('port')
        api = case_config.get('api')
        if ip is None:
            logging.error("ip is none")
            continue
        if port is None:
            logging.error("port is none")
            continue
        if api is None:
            logging.error("api is none")
        if api.startswith('/'):
            logging.warning("api is start / but we had add it ")
        url = f" http://{ip}:{port}/{api}"
        logging.info(f"正在执行测试用例: {api}")

        send_http_request(url, data)


if __name__ == '__main__':
    run_tests("./test.yaml")
