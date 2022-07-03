import QtQuick
import QtQuick.Controls

ApplicationWindow {

    id: root_window
    visible: true

    height: 450
    width: 450

    Rectangle {
        id: root
        width: parent.width
        height: parent.height

        function reload() {
            var oldSource = 'image://frameprovider/0';
            image.source = "";
            image.source = oldSource;
        }
        
        Image {
            id: image
            smooth: true
            cache: false
            width: parent.width
            height: parent.height
            source: 'image://frameprovider/0'  
        }
    }
    
    Timer {
        interval: 16
        repeat: true
        running: true
        triggeredOnStart: true
        onTriggered: root.reload()
    }
}