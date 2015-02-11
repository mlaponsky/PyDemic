import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Window 2.0

Repeater {
    id: city_list
    model: [
        { X: 35, Y: 239, name: "SAN FRANCISCO", color: "#75a4ff" },
        { X: 166, Y: 200, name: "CHICAGO", color: "#75a4ff" },
        { X: 297, Y: 179, name: "MONTREAL", color: "#75a4ff" },
        { X: 389, Y: 214, name: "NEW YORK", color: "#75a4ff" },
        { X: 310, Y: 273, name: "WASHINGTON", color: "#75a4ff" },
        { X: 221, Y: 291, name: "ATLANTA", color: "#75a4ff" },
        { X: 614, Y: 249, name: "MADRID", color: "#75a4ff" },
        { X: 643, Y: 110, name: "LONDON", color: "#75a4ff" },
        { X: 727, Y: 184, name: "PARIS", color: "#75a4ff" },
        { X: 813, Y: 173, name: "MILAN", color: "#75a4ff" },
        { X: 786, Y: 67, name: "ESSEN", color: "#75a4ff" },
        { X: 893, Y: 85, name: "ST. PETERSBURG", color: "#75a4ff" },

        { X: 25, Y: 322, name: "LOS ANGELES", color: "#ffe680" },
        { X: 161, Y: 386, name: "MEXICO CITY", color: "#ffe680" },
        { X: 271, Y: 348, name: "MIAMI", color: "#ffe680" },
        { X: 315, Y: 494, name: "BOGOTÁ", color: "#ffe680" },
        { X: 294, Y: 597, name: "LIMA", color: "#ffe680" },
        { X: 275, Y: 751, name: "SANTIAGO", color: "#ffe680" },
        { X: 389, Y: 754, name: "BUENOS AIRES", color: "#ffe680" },
        { X: 460, Y: 680, name: "SÃO PAULO", color: "#ffe680" },
        { X: 745, Y: 475, name: "LAGOS", color: "#ffe680" },
        { X: 807, Y: 525, name: "KINSHASA", color: "#ffe680" },
        { X: 858, Y: 713, name: "JOHANNESBURG", color: "#ffe680" },
        { X: 889, Y: 412, name: "KHARTOUM", color: "#ffe680" },

        { X: 882, Y: 325, name: "CAIRO", color: "black" },
        { X: 731, Y: 274, name: "ALGIERS", color: "black" },
        { X: 871, Y: 235, name: "ISTANBUL", color: "black" },
        { X: 975, Y: 168, name: "MOSCOW", color: "black" },
        { X: 1020, Y: 237, name: "TEHRAN", color: "black" },
        { X: 953, Y: 279, name: "BAGHDAD", color: "black" },
        { X: 971, Y: 381, name: "RIYADH", color: "black" },
        { X: 1072, Y: 327, name: "KARACHI", color: "black" },
        { X: 1152, Y: 264, name: "DELHI", color: "black" },
        { X: 1075, Y: 406, name: "MUMBAI", color: "black" },
        { X: 1149, Y: 451, name: "CHENNAI", color: "black" },
        { X: 1206, Y: 330, name: "KOLKATA", color: "black" },

        { X: 1268, Y: 407, name: "BANGKOK", color: "#ff8080" },
        { X: 1327, Y: 343, name: "KONG KONG", color: "#ff8080" },
        { X: 1328, Y: 249, name: "SHANGHAI", color: "#ff8080" },
        { X: 1347, Y: 173, name: "BEIJING", color: "#ff8080" },
        { X: 1448, Y: 198, name: "SEOUL", color: "#ff8080" },
        { X: 1544, Y: 266, name: "TOKYO", color: "#ff8080" },
        { X: 1523, Y: 361, name: "OSAKA", color: "#ff8080" },
        { X: 1428, Y: 399, name: "TAIPEI", color: "#ff8080" },
        { X: 1414, Y: 508, name: "MANILA", color: "#ff8080" },
        { X: 1321, Y: 480, name: "HO CHI MINH CITY", color: "#ff8080" },
        { X: 1254, Y: 567, name: "JAKARTA", color: "#ff8080" },
        { X: 1532, Y: 770, name: "SYDNEY", color: "#ff8080" }
    ]

    City { absX: modelData.X; absY: modelData.Y; name: modelData.name; cityColor: modelData.color }
 }
