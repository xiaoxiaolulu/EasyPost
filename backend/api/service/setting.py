import json
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.dao.setting import SettingDao
from api.filters.setting import (
    TestEnvironmentFilter,
    AddressFilter,
    DataSourceFilter
)
from api.models.setting import (
    TestEnvironment,
    Address,
    DataSource
)
from api.mixins.magic import (
    MagicListAPI,
    MagicUpdateApi,
    MagicDestroyApi,
    MagicCreateApi
)
from api.response.fatcory import ResponseStandard
from api.schema.setting import (
    TestEnvironmentSerializers,
    AddressSerializers,
    AddressWriteSerializers,
    DataSourceSerializers
)


class TestEnvironmentListViewSet(MagicListAPI): # noqa

    queryset = TestEnvironment.objects.all()
    serializer_class = TestEnvironmentSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TestEnvironmentFilter   # noqa
    search_fields = ['name']
    ordering_fields = ['create_time']


class TestEnvironmentDestroyViewSet(MagicDestroyApi):

    queryset = TestEnvironment.objects.all()
    serializer_class = TestEnvironmentSerializers
    permission_classes = [IsAuthenticated]
    

class TestEnvironmentUpdateViewSet(MagicUpdateApi):

    queryset = TestEnvironment.objects.all()
    serializer_class = TestEnvironmentSerializers
    permission_classes = [IsAuthenticated]


class TestEnvironmentCreateViewSet(MagicCreateApi):

    queryset = TestEnvironment.objects.all()
    serializer_class = TestEnvironmentSerializers
    permission_classes = [IsAuthenticated]
    

class AddressListViewSet(MagicListAPI):  # noqa

    queryset = Address.objects.all()
    serializer_class = AddressSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AddressFilter  # noqa
    search_fields = ['name']
    ordering_fields = ['create_time']


class AddressDestroyViewSet(MagicDestroyApi):  # noqa

    queryset = Address.objects.all()
    serializer_class = AddressSerializers
    permission_classes = [IsAuthenticated]


class AddressUpdateViewSet(MagicUpdateApi):

    queryset = Address.objects.all()
    serializer_class = AddressWriteSerializers
    permission_classes = [IsAuthenticated]
    

class AddressCreateViewSet(MagicCreateApi):  # noqa

    queryset = Address.objects.all()
    serializer_class = AddressWriteSerializers
    permission_classes = [IsAuthenticated]


class DataSourceListViewSet(MagicListAPI):  # noqa

    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DataSourceFilter  # noqa
    search_fields = ['database']
    ordering_fields = ['create_time']


class DataSourceDestroyViewSet(MagicDestroyApi):  # noqa

    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializers
    permission_classes = [IsAuthenticated]


class DataSourceUpdateViewSet(MagicUpdateApi):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializers
    permission_classes = [IsAuthenticated]


class DataSourceCreateViewSet(MagicCreateApi):  # noqa

    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializers
    permission_classes = [IsAuthenticated]


class DatabaseIsConnectView(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            request_body = json.loads(request.body.decode())
            ret = SettingDao.database_is_connect(config=request_body)
            return Response(ResponseStandard.success(
                data={"database_status": ret}
            ))
        except Exception as err:
            return Response(ResponseStandard.failed(err))


class FunctionSaveOrUpdateApiView(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, **kwargs):

        try:
            dao = SettingDao()
            response = dao.edit_builtin_function(request.data, kwargs['pk'])
            return Response(ResponseStandard.success(
                data={"func_id": response}
            ))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class GetFunctionListApiView(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, **kwargs):

        try:
            dao = SettingDao()
            response = dao.get_function_by_id(request.data, kwargs['pk'])
            return Response(ResponseStandard.success(
                data=response.get('func_list', [])
            ))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class DebugFunctionApiView(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, **kwargs):

        try:
            dao = SettingDao()
            response = dao.run_function(request.data, kwargs['pk'])
            return Response(ResponseStandard.success(
                data={"ret": response}
            ))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))
