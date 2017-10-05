# 自定义admin功能最终要生成一个类似如下的大字典 供前端显示
# sites = {
#     'crm':{
#         'customers':CustomerAdmin,
#         'customerfollowup':CustomerFollowUPAdmin,
#     }
# }


class AdminRegisterException(Exception):
    """
    自定义报错信息
    """
    def __init__(self, msg):
        self.message = msg


class BaseAdmin(object):
    """
    没有自定义条件的admin大字典
    """
    list_display = ()
    list_filter = ()
    search_fields = ()


class AdminSite(object):
    """
    用来生成有自定义条件的admin功能大字典
    """
    def __init__(self):
        # 定义空字典
        self.registered_sites = {}

    def register(self, model, admin_class=None):
        app_name = model._meta.app_label
        model_name = model._meta.model_name
        print(app_name, model_name)

        if app_name not in self.registered_sites:
            self.registered_sites[app_name] = {}

        if model_name in self.registered_sites[app_name]:
            raise AdminRegisterException("app [%s] model [%s] has already registered!" % (app_name, model_name))

        if not admin_class:
            admin_class = BaseAdmin
        admin_obj = admin_class()
        admin_obj.model = model

        self.registered_sites[app_name][model_name] = admin_obj
        print(self.registered_sites)

# 实例化注册类 会得到一个全局变量registered_sites
# {'crm': {'customer': <crm.kingadmin.CustomerAdmin object at 0x104006240>}}
site = AdminSite()
