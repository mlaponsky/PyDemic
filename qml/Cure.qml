import QtQuick 2.0

Rectangle {
    id: cure
    width: parent.height
    height: width
    color: "transparent"
    radius: width
    border.width: width*.1
    border.color: cureColor

    property color cureColor

    states: [
        State {
            name: "CURED"
            PropertyChanges { target: cure; color: cureColor }
        },

        State {
            name: "ERADICATED"
            PropertyChanges { target: cure; border.color: cureColor; border.width: width * 0.2; color: "ivory" }
        }

    ]
}
