from django.contrib import admin

from web import models
# Register your models here.


from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from web.models import UserProfile


class UserCreationForm(forms.ModelForm):
    """ 定制admin需要改的三个类--之一创建用户
    A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        # 在字段前加个clean会自动执行这个字段的验证
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """ 定制admin需要改的三个类--之二
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(BaseUserAdmin):
    """ 定制admin需要改的三个类--之三 """
    # The forms to add and change user instances

    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    # 字段显示列
    list_display = ('email', 'name', 'is_staff', 'is_admin')
    list_filter = ('is_admin', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # Personal info: name字段显示会加个蓝分割条
        ('Personal info', {'fields': ('name',)}),
        # 显示一个主机授权控件 支持M2M多选
        ('堡垒机主机授权', {'fields': ('bind_hosts', 'host_groups')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'user_permissions', 'groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    # filter_horizontal 多选式样
    filter_horizontal = ('user_permissions', 'groups', 'bind_hosts', 'host_groups')

# Now register the new UserAdmin...
admin.site.register(models.UserProfile, UserProfileAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


class RemoteUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'auth_type', 'password')


admin.site.register(models.Host)
admin.site.register(models.HostGroup)
admin.site.register(models.BindHost)
admin.site.register(models.RemoteUser, RemoteUserAdmin)
admin.site.register(models.IDC)
# admin.site.register(models.Session)
