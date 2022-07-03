
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QResource, Qt, QCoreApplication
from Backend.FrameProvider import FrameProvider

import sys

if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()

    QResource.registerResource("main.rcc")
    
    frame_provider = FrameProvider()

    frame_provider.open_camera(0)   
    
    engine.addImageProvider('frameprovider', frame_provider)
    
    engine.load('qrc:/main.qml')

    sys.exit(app.exec())