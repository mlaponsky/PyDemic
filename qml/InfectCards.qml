import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Window 2.0

Row {
    id: infect_cards
    x: parent.width * .65
    y: parent.height * .03
    width: parent.width / 4.5
    height: parent.height / 8
    spacing: width - 2*width/2.2

    Rectangle {
        id: infect_deck
        width: parent.width / 2.2
        height: parent.height
        radius: width*0.1
        color: "dark green"
        Text {
            anchors.centerIn: parent
            color: black
            text: "☣"
            font.pointSize: 72
        }
    }

    Rectangle {
        id: infect_discard
        width: parent.width / 2.2
        height: parent.height
        //source: "Pandemic_Images/infect_cards/blank_infect.png"
        radius: width*0.1
        color: "light green"
        opacity: 0.3
    }
}
