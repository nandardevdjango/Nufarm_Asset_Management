-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.2.11-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win32
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping data for table na_m_s.n_a_goods_receive: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_receive` DISABLE KEYS */;
REPLACE INTO `n_a_goods_receive` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `DateReceived`, `TotalPurchase`, `TotalReceived`, `Descriptions`, `DescBySystem`, `REFNO`, `FK_Suplier`, `fk_goods`, `FK_P_R_By`, `FK_ReceivedBy`) VALUES
	(1, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, '2016-03-04 00:00:00.000000', 8, 8, 'Pembelian HP J5 tahap pertama untuk IT dan marketing, dan IConcept dan kepentingan FMS lainnya', '(SAMSUNG, Type : J5, SN : 357005072234246-357004072234249, SAMSUNG, Type : J5, SN : 357004071145081-357005071145088, SAMSUNG, Type : J5, SN : 357005071145054-357004071145057, SAMSUNG, Type : J5, SN : 357004071145024-357005071145021, SAMSUNG, Type : J5, SN : 357004071144027-357005071144024, SAMSUNG, Type : J5, SN : 357004072234249-357005072234246, SAMSUNG, Type : J5, SN : 357004071145115-357004071145115, SAMSUNG, Type : J5, SN : ICONCEPT)', '15/16-000128-01', 'ERA004IDR', 3, 8, 9),
	(2, '2018-08-28 00:00:00.000000', 'nandar', NULL, NULL, '2015-07-30 00:00:00.000000', 6, 6, '', '(DELL, Type : LATITUDE E5440, SN : 7SOGWZ1/0001402, DELL, Type : LATITUDE E5440, SN : 3L4Z062/0001403, DELL, Type : LATITUDE E5440, SN :  3S30l32/0001404, DELL, Type : LATITUDE E5440, SN : HHS2F12/0001405, DELL, Type : LATITUDE E5440, SN : 1V1GWZ1/0001406, DELL, Type : LATITUDE E5440, SN : 3K65P12/0001407)', '14/15-000141-01', 'PAR002USD', 2, 8, 9);
/*!40000 ALTER TABLE `n_a_goods_receive` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_receive_detail: ~14 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_receive_detail` DISABLE KEYS */;
REPLACE INTO `n_a_goods_receive_detail` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `BrandName`, `PricePerUnit`, `TypeApp`, `Warranty`, `EndOfWarranty`, `SerialNumber`, `FK_App`) VALUES
	(1, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', '357005072234246-357004072234249', 1),
	(2, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', '357004071145081-357005071145088', 1),
	(3, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', '357005071145054-357004071145057', 1),
	(4, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', '357004071145024-357005071145021', 1),
	(5, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', '357004071144027-357005071144024', 1),
	(6, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', '357004072234249-357005072234246', 1),
	(7, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', '357004071145115-357004071145115', 1),
	(8, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', 'ICONCEPT', 1),
	(9, '2018-08-28 00:00:00.000000', 'nandar', NULL, NULL, 'DELL', 15001875.0000, 'LATITUDE E5440', 5.00, '2020-07-28 00:00:00.000000', '7SOGWZ1/0001402', 2),
	(10, '2018-08-28 00:00:00.000000', 'nandar', NULL, NULL, 'DELL', 15001875.0000, 'LATITUDE E5440', 5.00, '2020-07-28 00:00:00.000000', '3L4Z062/0001403', 2),
	(11, '2018-08-28 00:00:00.000000', 'nandar', NULL, NULL, 'DELL', 15001875.0000, 'LATITUDE E5440', 5.00, '2020-07-28 00:00:00.000000', ' 3S30l32/0001404', 2),
	(12, '2018-08-28 00:00:00.000000', 'nandar', NULL, NULL, 'DELL', 15001875.0000, 'LATITUDE E5440', 5.00, '2020-07-28 00:00:00.000000', 'HHS2F12/0001405', 2),
	(13, '2018-08-28 00:00:00.000000', 'nandar', NULL, NULL, 'DELL', 15001875.0000, 'LATITUDE E5440', 5.00, '2020-07-28 00:00:00.000000', '1V1GWZ1/0001406', 2),
	(14, '2018-08-28 00:00:00.000000', 'nandar', NULL, NULL, 'DELL', 15001875.0000, 'LATITUDE E5440', 5.00, '2020-07-28 00:00:00.000000', '3K65P12/0001407', 2);
/*!40000 ALTER TABLE `n_a_goods_receive_detail` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_receive_other: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_receive_other` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_receive_other` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_stock: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_stock` DISABLE KEYS */;
REPLACE INTO `n_a_stock` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `T_Goods_Spare`, `TotalQty`, `TIsUsed`, `TIsNew`, `TIsRenew`, `TIsBroken`, `TGoods_Return`, `TGoods_Received`, `TDisposal`, `TIsLost`, `TMaintenance`, `FK_Goods`) VALUES
	(1, '2018-08-21 17:04:53.000000', 'rimba88', NULL, NULL, 0, NULL, 0, 8, 0, NULL, 0, 8, NULL, NULL, 0, 00000000003),
	(2, '2018-08-28 23:21:55.000000', 'nandar', NULL, NULL, 0, NULL, 0, 6, 0, NULL, 0, 6, NULL, NULL, 0, 00000000002);
/*!40000 ALTER TABLE `n_a_stock` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
