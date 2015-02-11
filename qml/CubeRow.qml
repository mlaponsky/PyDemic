import QtQuick 2.2
import QtQuick.Controls 1.1

Row {
    id: cubes
    width: parent.width * (3/7)
    height: width/3
    anchors.left: parent.horizontalCenter
    property int sourceX
    property int sourceY

    Repeater {
        id: repeater
        model: 3
        Item { id: cube; height: parent.height; width: height }
    }
}
