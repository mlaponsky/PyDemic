import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Window 2.0
import QtGraphicalEffects 1.0

Item {
    width: parent.width*0.5
    height: width
    property string num
    property color num_color

    RectangularGlow {
        id: glow
        width: parent.width
        height: width
        anchors.fill: parent
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
        anchors.fill:parent
        color: "transparent"
        border.color: "ivory"
    }

    Text {
        id: number
        anchors.centerIn: slot
        text: parent.num
        color: num_color
        font.pixelSize: 14
    }

    states: [
        State {
            name: "SELECTED"
            PropertyChanges { target: slot; color: "ivory" }
            PropertyChanges { target: glow; color: slot.color }
        }
    ]
}
