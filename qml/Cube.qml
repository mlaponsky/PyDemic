import QtQuick 2.2
import QtQuick.Controls 1.1

/* This is the cube object. It is always instantiated with spcified image source and parent container*/
Image {
    id: cube

    ParallelAnimation {
        id: move
        NumberAnimation { target: cube; property: x; to: parent.x; duration: 500; easing.type: Easing.InOutQuad }
        NumberAnimation { target: cube; property: y; to: parent.y; duration: 500; easing.type: Easing.InOutQuad }
    }
}
