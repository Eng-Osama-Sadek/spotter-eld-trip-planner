from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TripRequestSerializer
from .services.trip_planner import plan_trip


class PlanTripView(APIView):
    def post(self, request):
        serializer = TripRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = plan_trip(**serializer.validated_data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            return Response({"error": f"Unexpected error: {e}"}, status=500)
        return Response(result, status=status.HTTP_200_OK)
