#!/usr/bin/env python3

import sys

# Determine Python binding for Qt to use
try:
    import PySide2.QtWidgets as QtWidgets

    print("Using PySide2")
except ImportError:
    try:
        import PySide.QtGui as QtWidgets

        print("Using PySide1")
    except ImportError:
        try:
            import PyQt5.QtWidgets as QtWidgets

            print("Using PyQt5")
        except:
            print("Cannot start application: No Python Qt-binding available.\n " +
                  "Install at least one of these: PySide1 (python3-pyside), PyQt5 (python3-pyqt5), PySide2")
            sys.exit(1)
import os.path
import traceback
import template


class WizardWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.setWindowTitle("Tim's Alternative Ubuntu Qmake Project Wizard")
        self.setMinimumSize(640, 480)
        self.setContentsMargins(16, 16, 16, 16)

        self.central_widget = QtWidgets.QGroupBox()
        self.central_widget.setTitle("Create Project")
        self.setCentralWidget(self.central_widget)

        self.vbox_central = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.vbox_central)

        self.vbox_central.addWidget(QtWidgets.QLabel("Application name:"))
        self.txt_app_name = QtWidgets.QLineEdit()
        self.txt_app_name.textChanged.connect(self.on_field_changed)
        self.txt_app_name.setPlaceholderText("Application name used in manifest.json")
        self.vbox_central.addWidget(self.txt_app_name)

        self.vbox_central.addWidget(QtWidgets.QLabel("Username:"))
        self.txt_username = QtWidgets.QLineEdit()
        self.txt_username.textChanged.connect(self.on_field_changed)
        self.txt_username.setPlaceholderText("Your Ubuntu Store account username")
        self.vbox_central.addWidget(self.txt_username)

        self.vbox_central.addWidget(QtWidgets.QLabel("Project path:"))
        self.hbox_dest_dir = QtWidgets.QHBoxLayout()
        self.vbox_central.addLayout(self.hbox_dest_dir)

        self.txt_dest_dir = QtWidgets.QLineEdit()
        self.txt_dest_dir.textChanged.connect(self.on_field_changed)
        self.txt_dest_dir.setPlaceholderText("The location where your new project should be created")
        self.hbox_dest_dir.addWidget(self.txt_dest_dir)

        self.vbox_central.addWidget(QtWidgets.QLabel("Please note that you have to create the project folder."))

        self.btn_dest_dir = QtWidgets.QToolButton()
        self.btn_dest_dir.setText("Choose")
        self.btn_dest_dir.clicked.connect(self.on_choose_directory)
        self.hbox_dest_dir.addWidget(self.btn_dest_dir)

        self.vbox_central.addStretch()

        self.hbox_bottom = QtWidgets.QHBoxLayout()
        self.vbox_central.addLayout(self.hbox_bottom)

        self.hbox_bottom.addStretch()

        self.btn_cancel = QtWidgets.QPushButton()
        self.btn_cancel.setText("Cancel")
        self.btn_cancel.clicked.connect(self.close)
        self.hbox_bottom.addWidget(self.btn_cancel)

        self.btn_create = QtWidgets.QPushButton()
        self.btn_create.setEnabled(False)
        self.btn_create.setText("Create")
        self.btn_create.clicked.connect(self.on_create)
        self.hbox_bottom.addWidget(self.btn_create)

    def show_warning(self, text, title="Warning"):
        QtWidgets.QMessageBox.warning(self, title, text)

    def on_field_changed(self):
        ready = True
        if self.txt_app_name.text() == "":
            ready = False
        elif self.txt_dest_dir.text() == "":
            ready = False
        elif self.txt_username.text() == "":
            ready = False
        self.btn_create.setEnabled(ready)

    def on_choose_directory(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose project path")
        self.txt_dest_dir.setText(dir)

    def on_create(self):
        if not os.path.isdir(self.txt_dest_dir.text()):
            self.show_warning("Your destination path does not exist or is not a directory.")
            return
        try:
            template.generate(self.txt_dest_dir.text(), self.txt_app_name.text(), self.txt_username.text())
            QtWidgets.QMessageBox.information(self, "Success", "Your project was created successfully. ")
            self.close()
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("An exception has occured while generating project:")
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                "An exception has occured. Traceback:\n" +
                "".join(t for t in traceback.format_tb(exc_traceback)) + "\n" +
                exc_type.__name__ + ": " + str(e)
            )


def main():
    app = QtWidgets.QApplication([])
    wizard = WizardWindow()
    wizard.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
