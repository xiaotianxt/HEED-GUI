import toml
from functools import wraps

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.config_data = cls.load_config()
        return cls._instance

    @staticmethod
    def load_config():
        try:
            with open('config.toml', 'r') as config_file:
                return toml.load(config_file)
        except FileNotFoundError:
            raise FileNotFoundError("The 'config.toml' file was not found.")

    @classmethod
    def get_config_value(cls, scope, key):
        if scope in cls._instance.config_data:
            if key in cls._instance.config_data[scope]:
                return cls._instance.config_data[scope][key]
        return None

# 使用装饰器来简化获取配置的过程
def with_config(scope, key):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            config = Config()
            value = config.get_config_value(scope, key)
            return func(value, *args, **kwargs)
        return wrapper
    return decorator

# 示例用法
@with_config("elective", "USERNAME")
def get_elective_username(username):
    return username

@with_config("elective", "PASSWORD")
def get_elective_password(password):
    return password

@with_config("captcha", "TT_USERNAME")
def get_captcha_username(username):
    return username

@with_config("captcha", "TT_PASSWORD")
def get_captcha_password(password):
    return password

@with_config("notifier", "API_KEY")
def get_notifier_api_key(api_key):
    return api_key

if __name__ == "__main__":
    elective_username = get_elective_username()
    elective_password = get_elective_password()
    captcha_username = get_captcha_username()
    captcha_password = get_captcha_password()
    notifier_api_key = get_notifier_api_key()
    print(f"Elective Username: {elective_username}")
    print(f"Elective Password: {elective_password}")
    print(f"Captcha Username: {captcha_username}")
    print(f"Captcha Password: {captcha_password}")
    print(f"Notifier API Key: {notifier_api_key}")
