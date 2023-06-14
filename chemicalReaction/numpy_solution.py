import numpy as np
import matplotlib.pyplot as plt
import os, shutil
from scipy.integrate import odeint

t = [0, 2.0000000000000013, 3.9999999999999587, 5.9999999999999165, 7.999999999999874, 9.999999999999831, 11.999999999999789, 13.999999999999746, 15.999999999999703, 18.000000000000014, 20.000000000000327, 22.00000000000064, 24.000000000000952, 26.000000000001265, 28.000000000001577, 30.00000000000189, 32.0000000000022, 34.000000000001805, 36.00000000000141, 38.00000000000101, 40.00000000000061, 42.00000000000021, 43.999999999999815, 45.99999999999942, 47.99999999999902, 49.99999999999862, 51.999999999998224, 53.999999999997826, 55.99999999999743, 57.99999999999703, 59.99999999999663, 61.999999999996234, 63.999999999995836, 65.99999999999686, 67.99999999999788, 69.9999999999989, 71.99999999999993, 74.00000000000095, 76.00000000000198, 78.000000000003, 80.00000000000402, 82.00000000000504, 84.00000000000607, 86.00000000000709, 88.00000000000811, 90.00000000000914, 92.00000000001016, 94.00000000001118, 96.00000000001221, 98.00000000001323, 100.00000000001425, 102.00000000001528, 104.0000000000163, 106.00000000001732, 108.00000000001835, 110.00000000001937, 112.00000000002039, 114.00000000002142, 116.00000000002244, 118.00000000002346, 120.00000000002449, 122.00000000002551, 124.00000000002653, 126.00000000002755, 128.00000000002856, 130.00000000002674, 132.00000000002493, 134.0000000000231, 136.0000000000213, 138.00000000001947, 140.00000000001765, 142.00000000001583, 144.000000000014, 146.0000000000122, 148.00000000001037, 150.00000000000855, 152.00000000000674, 154.00000000000492, 156.0000000000031, 158.00000000000128, 159.99999999999946, 161.99999999999764, 163.99999999999582, 165.999999999994, 167.99999999999218, 169.99999999999037, 171.99999999998855, 173.99999999998673, 175.9999999999849, 177.9999999999831, 179.99999999998127, 181.99999999997945, 183.99999999997763, 185.9999999999758, 187.999999999974, 189.99999999997218, 191.99999999997036, 193.99999999996854, 195.99999999996672, 197.9999999999649, 199.99999999996308, 201.99999999996126, 203.99999999995944, 205.99999999995762, 207.9999999999558, 209.99999999995399, 211.99999999995217, 213.99999999995035, 215.99999999994853, 217.9999999999467, 219.9999999999449, 221.99999999994307, 223.99999999994125, 225.99999999993943, 227.99999999993761, 229.9999999999358, 231.99999999993398, 233.99999999993216, 235.99999999993034, 237.99999999992852, 239.9999999999267, 241.99999999992488, 243.99999999992306, 245.99999999992124, 247.99999999991942, 249.9999999999176, 251.9999999999158, 253.99999999991397, 255.99999999991215, 257.99999999991036, 259.99999999990854, 261.9999999999067, 263.9999999999049, 265.9999999999031, 267.99999999990126, 269.99999999989944, 271.9999999998976, 273.9999999998958, 275.999999999894, 277.99999999989217, 279.99999999989035, 281.99999999988853, 283.9999999998867, 285.9999999998849, 287.9999999998831, 289.99999999988125, 291.99999999987944, 293.9999999998776, 295.9999999998758, 297.999999999874, 299.99999999987216, 301.99999999987034, 303.9999999998685, 305.9999999998667, 307.9999999998649, 309.99999999986306, 311.99999999986125, 313.9999999998594, 315.9999999998576, 317.9999999998558, 319.99999999985397, 321.99999999985215, 323.99999999985033, 325.9999999998485, 327.9999999998467, 329.9999999998449, 331.99999999984306, 333.99999999984124, 335.9999999998394, 337.9999999998376, 339.9999999998358, 341.99999999983396, 343.99999999983214, 345.9999999998303, 347.9999999998285, 349.9999999998267, 351.99999999982487, 353.99999999982305, 355.9999999998212, 357.9999999998194, 359.9999999998176, 361.99999999981577, 363.99999999981395, 365.99999999981213, 367.9999999998103, 369.9999999998085, 371.9999999998067, 373.99999999980486, 375.99999999980304, 377.9999999998012, 379.9999999997994, 381.9999999997976, 383.99999999979576, 385.99999999979394, 387.9999999997921, 389.9999999997903, 391.9999999997885, 393.99999999978667, 395.99999999978485, 397.99999999978303, 399.9999999997812, 401.9999999997794, 403.9999999997776, 405.99999999977575, 407.99999999977393, 409.9999999997721, 411.9999999997703, 413.9999999997685, 415.99999999976666, 417.99999999976484, 419.999999999763, 421.9999999997612, 423.9999999997594, 425.99999999975756, 427.99999999975574, 429.9999999997539, 431.9999999997521, 433.9999999997503, 435.99999999974847, 437.99999999974665, 439.99999999974483, 441.999999999743, 443.9999999997412, 445.9999999997394, 447.99999999973755, 449.99999999973573, 451.9999999997339, 453.9999999997321, 455.9999999997303, 457.99999999972846, 459.99999999972664, 461.9999999997248, 463.999999999723, 465.9999999997212, 467.99999999971936, 469.99999999971755, 471.9999999997157, 473.9999999997139, 475.9999999997121, 477.99999999971027, 479.99999999970845, 481.99999999970663, 483.9999999997048, 485.999999999703, 487.9999999997012, 489.99999999969936, 491.99999999969754, 493.9999999996957, 495.9999999996939, 497.9999999996921, 499.99999999969026, 501.99999999968844, 503.9999999996866, 505.9999999996848, 507.999999999683, 509.99999999968117, 511.99999999967935, 513.9999999996776, 515.9999999996758, 517.999999999674, 519.9999999996721, 521.9999999996703, 523.9999999996685, 525.9999999996667, 527.9999999996649, 529.999999999663, 531.9999999996612, 533.9999999996594, 535.9999999996576, 537.9999999996558, 539.9999999996539, 541.9999999996521, 543.9999999996503, 545.9999999996485, 547.9999999996467, 549.9999999996448, 551.999999999643, 553.9999999996412, 555.9999999996394, 557.9999999996376, 559.9999999996357, 561.9999999996339, 563.9999999996321, 565.9999999996303, 567.9999999996285, 569.9999999996267, 571.9999999996248, 573.999999999623, 575.9999999996212, 577.9999999996194, 579.9999999996176, 581.9999999996157, 583.9999999996139, 585.9999999996121, 587.9999999996103, 589.9999999996085, 591.9999999996066, 593.9999999996048, 595.999999999603, 597.9999999996012, 599.9999999995994, 601.9999999995975, 603.9999999995957, 605.9999999995939, 607.9999999995921, 609.9999999995903, 611.9999999995885, 613.9999999995866, 615.9999999995848, 617.999999999583, 619.9999999995812, 621.9999999995794, 623.9999999995775, 625.9999999995757, 627.9999999995739, 629.9999999995721, 631.9999999995703, 633.9999999995684, 635.9999999995666, 637.9999999995648, 639.999999999563, 641.9999999995612, 643.9999999995593, 645.9999999995575, 647.9999999995557, 649.9999999995539, 651.9999999995521, 653.9999999995503, 655.9999999995484, 657.9999999995466, 659.9999999995448, 661.999999999543, 663.9999999995412, 665.9999999995393, 667.9999999995375, 669.9999999995357, 671.9999999995339, 673.9999999995321, 675.9999999995302, 677.9999999995284, 679.9999999995266, 681.9999999995248, 683.999999999523, 685.9999999995212, 687.9999999995193, 689.9999999995175, 691.9999999995157, 693.9999999995139, 695.999999999512, 697.9999999995102, 699.9999999995084, 701.9999999995066, 703.9999999995048, 705.999999999503, 707.9999999995011, 709.9999999994993, 711.9999999994975, 713.9999999994957, 715.9999999994939, 717.999999999492, 719.9999999994902, 721.9999999994884, 723.9999999994866, 725.9999999994848, 727.999999999483, 729.9999999994811, 731.9999999994793, 733.9999999994775, 735.9999999994757, 737.9999999994739, 739.999999999472, 741.9999999994702, 743.9999999994684, 745.9999999994666, 747.9999999994648, 749.999999999463, 751.9999999994611, 753.9999999994593, 755.9999999994575, 757.9999999994557, 759.9999999994538, 761.999999999452, 763.9999999994502, 765.9999999994484, 767.9999999994466, 769.9999999994448, 771.9999999994429, 773.9999999994411, 775.9999999994393, 777.9999999994375, 779.9999999994357, 781.9999999994338, 783.999999999432, 785.9999999994302, 787.9999999994284, 789.9999999994266, 791.9999999994247, 793.9999999994229, 795.9999999994211, 797.9999999994193, 799.9999999994175, 801.9999999994156, 803.9999999994138, 805.999999999412, 807.9999999994102, 809.9999999994084, 811.9999999994066, 813.9999999994047, 815.9999999994029, 817.9999999994011, 819.9999999993993, 821.9999999993975, 823.9999999993956, 825.9999999993938, 827.999999999392, 829.9999999993902, 831.9999999993884, 833.9999999993865, 835.9999999993847, 837.9999999993829, 839.9999999993811, 841.9999999993793, 843.9999999993775, 845.9999999993756, 847.9999999993738, 849.999999999372, 851.9999999993702, 853.9999999993684, 855.9999999993665, 857.9999999993647, 859.9999999993629, 861.9999999993611, 863.9999999993593, 865.9999999993574, 867.9999999993556, 869.9999999993538, 871.999999999352, 873.9999999993502, 875.9999999993483, 877.9999999993465, 879.9999999993447, 881.9999999993429, 883.9999999993411, 885.9999999993393, 887.9999999993374, 889.9999999993356, 891.9999999993338, 893.999999999332, 895.9999999993302, 897.9999999993283, 899.9999999993265, 901.9999999993247, 903.9999999993229, 905.9999999993211, 907.9999999993192, 909.9999999993174, 911.9999999993156, 913.9999999993138, 915.999999999312, 917.9999999993101, 919.9999999993083, 921.9999999993065, 923.9999999993047, 925.9999999993029, 927.999999999301, 929.9999999992992, 931.9999999992974, 933.9999999992956, 935.9999999992938, 937.999999999292, 939.9999999992901, 941.9999999992883, 943.9999999992865, 945.9999999992847, 947.9999999992829, 949.999999999281, 951.9999999992792, 953.9999999992774, 955.9999999992756, 957.9999999992738, 959.999999999272, 961.9999999992701, 963.9999999992683, 965.9999999992665, 967.9999999992647, 969.9999999992629, 971.999999999261, 973.9999999992592, 975.9999999992574, 977.9999999992556, 979.9999999992538, 981.9999999992519, 983.9999999992501, 985.9999999992483, 987.9999999992465, 989.9999999992447, 991.9999999992428, 993.999999999241, 995.9999999992392, 997.9999999992374, 999.9999999992356, 1001.9999999992338, 1003.9999999992319, 1005.9999999992301, 1007.9999999992283, 1009.9999999992265, 1011.9999999992247, 1013.9999999992228, 1015.999999999221, 1017.9999999992192, 1019.9999999992174, 1021.9999999992156, 1023.9999999992137, 1025.999999999212, 1027.99999999921, 1029.9999999992083, 1031.9999999992065, 1033.9999999992046, 1035.9999999992028, 1037.999999999201, 1039.9999999991992, 1041.9999999991974, 1043.9999999991956, 1045.9999999991937, 1047.999999999192, 1049.99999999919, 1051.9999999991883, 1053.9999999991865, 1055.9999999991846, 1057.9999999991828, 1059.999999999181, 1061.9999999991792, 1063.9999999991774, 1065.9999999991755, 1067.9999999991737, 1069.999999999172, 1071.99999999917, 1073.9999999991683, 1075.9999999991664, 1077.9999999991646, 1079.9999999991628, 1081.999999999161, 1083.9999999991592, 1085.9999999991574, 1087.9999999991555, 1089.9999999991537, 1091.999999999152, 1093.99999999915, 1095.9999999991483, 1097.9999999991464, 1099.9999999991446, 1101.9999999991428, 1103.999999999141, 1105.9999999991392, 1107.9999999991373, 1109.9999999991355, 1111.9999999991337, 1113.999999999132, 1115.99999999913, 1117.9999999991282, 1119.9999999991264, 1121.9999999991246, 1123.9999999991228, 1125.999999999121, 1127.9999999991192, 1129.9999999991173, 1131.9999999991155, 1133.9999999991137, 1135.9999999991119, 1137.99999999911, 1139.9999999991082, 1141.9999999991064, 1143.9999999991046, 1145.9999999991028, 1147.999999999101, 1149.9999999990991, 1151.9999999990973, 1153.9999999990955, 1155.9999999990937, 1157.9999999990919, 1159.99999999909, 1161.9999999990882, 1163.9999999990864, 1165.9999999990846, 1167.9999999990828, 1169.999999999081, 1171.9999999990791, 1173.9999999990773, 1175.9999999990755, 1177.9999999990737, 1179.9999999990719, 1181.99999999907, 1183.9999999990682, 1185.9999999990664, 1187.9999999990646, 1189.9999999990628, 1191.999999999061, 1193.9999999990591, 1195.9999999990573, 1197.9999999990555, 1199.9999999990537, 1201.9999999990519, 1203.99999999905, 1205.9999999990482, 1207.9999999990464, 1209.9999999990446, 1211.9999999990428, 1213.999999999041, 1215.9999999990391, 1217.9999999990373, 1219.9999999990355, 1221.9999999990337, 1223.9999999990318, 1225.99999999903, 1227.9999999990282, 1229.9999999990264, 1231.9999999990246, 1233.9999999990227, 1235.999999999021, 1237.999999999019, 1239.9999999990173, 1241.9999999990155, 1243.9999999990137, 1245.9999999990118, 1247.99999999901, 1249.9999999990082, 1251.9999999990064, 1253.9999999990046, 1255.9999999990027, 1257.999999999001, 1259.999999998999, 1261.9999999989973, 1263.9999999989955, 1265.9999999989936, 1267.9999999989918, 1269.99999999899, 1271.9999999989882, 1273.9999999989864, 1275.9999999989845, 1277.9999999989827, 1279.999999998981, 1281.999999998979, 1283.9999999989773, 1285.9999999989755, 1287.9999999989736, 1289.9999999989718, 1291.99999999897, 1293.9999999989682, 1295.9999999989664, 1297.9999999989645, 1299.9999999989627, 1301.999999998961, 1303.999999998959, 1305.9999999989573, 1307.9999999989554, 1309.9999999989536, 1311.9999999989518, 1313.99999999895, 1315.9999999989482, 1317.9999999989464, 1319.9999999989445, 1321.9999999989427, 1323.999999998941, 1325.999999998939, 1327.9999999989373, 1329.9999999989354, 1331.9999999989336, 1333.9999999989318, 1335.99999999893, 1337.9999999989282, 1339.9999999989263, 1341.9999999989245, 1343.9999999989227, 1345.9999999989209, 1347.999999998919, 1349.9999999989172, 1351.9999999989154, 1353.9999999989136, 1355.9999999989118, 1357.99999999891, 1359.9999999989082, 1361.9999999989063, 1363.9999999989045, 1365.9999999989027, 1367.9999999989009, 1369.999999998899, 1371.9999999988972, 1373.9999999988954, 1375.9999999988936, 1377.9999999988918, 1379.99999999889, 1381.9999999988881, 1383.9999999988863, 1385.9999999988845, 1387.9999999988827, 1389.9999999988809, 1391.999999998879, 1393.9999999988772, 1395.9999999988754, 1397.9999999988736, 1399.9999999988718, 1401.99999999887, 1403.9999999988681, 1405.9999999988663, 1407.9999999988645, 1409.9999999988627, 1411.9999999988609, 1413.999999998859, 1415.9999999988572, 1417.9999999988554, 1419.9999999988536, 1421.9999999988518, 1423.99999999885, 1425.9999999988481, 1427.9999999988463, 1429.9999999988445, 1431.9999999988427, 1433.9999999988408, 1435.999999998839, 1437.9999999988372, 1439.9999999988354, 1441.9999999988336, 1443.9999999988318, 1445.99999999883, 1447.9999999988281, 1449.9999999988263, 1451.9999999988245, 1453.9999999988227, 1455.9999999988208, 1457.999999998819, 1459.9999999988172, 1461.9999999988154, 1463.9999999988136, 1465.9999999988117, 1467.99999999881, 1469.999999998808, 1471.9999999988063, 1473.9999999988045, 1475.9999999988027, 1477.9999999988008, 1479.999999998799, 1481.9999999987972, 1483.9999999987954, 1485.9999999987936, 1487.9999999987917, 1489.99999999879, 1491.999999998788, 1493.9999999987863, 1495.9999999987845, 1497.9999999987826, 1499.9999999987808, 1501.999999998779, 1503.9999999987772, 1505.9999999987754, 1507.9999999987735, 1509.9999999987717, 1511.99999999877, 1513.999999998768, 1515.9999999987663, 1517.9999999987645, 1519.9999999987626, 1521.9999999987608, 1523.999999998759, 1525.9999999987572, 1527.9999999987554, 1529.9999999987535, 1531.9999999987517, 1533.99999999875, 1535.999999998748, 1537.9999999987463, 1539.9999999987444, 1541.9999999987426, 1543.9999999987408, 1545.999999998739, 1547.9999999987372, 1549.9999999987353, 1551.9999999987335, 1553.9999999987317, 1555.99999999873, 1557.999999998728, 1559.9999999987263, 1561.9999999987244, 1563.9999999987226, 1565.9999999987208, 1567.999999998719, 1569.9999999987172, 1571.9999999987153, 1573.9999999987135, 1575.9999999987117, 1577.9999999987099, 1579.999999998708, 1581.9999999987062, 1583.9999999987044, 1585.9999999987026, 1587.9999999987008, 1589.999999998699, 1591.9999999986971, 1593.9999999986953, 1595.9999999986935, 1597.9999999986917, 1599.9999999986899, 1601.999999998688, 1603.9999999986862, 1605.9999999986844, 1607.9999999986826, 1609.9999999986808, 1611.999999998679, 1613.9999999986771, 1615.9999999986753, 1617.9999999986735, 1619.9999999986717, 1621.9999999986699, 1623.999999998668, 1625.9999999986662, 1627.9999999986644, 1629.9999999986626, 1631.9999999986608, 1633.999999998659, 1635.9999999986571, 1637.9999999986553, 1639.9999999986535, 1641.9999999986517, 1643.9999999986499, 1645.999999998648, 1647.9999999986462, 1649.9999999986444, 1651.9999999986426, 1653.9999999986408, 1655.999999998639, 1657.9999999986371, 1659.9999999986353, 1661.9999999986335, 1663.9999999986317, 1665.9999999986298, 1667.999999998628, 1669.9999999986262, 1671.9999999986244, 1673.9999999986226, 1675.9999999986208, 1677.999999998619, 1679.999999998617, 1681.9999999986153, 1683.9999999986135, 1685.9999999986117, 1687.9999999986098, 1689.999999998608, 1691.9999999986062, 1693.9999999986044, 1695.9999999986026, 1697.9999999986007, 1699.999999998599, 1701.999999998597, 1703.9999999985953, 1705.9999999985935, 1707.9999999985916, 1709.9999999985898, 1711.999999998588, 1713.9999999985862, 1715.9999999985844, 1717.9999999985826, 1719.9999999985807, 1721.999999998579, 1723.999999998577, 1725.9999999985753, 1727.9999999985735, 1729.9999999985716, 1731.9999999985698, 1733.999999998568, 1735.9999999985662, 1737.9999999985644, 1739.9999999985625, 1741.9999999985607, 1743.999999998559, 1745.999999998557, 1747.9999999985553, 1749.9999999985534, 1751.9999999985516, 1753.9999999985498, 1755.999999998548, 1757.9999999985462, 1759.9999999985444, 1761.9999999985425, 1763.9999999985407, 1765.999999998539, 1767.999999998537, 1769.9999999985353, 1771.9999999985334, 1773.9999999985316, 1775.9999999985298, 1777.999999998528, 1779.9999999985262, 1781.9999999985243, 1783.9999999985225, 1785.9999999985207, 1787.999999998519, 1789.999999998517, 1791.9999999985152, 1793.9999999985134, 1795.9999999985116, 1797.9999999985098, 1799.999999998508, 1801.9999999985062, 1803.9999999985043, 1805.9999999985025, 1807.9999999985007, 1809.9999999984989, 1811.999999998497, 1813.9999999984952, 1815.9999999984934, 1817.9999999984916, 1819.9999999984898, 1821.999999998488, 1823.9999999984861, 1825.9999999984843, 1827.9999999984825, 1829.9999999984807, 1831.9999999984789, 1833.999999998477, 1835.9999999984752, 1837.9999999984734, 1839.9999999984716, 1841.9999999984698, 1843.999999998468, 1845.9999999984661, 1847.9999999984643, 1849.9999999984625, 1851.9999999984607, 1853.9999999984589, 1855.999999998457, 1857.9999999984552, 1859.9999999984534, 1861.9999999984516, 1863.9999999984498, 1865.999999998448, 1867.9999999984461, 1869.9999999984443, 1871.9999999984425, 1873.9999999984407, 1875.9999999984389, 1877.999999998437, 1879.9999999984352, 1881.9999999984334, 1883.9999999984316, 1885.9999999984298, 1887.999999998428, 1889.9999999984261, 1891.9999999984243, 1893.9999999984225, 1895.9999999984207, 1897.9999999984188, 1899.999999998417, 1901.9999999984152, 1903.9999999984134, 1905.9999999984116, 1907.9999999984097, 1909.999999998408, 1911.999999998406, 1913.9999999984043, 1915.9999999984025, 1917.9999999984007, 1919.9999999983988, 1921.999999998397, 1923.9999999983952, 1925.9999999983934, 1927.9999999983916, 1929.9999999983897, 1931.999999998388, 1933.999999998386, 1935.9999999983843, 1937.9999999983825, 1939.9999999983806, 1941.9999999983788, 1943.999999998377, 1945.9999999983752, 1947.9999999983734, 1949.9999999983715, 1951.9999999983697, 1953.999999998368, 1955.999999998366, 1957.9999999983643, 1959.9999999983625, 1961.9999999983606, 1963.9999999983588, 1965.999999998357, 1967.9999999983552, 1969.9999999983534, 1971.9999999983515, 1973.9999999983497, 1975.999999998348, 1977.999999998346, 1979.9999999983443, 1981.9999999983424, 1983.9999999983406, 1985.9999999983388, 1987.999999998337, 1989.9999999983352, 1991.9999999983334, 1993.9999999983315, 1995.9999999983297, 1997.999999998328, 1999.999999998326, 2001.9999999983243, 2003.9999999983224, 2005.9999999983206, 2007.9999999983188, 2009.999999998317, 2011.9999999983152, 2013.9999999983133]
maxChainLength = 15
concentrations = []
for i in range(maxChainLength):
    concentrations.append(0)
concentrations[0] = 1
r = 0.01 # L/(mol s)

def DGL(concentrations,t):
    concentrationChange = []
    for i in range(maxChainLength):
        concentrationChange.append(0)
    r = 0.01 # L/(mol s)
    for i in range(2,len(concentrations)):
        concRate =  r * concentrations[0] * concentrations[i-2] # mol/(L s)

        # increase polymer concentration
        concentrationChange[i-1] +=  concRate

        # decrease monomer concentration
        concentrationChange[0] -= concRate

        # decrease concentration of the smaller polymer
        concentrationChange[i-2] -= concRate
    
    return concentrationChange

# chainLength = np.linspace(0,15)
y = odeint(DGL,concentrations, t)
# liste von listemit 1008 einträgen für jeden Zeitpunkt  dann 15 einträge für jede Kettenlänge
currentWorkingDir = os.path.dirname(__file__)
picDirNp = os.path.join(currentWorkingDir, 'picNp')

if os.path.isdir(picDirNp):
    shutil.rmtree(picDirNp)
    os.mkdir(picDirNp)
imageCounter = 0
for i in range(len(y)):
    for j in range(len(y[i])):
        plt.plot(list(range(15)),y[i])
        plt.xlabel('chainlength')
        plt.ylabel('concentration')
        plt.savefig(os.path.join(picDirNp,f'concentrationProfile-{imageCounter:04d}.png'))
        plt.close()
    imageCounter += 1

