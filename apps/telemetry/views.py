from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import TelemetrySerializer 

class TelemetryIngestionView(APIView):
    """
    API endpoint for devices to send real-time telemetry data.
    Ensures device registration and handles duplicates.
    """
   
    permission_classes = [permissions.IsAuthenticated] 

    def post(self, request):
       
        serializer = TelemetrySerializer(data=request.data)
        
        if serializer.is_valid():
          
            serializer.save()
            return Response(
                {
                    "status": "success", 
                    "message": "Telemetry data processed and saved successfully"
                }, 
                status=status.HTTP_201_CREATED
            )
        
       
        return Response(
            {
                "status": "error",
                "errors": serializer.errors
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )