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
    SaveOrUpdateApiView,
    SaveOrUpdateCaseView,
    RunCaseView,
    DelCaseView,
    CaseDetailView,
    ApiSnapshotView,
    CaseListView, ImportApiView
)
from api.service.plan import (
    UpdatePlanStateView,
    RunPlanView,
    DelPlanView,
    PlanDetailView,
    PlanListViewSet,
    SaveOrUpdatePlanView
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
from api.service.report import (
    ReportDetailView,
    ReportListViewSet
)
from api.service.setting import (
    TestEnvironmentListViewSet,
    TestEnvironmentDestroyViewSet,
    TestEnvironmentUpdateViewSet,
    TestEnvironmentCreateViewSet,
    AddressListViewSet,
    AddressDestroyViewSet,
    AddressUpdateViewSet,
    AddressCreateViewSet,
    DataSourceListViewSet,
    DataSourceDestroyViewSet,
    DataSourceUpdateViewSet,
    DataSourceCreateViewSet,
    DatabaseIsConnectView,
    FunctionSaveOrUpdateApiView,
    GetFunctionListApiView,
    DebugFunctionApiView,
    FunctionsListViewSet
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
    path("database/list", DataSourceListViewSet.as_view()),
    path("database/delete/<int:pk>", DataSourceDestroyViewSet.as_view()),
    path("database/update/<int:pk>", DataSourceUpdateViewSet.as_view()),
    path("database/create", DataSourceCreateViewSet.as_view()),
    path("database/isConnect", DatabaseIsConnectView.as_view()),
    path("function/saveOrUpdate/<int:pk>", FunctionSaveOrUpdateApiView.as_view()),
    path("function/detailList", GetFunctionListApiView.as_view()),
    path("function/debug/<int:pk>", DebugFunctionApiView.as_view()),
    path("function/list", FunctionsListViewSet.as_view()),

    # 接口测试
    path("http/", ApiFastView.as_view()),
    path("tree/<int:pk>&<int:use_type>", TreeView.as_view()),
    path("http/delete/<int:pk>", DelApiView.as_view()),
    path("http/detail/<int:pk>", ApiDetailView.as_view()),
    path("http/saveOrUpdate/<int:pk>", SaveOrUpdateApiView.as_view()),
    path('http/snapshot', ApiSnapshotView.as_view()),
    path("http/list", ApiTestListView.as_view({'get': 'list'})),
    path("http/importApi/<int:pk>", ImportApiView.as_view()),
    path('http/run', RunApiView.as_view()),
    path("case/SaveOrUpdate/<int:pk>", SaveOrUpdateCaseView.as_view()),
    path('case/run', RunCaseView.as_view()),
    path('case/delete/<int:pk>', DelCaseView.as_view()),
    path('case/detail/<int:pk>', CaseDetailView.as_view()),
    path("case/list", CaseListView.as_view({'get': 'list'})),

    # 测试计划
    path("plan/SaveOrUpdate/<int:pk>", SaveOrUpdatePlanView.as_view()),
    path("plan/UpdatePlanState/<int:task_id>/<int:target_status>", UpdatePlanStateView.as_view()),
    path("plan/run", RunPlanView.as_view()),
    path('plan/delete/<int:pk>', DelPlanView.as_view()),
    path('plan/detail/<int:pk>', PlanDetailView.as_view()),
    path("plan/list", PlanListViewSet.as_view()),

    # 测试报告
    path("report/detail", ReportDetailView.as_view({'get': 'list'})),
    path("report/list", ReportListViewSet.as_view())
]

app_name = "api"
urlpatterns = app_urls + router.urls
