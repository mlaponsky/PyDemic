import QtQuick 2.2
import QtQuick.Controls 1.1
import QtGraphicalEffects 1.0

Item {
    height: cures.y + cures.height
    property int spacing: width / 8

    Label {
        id: cures_label
        anchors.horizontalCenter: cures.horizontalCenter
        anchors.horizontalCenterOffset: -cures.spacing/2

        text: "CURES"
        font.pixelSize: 18
        font.bold: true
        color: "white"
    }

    Row {
        id: cures
        width: parent.width
        height: width/4 - spacing
        spacing: parent.spacing
        y: cures_label.height + cures_label.height*0.5
        signal cured(int index)
        Repeater {
            id: repeater
            model: ["#75a4ff", "#ffe680", "black", "#ff8080"]
            Cure { cureColor: modelData }
        }
    }
}
