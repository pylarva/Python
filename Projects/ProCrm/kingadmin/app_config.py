
from django import conf


for app in conf.settings.INSTALLED_APPS:
    try:
        print("import ", __import__("%s.kingadmin" % app))
    except ImportError as e:
        pass
        # print("app has no module kingadmin")