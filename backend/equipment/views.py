from django.shortcuts import render

import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedCSV
from .serializers import UploadedCSVSerializer

class CSVUploadView(APIView):
    def post(self, request):
        serializer = UploadedCSVSerializer(data=request.data)
        
        if serializer.is_valid():
            instance = serializer.save()

            #Read CSV
            file_path = instance.file.path
            df = pd.read_csv(file_path)

            #Compute summary
            summary = {
                "total_count": len(df),
                "columns": list(df.columns),
                "avg_flowrate": df["Flowrate"].mean() if "Flowrate" in df else None,
                "avg_pressure": df["Pressure"].mean() if "Pressure" in df else None,
                "avg_temperature": df["Temperature"].mean() if "Temperature" in df else None,
                "type_distribution": df["Type"].value_counts().to_dict() if "Type" in df else {},
            }

            #Save summary
            instance.summary = summary
            instance.save()

            return Response({
                "message": "CSV uploaded and processed successfully",
                "summary": summary
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadHistoryView(APIView):
    def get(self, request):
        last_5 = UploadedCSV.objects.order_by('-uploaded_at')[:5]
        serializer = UploadedCSVSerializer(last_5, many=True)
        return Response(serializer.data)
