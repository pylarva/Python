from django.db.models.signals import pre_save, post_save


def sg_add_user(sender, **kwargs):
    print(sender, kwargs)

    '''
    < class 'cmdb.models.UserInfo'> {'signal': <django.db.models.signals.ModelSignal object at
    0x1026f75c0 >, 'instance': < UserInfo: UserInfo
    object >, 'raw': False, 'using': 'default', 'update_fields': None}
    '''

    pre_save.connect(sg_add_user)