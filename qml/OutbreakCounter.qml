import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Window 2.0
import QtGraphicalEffects 1.0

Item {
    id: frame
    width: 100
    height: 5*(width/2 + width / 8) + 3*title.height/2

    Label {
        id: title
        text: qsTr("OUTBREAKS")
        font.pixelSize: 14
        font.family: "ARIAL NARROW"
        font.bold: true
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        color: "ivory"
    }

    Item {
        id: counter
        anchors.top: title.bottom
        height: parent.height - title.height/2
        anchors.topMargin: -3
        width: parent.width
        property int spacing: width / 8
        x: 0

        Repeater {
            id: slots
            model: ["#ffcaca", "#ed8585", "#e88b8b", "#e68585", "#d96a6a", "#d44c4c", "#d12a2a", "#cc1818", "#cc0000"]
            OutbreakChit { id: chit
                           num: (index != 8) ? index : '☠'
                           x: parent.x + (index % 2)*width
                           y: parent.y + index*height/2 + index*counter.spacing / 2
                           num_color: modelData }
        }
    }
 }

