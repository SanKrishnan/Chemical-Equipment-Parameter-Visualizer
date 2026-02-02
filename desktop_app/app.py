import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit,QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000/api/upload/"
TOKEN = None


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(300, 200, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Login to Continue")
        self.label.setFont(QFont("Segoe UI", 12))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.username = QTextEdit()
        self.username.setPlaceholderText("Username")
        self.username.setFixedHeight(30)
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password) 
        self.password.setFixedHeight(30)
        layout.addWidget(self.password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login_user)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def login_user(self):
        global TOKEN
        username = self.username.toPlainText().strip()
        password = self.password.text().strip()

        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/token/",
                data={"username": username, "password": password}
            )

            if response.status_code == 200:
                TOKEN = response.json().get("access")
                self.close()
            else:
                self.label.setText("Invalid username or password")

        except Exception as e:
            self.label.setText(f"Error: {str(e)}")


# ---------------------- MAIN DESKTOP APP ----------------------
class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Equipment Parameter Visualizer - Desktop App")
        self.setGeometry(200, 200, 600, 400)

        self.last_uploaded_id = None
        self.summary = None

        self.layout = QVBoxLayout()

        self.label = QLabel("Upload CSV File")
        self.label.setFont(QFont("Roboto", 14))
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.upload_button = QPushButton("Choose CSV File")
        self.upload_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.upload_button)

        self.summary_box = QTextEdit()
        self.summary_box.setReadOnly(True)
        self.layout.addWidget(self.summary_box)

        self.chart_button = QPushButton("Show Charts")
        self.chart_button.clicked.connect(self.show_charts)
        self.chart_button.setEnabled(False)
        self.layout.addWidget(self.chart_button)

        # ------------ PDF BUTTON (Correct Location) ------------
        self.pdf_button = QPushButton("Download PDF Report")
        self.pdf_button.clicked.connect(self.download_pdf)
        self.pdf_button.setEnabled(False)
        self.layout.addWidget(self.pdf_button)

        self.setLayout(self.layout)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.send_file_to_api(file_path)

    def send_file_to_api(self, file_path):
        try:
            files = {"file": open(file_path, "rb")}
            headers = {"Authorization": f"Bearer {TOKEN}"}

            response = requests.post(API_URL, files=files, headers=headers)

            if response.status_code == 200:
                data = response.json()
                self.summary = data["summary"]
                self.last_uploaded_id = data["id"]

                self.summary_box.setText(str(self.summary))

                self.chart_button.setEnabled(True)
                self.pdf_button.setEnabled(True)
            else:
                self.summary_box.setText("Error uploading file")

        except Exception as e:
            self.summary_box.setText(f"Error: {str(e)}")

    def show_charts(self):
        if not self.summary:
            self.summary_box.setText("No summary found")
            return

        try:
            labels = list(self.summary["type_distribution"].keys())
            sizes = list(self.summary["type_distribution"].values())

            avg_values = [
                self.summary.get("avg_flowrate", 0),
                self.summary.get("avg_pressure", 0),
                self.summary.get("avg_temperature", 0),
            ]

            fig, axes = plt.subplots(1, 2, figsize=(10, 5))

            # Pie Chart
            axes[0].pie(sizes, labels=labels, autopct="%1.1f%%")
            axes[0].set_title("Equipment Type Distribution")

            # Bar Chart
            axes[1].bar(["Flowrate", "Pressure", "Temperature"], avg_values, color="orange")
            axes[1].set_title("Average Values")

            plt.tight_layout()
            plt.show()

        except Exception as e:
            self.summary_box.append(f"\nChart Error: {str(e)}")

    def download_pdf(self):
        try:
            if not self.last_uploaded_id:
                self.summary_box.append("\nNo file ID found.")
                return

            pdf_url = f"http://127.0.0.1:8000/api/report/{self.last_uploaded_id}/"
            headers = {"Authorization": f"Bearer {TOKEN}"}

            response = requests.get(pdf_url, headers=headers)

            if response.status_code == 200:

                save_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save PDF Report",
                    f"report_{self.last_uploaded_id}.pdf",
                    "PDF Files (*.pdf)"
                )

                if save_path:
                    with open(save_path, "wb") as f:
                        f.write(response.content)
                    self.summary_box.append(f"\nPDF saved at:\n{save_path}")
                else:
                    self.summary_box.append("\nSave cancelled.")

            else:
                self.summary_box.append("\nFailed to download PDF")

        except Exception as e:
            self.summary_box.append(f"\nPDF Error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login = LoginWindow()
    login.show()
    app.exec_()

    window = DesktopApp()
    window.show()

    sys.exit(app.exec_())
