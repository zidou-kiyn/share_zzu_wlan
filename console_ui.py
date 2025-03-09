class ConsoleUI:
    """用户界面类，负责所有的输出和输入交互"""

    @staticmethod
    def print_header():
        print("\n" + "=" * 60)
        print("             校园网自动登录工具")
        print("=" * 60 + "\n")

    @staticmethod
    def print_section(title):
        print("\n" + "-" * 50)
        print(f"  {title}")
        print("-" * 50)

    @staticmethod
    def print_info(message):
        print(f"[信息] {message}")

    @staticmethod
    def print_success(message):
        print(f"[成功] {message}")

    @staticmethod
    def print_error(message):
        print(f"[错误] {message}")

    @staticmethod
    def print_wait(message):
        print(f"[等待] {message}", end="", flush=True)

    @staticmethod
    def print_wait_update(message):
        print(f"\r[等待] {message}", end="", flush=True)

    @staticmethod
    def print_wait_done():
        print()  # 换行

    @staticmethod
    def get_input(prompt):
        return input(f"[输入] {prompt}: ")

    @staticmethod
    def get_password(prompt):
        import getpass
        print(f"[输入] {prompt}: ", end="", flush=True)
        return getpass.getpass("")
