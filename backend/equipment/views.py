from django.shortcuts import render
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import FileResponse
from reportlab.pdfgen import canvas
import io

from .models import UploadedCSV
from .serializers import UploadedCSVSerializer

class CSVUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Debug print to verify token is received
        print("AUTH HEADER:", request.headers.get("Authorization"))
        print("USER:", request.user)

        serializer = UploadedCSVSerializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save()

            # Read file
            file_path = instance.file.path
            df = pd.read_csv(file_path)

            # Convert numeric columns
            numeric_cols = ["Flowrate", "Pressure", "Temperature"]
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")

            df = df.dropna(subset=numeric_cols)

            # Summary result
            summary = {
                "total_count": len(df),
                "columns": list(df.columns),
                "avg_flowrate": float(df["Flowrate"].mean()) if "Flowrate" in df else 0,
                "avg_pressure": float(df["Pressure"].mean()) if "Pressure" in df else 0,
                "avg_temperature": float(df["Temperature"].mean()) if "Temperature" in df else 0,
                "type_distribution": df["Type"].value_counts().to_dict() if "Type" in df else {},
            }

            print("SUMMARY:", summary)

            # Save summary to DB
            instance.summary = summary
            instance.save()

            return Response(
                {
                    "message": "CSV uploaded and processed successfully",
                    "id":instance.id,
                    "summary": summary
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UploadHistoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        last_5 = UploadedCSV.objects.order_by('-uploaded_at')[:5]
        serializer = UploadedCSVSerializer(last_5, many=True)
        return Response(serializer.data)

class GeneratePDFView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            record = UploadedCSV.objects.get(id=pk)
        except UploadedCSV.DoesNotExist:
            return Response({"error": "Record not found"}, status=404)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)

        p.drawString(100, 800, "Chemical Equipment Report")
        p.drawString(100, 780, f"File: {record.file.name}")
        p.drawString(100, 760, f"Uploaded At: {record.uploaded_at}")

        summary = record.summary
        y = 730
        for key, value in summary.items():
            p.drawString(100, y, f"{key}: {value}")
            y -= 20

        p.save()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename="equipment_report.pdf")
