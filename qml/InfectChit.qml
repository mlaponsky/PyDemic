import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Window 2.0
import QtGraphicalEffects 1.0

Item {
    id: container
    width: parent.width / 7 - parent.spacing
    height: width
    property string num: "2"
    property color num_color

    RectangularGlow {
        id: glow
        width: parent.width
        height: width
        anchors.top: parent.top
        spread: 0.5
        glowRadius: 4
        cornerRadius: slot.radius + glowRadius
        color: "transparent"
    }

    Rectangle {
        id: slot
        //width: row1.width / 7 - row1.spacing
        width: parent.width
        height: width
        radius: width
        anchors.top: parent.top
        color: game.color
        border.color: "ivory"

        Label {
            id: number
            text: container.num
            font.pixelSize: 16
            color: container.num_color
            anchors.centerIn: parent
        }
    }


    states: [
        State {
            name: "SELECTED"
            PropertyChanges { target: slot; color: border.color }
            PropertyChanges { target: glow; color: slot.color }
        }
    ]
}
