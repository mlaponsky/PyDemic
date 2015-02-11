import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Window 2.0

ApplicationWindow {
    title: qsTr("PyDemic")
    width: Screen.width
    height: Screen.height
    visible: true


    menuBar: MenuBar {
        Menu {
            title: qsTr("File")
            MenuItem {
                text: qsTr("Exit")
                onTriggered: Qt.quit();
            }
        }
    }

    Rectangle {
        id: game
        anchors.fill: parent
        width: parent.width
        height: parent.height
        color: "#3d3d3d"
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        property int spacing: width * 0.005

        TurnArea {
            id: turn
            height: parent.height - background.height
            width: parent.width
            anchors.top: background.bottom
            anchors.left: parent.left
        }

        Image {
            id: background
            anchors.top: parent.top
            anchors.left: parent.left
            width: height*1.84123
            height: parent.height*0.84
            anchors.leftMargin: 0
            anchors.topMargin: 0
            source: "Pandemic_Images/board.png"

            PlayerCards { id: player_cards; x: 1005; y: 676 }

            InfectCards{ id: infect_cards; x: 1016; y: 21}

            InfectCounter {
                id: infect_rate
                width: infect_cards.width * .75
                anchors.topMargin: game.spacing
                anchors.horizontalCenter: infect_cards.horizontalCenter
                anchors.top: infect_cards.bottom
            }

            OutbreakCounter {
                id: outbreaks
                x: 84
                y: 521
                width: parent.width*0.05
            }

            Cities { }
            //CityLabels { }

//            Text {
//                x: 1540
//                y: 858
//                text: "SYDNEY"
//                font.family: "ARIAL NARROW"
//                font.pointSize: 8
//                color: "ivory"
//            }

//            City {
//                id: new_york
//                x: 389
//                y: 214
//                width: parent.width*0.05
//                cityColor: "#75a4ff"
//                onHover: "yellow"
//            }

//            City {
//                id: washington
//                x: 310
//                y: 273
//                width: parent.width*0.05
//                cityColor: "#75a4ff"
//                onHover: "yellow"
//            }

//            City {
//                id: montreal
//                x: 297
//                y: 179
//                width: parent.width*0.05
//            }

//            City {
//                id: chicago
//                x: 166
//                y: 200
//                width: parent.width*0.05
//            }

//            City {
//                id: atlanta
//                x: 221
//                y: 291
//                width: parent.width*0.05
//            }

//            City {
//                id: lima
//                x: 294
//                y: 597
//                width: parent.width*0.05
//            }

//            City {
//                id: mexico_city
//                x: 161
//                y: 386
//                width: parent.width*0.05
//            }

//            City {
//                id: los_angeles
//                x: 25
//                y: 322
//                width: parent.width*0.05
//            }

//            City {
//                id: san_francisco
//                x: 35
//                y: 239
//                width: parent.width*0.05
//            }

//            City {
//                id: miami
//                x: 271
//                y: 348
//                width: parent.width*0.05
//            }

//            City {
//                id:bogota
//                x: 315
//                y: 494
//                width: parent.width*0.05
//            }

//            City {
//                id: santiago
//                x: 275
//                y: 751
//                width: parent.width*0.05
//            }

//            City {
//                id: buenos_aires
//                x: 389
//                y: 754
//                width: parent.width*0.05
//            }

//            City {
//                id: sao_paulo
//                x: 460
//                y: 680
//                width: parent.width*0.05
//            }

//            City {
//                id: lagos
//                x: 745
//                y: 475
//                width: parent.width*0.05
//            }

//            City {
//                id: kinshasa
//                x: 807
//                y: 525
//                width: parent.width*0.05
//            }

//            City {
//                id: johannesburg
//                x: 858
//                y: 713
//                width: parent.width*0.05
//            }

//            City {
//                id: khartoum
//                x: 889
//                y: 412
//                width: parent.width*0.05
//            }

//            City {
//                id: cairo
//                x: 882
//                y: 325
//                width: parent.width*0.05
//            }

//            City {
//                id: algiers
//                x: 731
//                y: 274
//                width: parent.width*0.05
//            }

//            City {
//                id: madrid
//                x: 614
//                y: 249
//                width: parent.width*0.05
//            }

//            City {
//                id: london
//                x: 643
//                y: 110
//                width: parent.width*0.05
//            }

//            City {
//                id: paris
//                x: 727
//                y: 184
//                width: parent.width*0.05
//            }

//            City {
//                id: milan
//                x: 813
//                y: 173
//                width: parent.width*0.05
//            }

//            City {
//                id: essen
//                x: 786
//                y: 67
//                width: parent.width*0.05
//            }

//            City {
//                id: st_petersburg
//                x: 893
//                y: 85
//                width: parent.width*0.05
//            }

//            City {
//                id: istanbul
//                x: 871
//                y: 235
//                width: parent.width*0.05
//            }

//            City {
//                id: moscow
//                x: 975
//                y: 168
//                width: parent.width*0.05
//            }

//            City {
//                id: tehran
//                x: 1020
//                y: 237
//                width: parent.width*0.05
//            }

//            City {
//                id: baghdad
//                x: 953
//                y: 279
//                width: parent.width*0.05
//            }

//            City {
//                id: riyadh
//                x: 971
//                y: 381
//                width: parent.width*0.05
//            }

//            City {
//                id: karachi
//                x: 1072
//                y: 327
//                width: parent.width*0.05
//            }

//            City {
//                id: delhi
//                x: 1152
//                y: 264
//                width: parent.width*0.05
//            }

//            City {
//                id: mumbai
//                x: 1075
//                y: 406
//                width: parent.width*0.05
//            }

//            City {
//                id: chennai
//                x: 1149
//                y: 451
//                width: parent.width*0.05
//            }

//            City {
//                id: kolkata
//                x: 1206
//                y: 330
//                width: parent.width*0.05
//            }

//            City {
//                id: bangkok
//                x: 1268
//                y: 407
//                width: parent.width*0.05
//            }

//            City {
//                id: hongkong
//                x: 1327
//                y: 343
//                width: parent.width*0.05
//            }

//            City {
//                id: shanghai
//                x: 1328
//                y: 249
//                width: parent.width*0.05
//            }

//            City {
//                id: beijing
//                x: 1347
//                y: 173
//                width: parent.width*0.05
//            }

//            City {
//                id: seoul
//                x: 1448
//                y: 198
//                width: parent.width*0.05
//            }

//            City {
//                id: tokyo
//                x: 1544
//                y: 266
//                width: parent.width*0.05
//            }

//            City {
//                id: osaka
//                x: 1523
//                y: 361
//                width: parent.width*0.05
//            }

//            City {
//                id: taipei
//                x: 1428
//                y: 399
//                width: parent.width*0.05
//            }

//            City {
//                id: manila
//                x: 1414
//                y: 508
//                width: parent.width*0.05
//            }

//            City {
//                id: ho_chi_minh_city
//                x: 1321
//                y: 480
//                width: parent.width*0.05
//            }

//            City {
//                id: jakarta
//                x: 1254
//                y: 567
//                width: parent.width*0.05
//            }

//            City {
//                id: sydney
//                x: 1532
//                y: 770
//                width: parent.width*0.05
//            }
        }
    }
}
