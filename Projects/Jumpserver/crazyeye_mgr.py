import os

if __name__ == "__main__":
    # 自定义的脚本需要访问Django的数据库 需先设置环境变量
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Jumpserver.settings")
    # 将所以的app加载一遍然后 import 脚本
    import django
    django.setup()
    from backend import main

    obj = main.HostManager()
    obj.interactive()
