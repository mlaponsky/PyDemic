import QtQuick 2.0

Item {

    Rectangle {
        id: role
        width: game.width - background.width
        height: game.height - background.height
        property string name
        property color roleColor

        Text {
            text: name
            font.family: "ARIAL"
            font.pixelSize: 40
            anchors.horizontalCenter: parent.horizontalCenter
            y: parent.y + 0.15*parent.height
        }

        Rectangle {
            height:(1/3)*parent.height
            width: height
            radius: height
            color: game.color
            border.width: width*0.3
            border.color: parent.roleColor
        }
    }
}
