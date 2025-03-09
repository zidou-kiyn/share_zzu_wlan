import socket
import requests
import base64
import random
from typing import Optional, Dict, Any, Tuple
from config_manager import ConfigManager
from console_ui import ConsoleUI


class CampusNetworkLogin:
    """校园网登录管理类"""

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager

    @staticmethod
    def generate_v() -> int:
        """生成一个随机数，范围在500到10499之间"""
        return random.randint(500, 10499)

    @staticmethod
    def get_local_ip() -> str:
        """获取本机IP地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("223.5.5.5", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            ConsoleUI.print_error(f"获取本机IP失败: {e}")
            return "127.0.0.1"

    @staticmethod
    def get_key(ip: str = '') -> int:
        """计算输入字符串的异或密钥"""
        ret = 0
        for char in ip:
            ret ^= ord(char)
        return ret

    @staticmethod
    def enc_pwd(pass_in: str, key: int) -> str:
        """加密函数：将密码与密钥进行异或运算，并转为十六进制字符串"""
        if len(pass_in) > 512:
            return "-1"

        pass_out = ""
        for char in pass_in:
            ch = ord(char) ^ key
            hex_str = format(ch, '02x')
            pass_out += hex_str

        return pass_out

    @staticmethod
    def dec_pwd(hex_string: str, key: int) -> str:
        """解密函数：将十六进制字符串解密回原始密码"""
        if len(hex_string) % 2 != 0:
            return "错误：十六进制字符串长度必须为偶数"

        original_password = ""
        for i in range(0, len(hex_string), 2):
            hex_pair = hex_string[i:i + 2]
            decimal_value = int(hex_pair, 16)
            original_char = chr(decimal_value ^ key)
            original_password += original_char

        return original_password

    @staticmethod
    def base64_encode(data: str) -> str:
        """对输入字符串进行Base64编码"""
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')

    def portal_login(self) -> Tuple[bool, str]:
        """执行Portal认证登录操作"""
        try:
            # 获取必要的信息
            ip = self.get_local_ip()

            key = self.get_key(ip)

            username = f",0,{self.config_manager.get('username')}{self.config_manager.get('operator')}"
            password = self.config_manager.get("password")

            # 进行加密
            user_account_encrypted = self.enc_pwd(username, key)
            user_password_base64 = self.base64_encode(password)
            user_password_encrypted = self.enc_pwd(user_password_base64, key)

            # 构建请求参数
            params = {
                "callback": self.enc_pwd("dr1003", key),
                "login_method": self.enc_pwd("1", key),
                "user_account": user_account_encrypted,
                "user_password": user_password_encrypted,
                "wlan_user_ip": self.enc_pwd(ip, key),
                "wlan_user_ipv6": "",
                "wlan_user_mac": self.enc_pwd("000000000000", key),
                "wlan_ac_ip": "", # 172.16.1.10加密？
                "wlan_ac_name": "",
                "jsVersion": self.enc_pwd("4.2.1", key),
                "terminal_type": self.enc_pwd("1", key),
                "lang": self.enc_pwd("zh-cn", key),
                "encrypt": "1",
                "v": self.generate_v(),
                "lang": "zh"
            }

            # 发起登录请求
            login_url = "http://10.2.8.8:801/eportal/portal/login"
            ConsoleUI.print_wait("正在尝试Portal认证登录...")
            response = requests.get(login_url, params=params)

            # 解析响应，判断是否登录成功
            if "result" in response.text and '"result":1' in response.text:
                return True, "Portal协议认证成功！"
            else:
                return False, f"登录失败: {response.text}"

        except Exception as e:
            return False, f"登录过程中出错: {str(e)}"

    def portal_logout(self) -> Tuple[bool, str]:
        """执行Portal认证注销操作"""
        try:
            # 获取必要的信息
            ip = self.get_local_ip()
            key = self.get_key(ip)

            # 构建请求参数
            params = {
                "callback": self.enc_pwd("dr1003", key),
                "login_method": self.enc_pwd("1", key),
                "user_account": self.enc_pwd("drcom", key),
                "user_password": self.enc_pwd("123", key),
                "ac_logout": self.enc_pwd("1", key),
                "register_mode": self.enc_pwd("1", key),
                "wlan_user_ip": self.enc_pwd(ip, key),
                "wlan_user_ipv6": "",
                "wlan_vlan_id": self.enc_pwd("1", key),
                "wlan_user_mac": self.enc_pwd("000000000000", key),
                "wlan_ac_ip": "", # 172.16.1.10加密？
                "wlan_ac_name": "",
                "jsVersion": self.enc_pwd("4.2.1", key),
                "terminal_type": self.enc_pwd("1", key),
                "encrypt": "1",
                "v": self.generate_v(),
                "lang": "zh"
            }

            logout_url = "http://10.2.8.8:801/eportal/portal/logout"
            ConsoleUI.print_wait("正在尝试注销Portal认证...")
            response = requests.get(logout_url, params=params)

            # 解析响应，判断是否登录成功
            if "result" in response.text and '"result":1' in response.text:
                return True, "注销Portal认证成功！"
            else:
                return False, f"注销失败: {response.text}"

        except Exception as e:
            return False, f"注销过程中出错: {str(e)}"

if __name__ == "__main__":
    config_manager = ConfigManager()  # 假设这里加载了配置
    login_manager = CampusNetworkLogin(config_manager)
