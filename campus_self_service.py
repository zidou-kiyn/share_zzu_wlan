import requests
import re
import random
from config_manager import ConfigManager
from console_ui import ConsoleUI


class CampusSelfServiceManager:
    """校园自助服务系统管理类"""

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.session = requests.session()
        # 设置 User-Agent 以伪装成 Chrome 浏览器
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.57 Safari/537.36'
        })

    def get_checkcode(self) -> str:
        """获取jsessionid和checkcode"""
        url = "http://10.2.7.16:8080/Self/login/?302=LI"

        ConsoleUI.print_wait("正在获取checkcode...")

        response = self.session.get(url, allow_redirects=False)

        match = re.search(r'name="checkcode" value="(\d+)"', response.text)

        checkcode = match.group(1) if match else ""

        return checkcode

    def send_verification_code(self) -> None:
        """发送验证码请求，使用随机数"""
        url = f"http://10.2.7.16:8080/Self/login/randomCode?t={random.random()}"
        ConsoleUI.print_wait("正在发送验证码请求...")

        # 发送请求以获取验证码
        response = self.session.get(url)

        if response.status_code == 200:
            ConsoleUI.print_success("验证码请求成功")
        else:
            ConsoleUI.print_error("验证码请求失败")

    def verify_jsessionid(self) -> bool:
        """通过verify接口认证jsessionid"""

        url = "http://10.2.7.16:8080/Self/login/verify"
        account = self.config_manager.get("username")
        password = self.config_manager.get("password")
        checkcode = self.get_checkcode()
        self.send_verification_code()


        if not checkcode:
            return False

        payload = {
            "foo": "",
            "bar": "",
            "checkcode": checkcode,
            "account": account,
            "password": password,
            "code": ""
        }

        ConsoleUI.print_wait("正在验证JSESSIONID...")
        response = self.session.post(url, data=payload, allow_redirects=False)

        if response.status_code == 302 and "/Self/dashboard" in response.headers.get('Location', ''):
            ConsoleUI.print_success("JSESSIONID验证成功")
            return True
        else:
            ConsoleUI.print_error("JSESSIONID验证失败")
            return False

    import re

    def get_csrf_token(self) -> str:
        """通过csrf_token接口获取csrf_token"""
        url = "http://10.2.7.16:8080/Self/service/operatorId"
        ConsoleUI.print_wait("正在获取CSRF Token...")
        response = self.session.get(url)

        if response.status_code == 200:
            # 使用正则表达式提取 csrftoken
            match = re.search(r'csrftoken:\s*\'([0-9a-fA-F\-]+)\'', response.text)
            if match:
                token = match.group(1)
                ConsoleUI.print_success("成功获取CSRF Token")
                return token

        ConsoleUI.print_error("获取CSRF Token失败")
        return ""

    def bind_operator(self, phone: str) -> bool:
        """通过bind接口绑定运营商"""
        csrf_token = self.get_csrf_token()
        if not csrf_token:
            return False

        phone_last_six = phone[-6:]  # 获取手机号后六位
        url = "http://10.2.7.16:8080/Self/service/bind-operator"
        payload = {
            "csrftoken": csrf_token,
            "FLDEXTRA1": "",  # 科研专网账号
            "FLDEXTRA2": "",  # 科研专网密码
            "FLDEXTRA3": phone,  # 移动账号
            "FLDEXTRA4": phone_last_six  # 移动密码（后六位）
        }

        ConsoleUI.print_wait("正在绑定运营商账号...")
        response = self.session.post(url, data=payload)

        if response.status_code == 200:
            result = response.json()
            if result.get("bind-state"):
                ConsoleUI.print_success("运营商账号绑定成功")
                # input()
                return True
            else:
                ConsoleUI.print_error(f"绑定失败: {result.get('bind-msg')}")
                return False
        else:
            ConsoleUI.print_error("绑定请求失败")
            return False


    def unbind_operator(self, phone: str) -> bool:
        """解绑运营商账号"""
        csrf_token = self.get_csrf_token()
        if not csrf_token:
            return False

        url = "http://10.2.7.16:8080/Self/service/bind-operator"
        payload = {
            "csrftoken": csrf_token,
            "FLDEXTRA1": "",  # 科研专网账号
            "FLDEXTRA2": "",  # 科研专网密码
            "FLDEXTRA3": "",  # 移动账号
            "FLDEXTRA4": ""  # 移动密码
        }

        ConsoleUI.print_wait("正在解绑运营商账号...")
        response = self.session.post(url, data=payload)
        # print(response.text)
        if response.status_code == 200:
            result = response.json()
            if result.get("bind-msg") == "":
                ConsoleUI.print_success("运营商账号解绑成功")
                return True
            else:
                ConsoleUI.print_error(f"解绑失败: {result.get('bind-msg')}")
                return False
        else:
            ConsoleUI.print_error("解绑请求失败")
            return False






if __name__ == "__main__":
    config_manager = ConfigManager()  # 假设这里加载了配置
