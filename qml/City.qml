import QtQuick 2.2
import QtQuick.Controls 1.1
import QtGraphicalEffects 1.0

Item {
    id: city
    width: background.width*0.05
    height: width
    x: background.x + (absX/1670)*background.width
    y: background.y + (absY/907)*background.height

    property color cityColor: "#ffe680"
    property color onHover: "#acff00"
    property color onClick: "purple"
    property string name: "WASHINGTON"
    property int absX
    property int absY

    RectangularGlow {
        id: outline
        width: parent.width*(3/7)
        height: width
        glowRadius: width * 0.1
        spread: 0.8
        color: "ivory"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        cornerRadius: icon.radius + glowRadius
    }

    Rectangle {
        id: icon
        objectName: name
        width: parent.width*(3/7)
        height: width
        radius: width
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        color: parent.cityColor
        border.color: color
        border.width: width*0.1

        SequentialAnimation {
            id: flashing
            running: false
            loops: Animation.Infinite

            OpacityAnimator { target: icon; from: 1; to: 0.3; duration: 200; easing.type: Easing.InOutQuad }
            PauseAnimation { duration: 50 }
            OpacityAnimator { target: icon; from: 0.3; to: 1; duration: 200; easing.type: Easing.InOutQuad }
            PauseAnimation { duration: 50 }
        }
    }

    MouseArea {
        id: interactive
        anchors.fill: icon
        hoverEnabled: false
        enabled: false
        onEntered: icon.border.color = onHover
        onExited: icon.border.color = cityColor
        onPressed: icon.border.color = onClick
        onReleased: icon.border.color = onHover
    }

    CubeRow { id: primary; anchors.verticalCenter: icon.verticalCenter }
    CubeRow { id: secondary; anchors.top: primary.bottom }

    PlayerRow { id: player }

    Image {
        id: station
        sourceSize.width: parent.width*(3/14)
        sourceSize.height: parent.height*(3/14)
        source: "Pandemic_Images/markers/research_station.png"
        opacity: 0.0
        anchors.right: icon.left
        anchors.bottom: icon.bottom
    }

    Text { id: label
           anchors.top: icon.bottom
           anchors.topMargin: icon.height*0.1
           anchors.horizontalCenter: icon.horizontalCenter
           color: "ivory"
           text: city.name
           font.pixelSize: 12
           font.family: "ARIAL NARROW" }



    states: [
        State {
            name: "AVAILABLE"
            PropertyChanges { target: interactive; hoverEnabled: true; enabled: true }
        },

        State {
            name: "UNAVAILABLE"
            PropertyChanges { target: interactive; hoverEnabled: false; enabled: false }
        },

        State {
            name: "RESEARCH"
            PropertyChanges { target: station; opacity: 1.0 }
        },

        State {
            name: "OUTBREAK"
            PropertyChanges { target: flashing; running: true }
            PropertyChanges { target: outline; color: "orange"; glowRadius: width * 0.2 }
        }
    ]
}
