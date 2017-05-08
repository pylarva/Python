from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from web.views import account
from web.views import home
from web.views import asset
from web.views import user
from web.views import group
from web.views import authorize
from web.views import authorizer
from web.views import read
from web.views import business
from web.views import PhysicalMachine
from web.views import VirtualMachine

urlpatterns = [
    url(r'^login.html$', account.LoginView.as_view()),
    url(r'^logout.html$', account.LogoutView.as_view()),
    url(r'^index.html$', home.IndexView.as_view()),
    url(r'^cmdb.html$', home.CmdbView.as_view()),
    url(r'^task.html$', home.TaskView.as_view()),
    url(r'^task_physical.html$', PhysicalMachine.PhysicalListView.as_view()),
    url(r'^task_virtual.html', VirtualMachine.VirtualListView.as_view()),
    url(r'^virtual_list.html', VirtualMachine.VirtualListView.as_view()),
    url(r'^asset.html$', asset.AssetListView.as_view()),
    url(r'^assets.html$', asset.AssetJsonView.as_view()),
    url(r'^asset-(?P<device_type_id>\d+)-(?P<asset_nid>\d+).html$', asset.AssetDetailView.as_view()),
    url(r'^add-asset.html$', asset.AddAssetView.as_view()),

    url(r'^read.html$', read.ReadListView.as_view()),
    url(r'^reads.html$', read.ReadJsonView.as_view()),

    url(r'^authorize.html$', authorize.AuthListView.as_view()),
    url(r'^authorizes.html$', authorize.AuthJsonView.as_view()),

    url(r'^authorizer.html$', authorizer.AuthListView.as_view()),
    url(r'^authorizers.html$', authorizer.AuthJsonView.as_view()),

    url(r'^business_1.html$', business.Business1ListView.as_view()),
    url(r'^business_1s.html$', business.Business1JsonView.as_view()),

    url(r'^business_2.html$', business.Business2ListView.as_view()),
    url(r'^business_2s.html$', business.Business2JsonView.as_view()),

    url(r'^business_3.html$', business.Business3ListView.as_view()),
    url(r'^business_3s.html$', business.Business3JsonView.as_view()),

    url(r'^users.html$', user.UserListView.as_view()),
    url(r'^user.html$', user.UserJsonView.as_view()),

    url(r'^group.html$', group.GroupListView.as_view()),
    url(r'^groups.html$', group.GroupJsonView.as_view()),

    url(r'^ldap.html$', user.LdapListView.as_view()),

    url(r'^chart-(?P<chart_type>\w+).html$', home.ChartView.as_view()),


]
