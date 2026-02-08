import sys
import os
from PIL import Image
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QFileDialog, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QMessageBox
)

class ImageTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Crop & Resize Tool")
        self.setGeometry(200, 200, 400, 250)

        self.image_path = []

        layout = QVBoxLayout()

        # Select Image Button
        self.btn_select = QPushButton("Select Image")
        self.btn_select.clicked.connect(self.select_image)
        layout.addWidget(self.btn_select)

        # Show selected image
        self.label_path = QLabel("No image selected")
        layout.addWidget(self.label_path)

        # Width & Height inputs
        size_layout = QHBoxLayout()
        self.input_width = QLineEdit("1080")
        self.input_height = QLineEdit("1080")
        size_layout.addWidget(QLabel("Width:"))
        size_layout.addWidget(self.input_width)
        size_layout.addWidget(QLabel("Height:"))
        size_layout.addWidget(self.input_height)
        layout.addLayout(size_layout)

        # Format selection
        format_layout = QHBoxLayout()
        self.combo_format = QComboBox()
        self.combo_format.addItems(["jpg", "png", "webp"])
        format_layout.addWidget(QLabel("Output Format:"))
        format_layout.addWidget(self.combo_format)
        layout.addLayout(format_layout)

        # Process button
        self.btn_process = QPushButton("Crop & Resize")
        self.btn_process.clicked.connect(self.process_image)
        layout.addWidget(self.btn_process)

        self.setLayout(layout)

    def select_image(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            "Images (*.png *.jpg *.jpeg *.webp)"
        )
        if files:
            self.image_paths = files
            self.label_path.setText(f"{len(files)} images selected")


    def center_crop(self, img):
        width, height = img.size
        min_dim = min(width, height)

        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim

        return img.crop((left, top, right, bottom))

    def process_image(self):
        if not self.image_paths:
            QMessageBox.warning(self, "Error", "Please select images first.")
            return

        try:
            width = int(self.input_width.text())
            height = int(self.input_height.text())
            output_format = self.combo_format.currentText()

            success_count = 0

            for path in self.image_paths:
                img = Image.open(path)
                img = self.center_crop(img)
                img = img.resize((width, height), Image.LANCZOS)

                base_name = os.path.splitext(os.path.basename(path))[0]
                save_path = os.path.join(
                    os.path.dirname(path),
                    f"{base_name}_{width}x{height}.{output_format}"
                )

                if output_format == "jpg":
                    img = img.convert("RGB")

                img.save(save_path)
                success_count += 1

            QMessageBox.information(
                self,
                "Success",
                f"{success_count} images processed successfully!"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageTool()
    window.show()
    sys.exit(app.exec_())
