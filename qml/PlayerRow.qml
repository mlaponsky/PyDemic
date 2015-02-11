import QtQuick 2.2
import QtQuick.Controls 1.1

Row {
    id: players
    width: 5*city.width / 7
    height: icon.height
    anchors.left: icon.left
    anchors.bottom: primary.top

    Repeater {
        id: repeater
        model: 4
        Item { id: player; height: parent.height; width: parent.width / 4 }
    }
}
