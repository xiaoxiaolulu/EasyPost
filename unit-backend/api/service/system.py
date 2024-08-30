from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.dao.setting import SettingDao
from api.response.fatcory import ResponseStandard


class MenuView(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, **kwargs):

        try:
            response = SettingDao.all_menu_nesting()
            return Response(ResponseStandard.success(data=response))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))
