import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Window 2.0


Row {
    id: player_cards
    x: 1050
    y: 696
    width: parent.width / 6.4
    height: parent.height / 5.1
    spacing: width - 2*width/2.2

    Rectangle {
        id: player_deck
        width: parent.width / 2.2
        height: parent.height
        radius: width*0.1
        color: "navy"
        Text {
            anchors.centerIn: parent
            color: "light blue"
            font.pointSize: 72
            text: "✙"
        }
    }

    Rectangle {
        id: player_discard
        width: parent.width / 2.2
        height: parent.height
        radius: width*0.1
        color: "#add9e6"
        opacity: 0.3
    }
}

