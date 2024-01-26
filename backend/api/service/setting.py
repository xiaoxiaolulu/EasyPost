from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from api.filters.setting import (
    TestEnvironmentFilter,
    AddressFilter
)
from api.models.setting import (
    TestEnvironment,
    Address
)
from api.mixins.magic import (
    MagicListAPI,
    MagicUpdateApi,
    MagicDestroyApi,
    MagicCreateApi
)
from api.schema.setting import (
    TestEnvironmentSerializers,
    AddressSerializers,
    AddressWriteSerializers
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
