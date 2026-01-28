import sys
import requests
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit
)
from PyQt5.QtGui import QFont
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt


API_URL = "http://127.0.0.1:8000/api/upload/"


class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Equipment Parameter Visualizer - Desktop App")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Upload CSV File")
        self.label.setFont(QFont("Arial", 14))
        layout.addWidget(self.label)

        self.upload_button = QPushButton("Choose CSV File")
        self.upload_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.upload_button)

        self.summary_box = QTextEdit()
        self.summary_box.setReadOnly(True)
        layout.addWidget(self.summary_box)

        self.chart_button = QPushButton("Show Charts")
        self.chart_button.clicked.connect(self.show_charts)
        self.chart_button.setEnabled(False)
        layout.addWidget(self.chart_button)

        self.summary = None
        self.df = None

        self.setLayout(layout)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")

        if file_path:
            self.send_file_to_api(file_path)

    def send_file_to_api(self, file_path):
        try:
            files = {'file': open(file_path, 'rb')}
            response = requests.post(API_URL, files=files)

            if response.status_code == 200:
                data = response.json()
                self.summary = data["summary"]

                self.summary_box.setText(str(self.summary))
                self.chart_button.setEnabled(True)

            else:
                self.summary_box.setText("Error uploading file")

        except Exception as e:
            self.summary_box.setText(f"Error: {str(e)}")

    def show_charts(self):
        if not self.summary:
            self.summary_box.setText("No summary found")
            return

        try:
            # PIE CHART
            labels = list(self.summary["type_distribution"].keys())
            sizes = list(self.summary["type_distribution"].values())

            if len(labels) == 0:
                self.summary_box.append("\nNo type distribution found")
            else:
                plt.figure(figsize=(6, 6))
                plt.pie(sizes, labels=labels, autopct='%1.2f%%')
                plt.title("Equipment Type Distribution")
                plt.show()

            # BAR CHART
            averages = {
                "Flowrate": self.summary.get("avg_flowrate"),
                "Pressure": self.summary.get("avg_pressure"),
                "Temperature": self.summary.get("avg_temperature"),
            }

            avg_keys = list(averages.keys())
            avg_values = [v if v is not None else 0 for v in averages.values()]

            plt.figure(figsize=(6, 4))
            plt.bar(avg_keys, avg_values)
            plt.title("Average Values")
            plt.ylabel("Values")
            plt.show()

        except Exception as e:
            self.summary_box.append(f"\nChart Error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopApp()
    window.show()
    sys.exit(app.exec_())
