import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Window 2.0
import QtGraphicalEffects 1.0

Item {
    id: frame
    width: 450
    height: title.height + counter.height

    Label {
        id: title
        text: qsTr("INFECTION RATE")
        font.pixelSize: 12
        font.family: "ARIAL NARROW"
        font.bold: true
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.horizontalCenterOffset: -counter.spacing
        anchors.top: counter.bottom
        color: "ivory"
    }

    Row {
        id: counter
        width: frame.width
        height: chit.height
        anchors.top: parent.top
        spacing: width / 50

        Repeater {
            id: slots
            model: [
                { num: "2", color: "#c9ffac" },
                { num: "2", color: "#c9ffac" },
                { num: "2", color: "#c9ffac" },
                { num: "3", color: "#92ff57" },
                { num: "3", color: "#92ff57" },
                { num: "4", color: "#4bd400" },
                { num: "4", color: "#4bd400" }
            ]
            InfectChit {id: chit; num: modelData.num; num_color: modelData.color }
        }
    }
 }
