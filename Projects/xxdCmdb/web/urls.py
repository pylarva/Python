from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from web.views import account
from web.views import home
from web.views import asset
from web.views import config
from web.views import user
from web.views import group
from web.views import authorize
from web.views import authorizer
from web.views import read
from web.views import business
from web.views import PhysicalMachine
from web.views import VirtualMachine
from web.views import project
from web.views import projects
from web.views import project_admin
from web.views import release
from web.views import apply
from web.views import apply_read
from web.views import audit
from web.views import audit_db
from web.views import audit_sa
from web.views import logs
from web.views import document

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
    # url(r'^asset-(?P<device_type_id>\d+)-(?P<asset_nid>\d+).html$', asset.AssetDetailView.as_view()),
    url(r'^asset-(?P<nid>\d+).html$', asset.AssetDetailView.as_view()),
    url(r'^release-(?P<nid>\d+).html$', asset.ReleaseDetailView.as_view()),
    url(r'^add-asset.html$', asset.AddAssetView.as_view()),

    url(r'^config.html$', config.AssetListView.as_view()),
    url(r'^configs.html$', config.ConfigListView.as_view()),

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

    url(r'^user.html$', user.UserListView.as_view()),
    url(r'^users.html$', user.UserJsonView.as_view()),

    url(r'^group.html$', group.GroupListView.as_view()),
    url(r'^groups.html$', group.GroupJsonView.as_view()),

    url(r'^_project.html$', project.ProjectListView.as_view()),
    # 开发-项目列表
    url(r'^project_list.html$', projects.ProjectsListView.as_view()),
    url(r'^projects_list.html$', projects.ProjectsJsonView.as_view()),
    url(r'^projects_list_r.html$', projects.ProjectsJsonReadView.as_view()),

    # admin-项目列表
    url(r'^project_admin.html$', project_admin.ProjectAdminListView.as_view()),
    url(r'^project_admins.html$', project_admin.ProjectAdminJsonView.as_view()),

    # 普通用户-项目列表
    url(r'^projects_read.html$', projects.ProjectListView.as_view()),
    url(r'^projects_reads.html$', projects.ProjectJsonReadView.as_view()),

    url(r'^project_list_r.html$', projects.ProjectsReadListView.as_view()),
    url(r'^projects_list_r.html$', projects.ProjectsJsonReadView.as_view()),

    url(r'^release.html$', release.ReleaseListView.as_view()),
    url(r'^releases.html$', release.ReleaseJsonView.as_view()),

    url(r'^apply.html$', apply.ApplyListView.as_view()),
    url(r'^applys.html$', apply.ApplyJsonView.as_view()),

    url(r'^apply_read.html$', apply_read.ApplyListView.as_view()),
    url(r'^apply_reads.html$', apply_read.ApplyJsonView.as_view()),

    url(r'^audit.html$', audit.ApplyListView.as_view()),
    url(r'^audits.html$', audit.ApplyJsonView.as_view()),

    url(r'^audit_db.html$', audit_db.ApplyListView.as_view()),
    url(r'^audits_db.html$', audit_db.ApplyJsonView.as_view()),

    url(r'^audit_sa.html$', audit_sa.ApplyListView.as_view()),
    url(r'^audits_sa.html$', audit_sa.ApplyJsonView.as_view()),

    url(r'^release_r.html$', release.ReleaseReadListView.as_view()),
    url(r'^releases_r.html$', release.ReleaseJsonView.as_view()),

    url(r'^release_log.html$', logs.ReleaseLogJsonView.as_view()),

    url(r'^ldap.html$', user.LdapListView.as_view()),

    url(r'^chart-(?P<chart_type>\w+).html$', home.ChartView.as_view()),

    url(r'^document-(?P<nid>\d+).html$', document.DocumentListView.as_view()),
]
