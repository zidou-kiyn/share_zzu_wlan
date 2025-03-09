import time, sys
from config_manager import ConfigManager
from campus_self_service import CampusSelfServiceManager
from campus_network_login import CampusNetworkLogin
from console_ui import ConsoleUI

def exit_with_status(status_code):
    ConsoleUI.print_wait("3s后退出程序....")
    # input("")
    time.sleep(3)
    sys.exit(status_code)

if __name__ == "__main__":
    config_manager = ConfigManager()
    self_service_manager = CampusSelfServiceManager(config_manager)
    login_manager = CampusNetworkLogin(config_manager)
    phone = config_manager.get("phone")

    if not self_service_manager.verify_jsessionid():
        exit_with_status(1)

    if not self_service_manager.bind_operator(phone):
        exit_with_status(1)

    success, message = login_manager.portal_logout()

    if success:
        ConsoleUI.print_success(message)
    else:
        ConsoleUI.print_error(message)

    ConsoleUI.print_wait("等待3秒后进行Portal认证...")
    time.sleep(3)

    success, message = login_manager.portal_login()

    if success:
        ConsoleUI.print_success(message)
    else:
        ConsoleUI.print_error(message)


    if not self_service_manager.unbind_operator(phone):
        exit_with_status(1)

    exit_with_status(0)