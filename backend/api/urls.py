from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter
from api.service.https import (
    ApiFastView,
    TreeView,
    DelApiView,
    ApiDetailView,
    ApiTestListView,
    RunApiView,
    SaveOrUpdateApiView
)
from api.service.project import (
    ProjectListViewSet,
    ProjectDestroyViewSet,
    ProjectUpdateViewSet,
    ProjectCreateViewSet,
    ProjectRetrieveApi,
    ProjectRoleDestroyViewSet,
    ProjectRoleUpdateViewSet
)
from api.service.setting import (
    TestEnvironmentListViewSet,
    TestEnvironmentDestroyViewSet,
    TestEnvironmentUpdateViewSet,
    TestEnvironmentCreateViewSet,
    AddressListViewSet,
    AddressDestroyViewSet,
    AddressUpdateViewSet,
    AddressCreateViewSet
)
from api.service.user import (
    CustomJsonWebToken,
    UserListViewSet
)

router = DefaultRouter()

app_urls = [
    # API
    path("", include(router.urls)),
    # API Authentication
    path("login/", CustomJsonWebToken.as_view()),
    path("user/list", UserListViewSet.as_view()),

    # 项目管理
    path("project/list", ProjectListViewSet.as_view()),
    path("project/delete/<int:pk>", ProjectDestroyViewSet.as_view()),
    path("project/update/<int:pk>", ProjectUpdateViewSet.as_view()),
    path("project/create", ProjectCreateViewSet.as_view()),
    path("project/detail/<int:pk>", ProjectRetrieveApi.as_view()),
    path("project/role/delete", ProjectRoleDestroyViewSet.as_view()),
    path("project/role/add", ProjectRoleUpdateViewSet.as_view()),

    # 测试配置
    path("env/list", TestEnvironmentListViewSet.as_view()),
    path("env/delete/<int:pk>", TestEnvironmentDestroyViewSet.as_view()),
    path("env/update/<int:pk>", TestEnvironmentUpdateViewSet.as_view()),
    path("env/create", TestEnvironmentCreateViewSet.as_view()),
    path("address/list", AddressListViewSet.as_view()),
    path("address/delete/<int:pk>", AddressDestroyViewSet.as_view()),
    path("address/update/<int:pk>", AddressUpdateViewSet.as_view()),
    path("address/create", AddressCreateViewSet.as_view()),

    # 接口测试
    path("http/", ApiFastView.as_view()),
    path("tree/<int:pk>", TreeView.as_view()),
    path("http/delete/<int:pk>", DelApiView.as_view()),
    path("http/detail/<int:pk>", ApiDetailView.as_view()),
    path("http/saveOrUpdate/<int:pk>", SaveOrUpdateApiView.as_view()),
    path("http/list", ApiTestListView.as_view({
        'get': 'list'
    })),
    path('http/run', RunApiView.as_view())
]


# Final URL configuration
app_name = "api"
urlpatterns = app_urls + router.urls
