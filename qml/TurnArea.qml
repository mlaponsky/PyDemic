import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Window 2.0
import QtGraphicalEffects 1.0

Item {
    property int spacing: parent.spacing
    ActionButtons { id: actions
                    height: parent.height - 2*spacing
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.leftMargin: spacing
                    anchors.left: parent.left
                    width: parent.width * 0.25
    }

    CureBox { width: parent.width*0.13
              anchors.verticalCenter: actions.verticalCenter
              anchors.verticalCenterOffset: -parent.spacing
              anchors.left: actions.right
              anchors.leftMargin: spacing }




}
