from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.dao.dashboard import DashboardDao
from api.response.fatcory import ResponseStandard


class StatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, **kwargs):

        try:
            dashboard = DashboardDao()
            ret = dashboard.summary(request)
            return Response(ResponseStandard.success(
                data={"summary": ret}
            ))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))
