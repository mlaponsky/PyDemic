import QtQuick 2.2
import QtQuick.Controls 1.1

Rectangle {
    id: button
    color: "#bdbdbd"
    property alias text: label.text
    border {color: "#636363"; width: 1}
    radius: height*0.2

    Text {
        id: label
        anchors.centerIn: parent
        text: "Click Me!"
        font.pixelSize: 12
        color: "#525252"
    }

    MouseArea {
        id: to_click
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        anchors.fill: parent
        onPressed: parent.state = "clicked"
        onReleased: parent.state = "clickable"
    }
    states: [
        State {
            name: "clickable"
            PropertyChanges { target: button; opacity: 1.0 }
            PropertyChanges { target: to_click; enabled: true }
        },

        State {
            name: "unclickable"
            PropertyChanges { target: button; opacity: 0.7 }
            PropertyChanges { target: to_click; enabled: false }
        },

        State {
            name: "clicked"
            PropertyChanges { target: button; color: "darkgrey"}
        }




    ]
}

