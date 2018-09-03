-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.2.11-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win32
-- HeidiSQL Version:             9.5.0.5261
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping data for table na_m_s.employee: ~9 rows (approximately)
DELETE FROM `employee`;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `TypeApp`, `InActive`, `Descriptions`, `NIK`, `Employee_Name`, `JobType`, `Gender`, `Status`, `TelpHP`, `Territory`) VALUES
	(1, '2018-08-20 16:45:37.409544', 'rimba88', NULL, NULL, 'P', 0, 'Nufarm IT Manager', '2011131', 'Tandry Adrian Hartanto', 'IT Bussines Developmen Manager', 'M', 'M', '0818925270', 'JAKARTA'),
	(2, '2018-08-20 16:49:27.557851', 'rimba88', '2018-08-20 17:28:46.990922', 'rimba88', 'P', 0, 'Pak suroto asalnya Office Boy menggantikan Ridho', 'C020', 'Suroto', 'RECEPTIONIST', 'M', 'M', '087808451709', 'JAKARTA'),
	(3, '2018-08-20 16:56:03.069993', 'rimba88', NULL, NULL, 'P', 0, 'Luther Juan pengganti Muhammad Syahwil', '2017457', 'Luther Juan Sanda', 'Purchasing Executif', 'M', 'S', '08992474947', 'JAKARTA'),
	(4, '2018-08-20 17:09:48.969665', 'rimba88', '2018-08-20 17:28:41.245768', 'rimba88', 'P', 0, 'pak iman naik jabatan sekarang jafi GA Supervisor menggantikan Tri Wahyudi', '20050201', 'Iman Utomo', 'GA Supervisor', 'M', 'M', '085693330550', 'JAKARTA'),
	(5, '2018-08-20 17:18:33.601710', 'rimba88', NULL, NULL, 'P', 0, 'Wahyu bima karyawan menggantikan posisi surya sofianto', '2016367', 'R. Wahyoe Bima D.K', 'Purchasing Executif', 'M', 'M', '082123326963', 'JAKARTA'),
	(6, '2018-08-20 17:24:45.145917', 'rimba88', '2018-08-20 17:28:33.328118', 'rimba88', 'P', 0, 'SENIOR IT NUFARM', '990642', 'Indradjaja Tjandra Poernama', 'IT SUPERVISOR', 'M', 'M', '08129239707', 'JAKARTA'),
	(7, '2018-08-20 17:27:55.332142', 'rimba88', '2018-08-20 17:28:29.206281', 'rimba88', 'P', 0, 'Nandar memulai karir di nufarm sebagai programmer di bagian sales retailer dan distributor', '201311', 'Kusnandar', 'IT PROGRAMMER', 'M', 'M', '08118855107', 'JAKARTA'),
	(8, '2018-08-20 18:29:16.104895', 'rimba88', NULL, NULL, 'P', 0, 'Sudah keluar di ganti sama Luther Juan', 'F212014512', 'Junaid syahwil', 'PURCHASING EXECUTIVE', 'M', 'M', '083876640037', 'JAKARTA'),
	(9, '2018-08-20 18:48:14.723854', 'rimba88', NULL, NULL, 'P', 0, 'Sidik sebelumnya menjabat sebagai IT technical support, mula tahun 2016 berpindah ke divisi marketing sebagai marketing digital', '20040903', 'SIDIK HARTADI', 'MARKETING DIGITAL', 'M', 'M', '08118855106', 'JAKARTA');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;

-- Dumping data for table na_m_s.logevent: ~14 rows (approximately)
DELETE FROM `logevent`;
/*!40000 ALTER TABLE `logevent` DISABLE KEYS */;
/*!40000 ALTER TABLE `logevent` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_acc_fa: ~0 rows (approximately)
DELETE FROM `n_a_acc_fa`;
/*!40000 ALTER TABLE `n_a_acc_fa` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_acc_fa` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_appparams: ~0 rows (approximately)
DELETE FROM `n_a_appparams`;
/*!40000 ALTER TABLE `n_a_appparams` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_appparams` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_disposal: ~0 rows (approximately)
DELETE FROM `n_a_disposal`;
/*!40000 ALTER TABLE `n_a_disposal` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_disposal` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_ga_maintenance: ~0 rows (approximately)
DELETE FROM `n_a_ga_maintenance`;
/*!40000 ALTER TABLE `n_a_ga_maintenance` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_maintenance` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_ga_outwards: ~0 rows (approximately)
DELETE FROM `n_a_ga_outwards`;
/*!40000 ALTER TABLE `n_a_ga_outwards` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_outwards` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_ga_receive: ~0 rows (approximately)
DELETE FROM `n_a_ga_receive`;
/*!40000 ALTER TABLE `n_a_ga_receive` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_receive` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_ga_return: ~0 rows (approximately)
DELETE FROM `n_a_ga_return`;
/*!40000 ALTER TABLE `n_a_ga_return` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_return` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_ga_vn_history: ~0 rows (approximately)
DELETE FROM `n_a_ga_vn_history`;
/*!40000 ALTER TABLE `n_a_ga_vn_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_vn_history` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods: ~26 rows (approximately)
DELETE FROM `n_a_goods`;
/*!40000 ALTER TABLE `n_a_goods` DISABLE KEYS */;
INSERT INTO `n_a_goods` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `InActive`, `Descriptions`, `ItemCode`, `GoodsName`, `BrandName`, `PricePerUnit`, `DepreciationMethod`, `Unit`, `EconomicLife`, `Placement`, `typeapp`) VALUES
	(1, '2018-08-15 00:00:00.000000', 'rimba88', NULL, NULL, 0, 'Price tidak di includekan di sini karena price di entry dilain form, kecuali untuk barang-barang lain,(others)', 'IT-001', 'COMPUTER DESKTOP', 'DELL', 0.0000, 'SL', 'Unit', 5.00, 'Gudang IT', 'IT'),
	(2, '2018-08-16 00:00:00.000000', 'rimba88', '2018-08-16 16:14:13.461843', 'rimba88', 0, 'Price tidak di isi di bagian form ini , tapi di bagian penerimaan barang baru', 'IT-002', 'LAPTOP', 'DELL', 0.0000, 'SL', 'Unit', 5.00, 'Gudang IT', 'IT'),
	(3, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, 'Price tidak di input di form ini', 'IT-003', 'HANDPHONE', 'SAMSUNG', 0.0000, 'SL', 'Pcs', 5.00, 'Gudang IT', 'IT'),
	(4, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, 'Harga tidak di cantumkan di sini karena ini master barang global', 'IT-004', 'LCD PROJECTOR', 'NEC', 0.0000, 'SL', 'Pcs', 3.00, 'Gudang IT', 'IT'),
	(5, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, 'Price tidak di input di form ini karena ini form master general/pengelompokan barang', 'IT-005', 'CAMERA', 'CANON', 0.0000, 'SL', 'Pcs', 3.00, 'Gudang IT', 'IT'),
	(6, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, '', 'IT-006', 'HANDYCAM', 'SONY', 0.0000, 'SL', 'Pcs', 5.00, 'Gudang IT', 'IT'),
	(7, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, 'Price tidak di input di sini', 'IT-007', 'PRINTER', 'HEWLET PACKARD', 0.0000, 'SL', 'Pcs', 5.00, 'Gudang IT', 'IT'),
	(9, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, 'Price tidak di input di sini', 'IT-009', 'SCANNER', 'CANNON', 0.0000, 'SL', 'Pcs', 5.00, 'Gudang IT', 'IT'),
	(10, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, '', 'IT-008', 'EKSTERNAL HARDDISK', 'SEAGATE', 0.0000, 'SL', 'Pcs', 3.00, 'Gudang IT', 'IT'),
	(11, '2018-08-16 00:00:00.000000', 'rimba88', '2018-08-16 17:40:08.987357', 'rimba88', 0, '', 'IT-010', 'SERVER', 'DELL', 0.0000, 'SYD', 'Unit', 5.00, 'Gudang IT', 'IT'),
	(12, '2018-08-16 00:00:00.000000', 'rimba88', '2018-08-16 17:29:10.200725', 'rimba88', 0, '', 'IT-011', 'UPS', 'ICA', 0.0000, 'DDB', 'Unit', 5.00, 'Gudang IT', 'IT'),
	(13, '2018-08-16 00:00:00.000000', 'rimba88', '2018-08-16 17:28:41.482523', 'rimba88', 0, '', 'IT-012', 'ROUTER', 'CISCO', 0.0000, 'SH', 'Unit', 5.00, 'Gudang IT', 'IT'),
	(14, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, '', 'IT-013', 'SWITCH/HUB', 'HEWLET PACKARD', 0.0000, 'SL', 'Unit', 5.00, 'Gudang IT', 'IT'),
	(15, '2018-08-16 00:00:00.000000', 'rimba88', '2018-08-16 17:43:49.325351', 'rimba88', 0, 'Merek bukan cuma satu, tapi sebagai global saja', 'GA-001', 'MOTOR', 'KAWASAKI', 0.0000, 'SL', 'Unit', 5.00, 'Gudang IT', 'GA'),
	(16, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, 'Merek bukan cuma Toyota, tapi diambil sebagai global saja', 'GA-002', 'MOBIL', 'TOYOTA', 0.0000, 'SL', 'Unit', 5.00, 'Gudang IT', 'IT'),
	(18, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, 'Untuk HP yang mahal di pegang sama GA', 'GA-003', 'HP HIGH-END', 'SAMSUNG', 0.0000, 'SL', 'Pcs', 5.00, 'Gudang IT', 'IT'),
	(19, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, '', 'GA-004', 'TV', 'SONY', 0.0000, 'SL', 'Unit', 5.00, 'Gudang 2', 'GA'),
	(20, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, 'Brand di isi ke other karena tidak ada brand standar', 'IT-014', 'SOUND SYSTEM', 'Other', 0.0000, 'SL', 'Unit', 5.00, 'Gudang IT', 'IT'),
	(21, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, '', 'IT-015', 'STABILIZER', 'ICA', 0.0000, 'SL', 'Unit', 5.00, 'Gudang IT', 'IT'),
	(22, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, 'Brand untuk kulkas tidak global', 'GA-005', 'COOLCASE', 'SANYO', 0.0000, 'SL', 'Unit', 5.00, 'Gudang 2', 'IT'),
	(23, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, '', 'GA-006', 'DISPENSER', 'Other', 0.0000, 'SL', 'Unit', 5.00, 'Gudang 2', 'IT'),
	(24, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, '', 'GA-007', 'COPYING MACHINE', 'KYOCERA', 0.0000, 'SL', 'Unit', 5.00, 'Gudang 2', 'IT'),
	(25, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, '', 'GA-008', 'PAPER SHREDDER', 'Other', 0.0000, 'SL', 'Unit', 5.00, 'Gudang IT', 'IT'),
	(26, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, '', 'GA-009', 'PABX', 'Other', 0.0000, 'SL', 'Unit', 5.00, 'Gudang IT', 'IT'),
	(27, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, '', 'GA-010', 'TELP', 'NEC', 0.0000, 'SL', 'Unit', 5.00, 'Gudang IT', 'IT'),
	(28, '2018-08-16 00:00:00.000000', 'rimba88', NULL, NULL, 0, '', 'IT-016', 'FAX', 'CANON', 0.0000, 'SL', 'Unit', 5.00, 'Gudang IT', 'IT');
/*!40000 ALTER TABLE `n_a_goods` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_history: ~0 rows (approximately)
DELETE FROM `n_a_goods_history`;
/*!40000 ALTER TABLE `n_a_goods_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_history` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_lending: ~0 rows (approximately)
DELETE FROM `n_a_goods_lending`;
/*!40000 ALTER TABLE `n_a_goods_lending` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_lending` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_lost: ~0 rows (approximately)
DELETE FROM `n_a_goods_lost`;
/*!40000 ALTER TABLE `n_a_goods_lost` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_lost` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_outwards: ~0 rows (approximately)
DELETE FROM `n_a_goods_outwards`;
/*!40000 ALTER TABLE `n_a_goods_outwards` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_outwards` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_receive: ~0 rows (approximately)
DELETE FROM `n_a_goods_receive`;
/*!40000 ALTER TABLE `n_a_goods_receive` DISABLE KEYS */;
INSERT INTO `n_a_goods_receive` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `DateReceived`, `TotalPurchase`, `TotalReceived`, `Descriptions`, `DescBySystem`, `REFNO`, `FK_Supplier`, `fk_goods`, `FK_P_R_By`, `FK_ReceivedBy`) VALUES
	(1, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, '2016-03-04 00:00:00.000000', 8, 8, 'Pembelian HP J5 tahap pertama untuk IT dan marketing, dan IConcept dan kepentingan FMS lainnya', '(SAMSUNG, Type : J5, SN : 357005072234246-357004072234249, SAMSUNG, Type : J5, SN : 357004071145081-357005071145088, SAMSUNG, Type : J5, SN : 357005071145054-357004071145057, SAMSUNG, Type : J5, SN : 357004071145024-357005071145021, SAMSUNG, Type : J5, SN : 357004071144027-357005071144024, SAMSUNG, Type : J5, SN : 357004072234249-357005072234246, SAMSUNG, Type : J5, SN : 357004071145115-357004071145115, SAMSUNG, Type : J5, SN : ICONCEPT)', '15/16-000128-01', 'ERA004IDR', 3, 8, 9);
/*!40000 ALTER TABLE `n_a_goods_receive` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_receive_detail: ~0 rows (approximately)
DELETE FROM `n_a_goods_receive_detail`;
/*!40000 ALTER TABLE `n_a_goods_receive_detail` DISABLE KEYS */;
INSERT INTO `n_a_goods_receive_detail` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `BrandName`, `PricePerUnit`, `TypeApp`, `Warranty`, `EndOfWarranty`, `SerialNumber`, `FK_App`) VALUES
	(1, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', '357005072234246-357004072234249', 1),
	(2, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', '357004071145081-357005071145088', 1),
	(3, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', '357005071145054-357004071145057', 1),
	(4, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', '357004071145024-357005071145021', 1),
	(5, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', '357004071144027-357005071144024', 1),
	(6, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', '357004072234249-357005072234246', 1),
	(7, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', '357004071145115-357004071145115', 1),
	(8, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 2400000.0000, 'J5', 1.00, '2017-03-03 00:00:00.000000', 'ICONCEPT', 1);
/*!40000 ALTER TABLE `n_a_goods_receive_detail` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_receive_other: ~0 rows (approximately)
DELETE FROM `n_a_goods_receive_other`;
/*!40000 ALTER TABLE `n_a_goods_receive_other` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_receive_other` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_return: ~0 rows (approximately)
DELETE FROM `n_a_goods_return`;
/*!40000 ALTER TABLE `n_a_goods_return` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_return` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_maintenance: ~0 rows (approximately)
DELETE FROM `n_a_maintenance`;
/*!40000 ALTER TABLE `n_a_maintenance` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_maintenance` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_privilege: ~1 rows (approximately)
DELETE FROM `n_a_privilege`;
/*!40000 ALTER TABLE `n_a_privilege` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_privilege` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_privilege_form: ~6 rows (approximately)
DELETE FROM `n_a_privilege_form`;
/*!40000 ALTER TABLE `n_a_privilege_form` DISABLE KEYS */;
INSERT INTO `n_a_privilege_form` (`IDApp`, `Form_id`, `Form_name`, `Form_name_ori`) VALUES
	(1, '0001M', 'Supplier Form', 'n_a_supplier'),
	(2, '0002M', 'Employee Form', 'employee'),
	(3, '0003M', 'Goods Form', 'goods'),
	(6, '0001T', 'Goods Receive', 'n_a_goods_receive'),
	(7, '0004M', 'User Privilege', 'n_a_privilege'),
	(8, '0001O', 'Fix Asset Form', 'n_a_acc_fa');
/*!40000 ALTER TABLE `n_a_privilege_form` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_privilege_groups: ~0 rows (approximately)
DELETE FROM `n_a_privilege_groups`;
/*!40000 ALTER TABLE `n_a_privilege_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_privilege_groups` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_privilege_user_permissions: ~0 rows (approximately)
DELETE FROM `n_a_privilege_user_permissions`;
/*!40000 ALTER TABLE `n_a_privilege_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_privilege_user_permissions` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_stock: ~0 rows (approximately)
DELETE FROM `n_a_stock`;
/*!40000 ALTER TABLE `n_a_stock` DISABLE KEYS */;
INSERT INTO `n_a_stock` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `T_Goods_Spare`, `TotalQty`, `TIsUsed`, `TIsNew`, `TIsRenew`, `TIsBroken`, `TGoods_Return`, `TGoods_Received`, `TDisposal`, `TIsLost`, `TMaintenance`, `FK_Goods`) VALUES
	(1, '2018-08-21 17:04:53.000000', 'rimba88', NULL, NULL, 0, NULL, 0, 8, 0, NULL, 0, 8, NULL, NULL, 0, 00000000003);
/*!40000 ALTER TABLE `n_a_stock` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_supplier: ~7 rows (approximately)
DELETE FROM `n_a_supplier`;
/*!40000 ALTER TABLE `n_a_supplier` DISABLE KEYS */;
INSERT INTO `n_a_supplier` (`CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `InActive`, `SupplierCode`, `SupplierName`, `Address`, `Telp`, `HP`, `ContactPerson`) VALUES
	('2018-08-20 18:53:37.355965', 'rimba88', NULL, NULL, 0, 'ALD002IDR', 'ALDI JAYA', 'Mangga Dua Mall Lt. IV/A-106 jakarta 10730', '0216018430', '08888099312', 'Bambang'),
	('2018-08-15 17:47:02.807019', 'rimba88', '2018-08-15 17:47:17.653669', 'rimba88', 1, 'AST002IDR', 'PT. ASTRA HONDA MOTOR', 'Jl. Laksda Yos Sudarso – Sunter I Jakarta 14350, Indonesia Tel. 0811-9-500-989', '021-7252000', '021-7252000', 'ASTRA'),
	('2018-08-15 17:38:21.108955', 'rimba88', NULL, NULL, 0, 'AST007IDR', 'PT. ASTRA INTERNATIONAL TBK', 'Jl. Pangeran Jayakarta no 28', '021-65906060', '021-6522555', 'Eko'),
	('2018-08-15 17:00:31.272246', 'rimba88', NULL, NULL, 0, 'CHA001IDR', 'CV CHA-CHA KARYA', 'JLn Sultan Agung Prokyek Pasar Rumput', '021-8033870', '081288725559', 'Rudi'),
	('2018-08-15 17:08:39.503456', 'rimba88', NULL, NULL, 0, 'ERA004IDR', 'PT. ERAPOINT GLOBALINDO', 'Jl. KH. Hasyim Azhari No.125 Komp. Niaga Roxy Mas Blok D4/21-22 JakartaPusat 10150', '021-6322555', '082111188729', 'Debby Cintya Dewi'),
	('2018-08-15 16:50:03.851840', 'rimba88', '2018-08-15 17:09:32.926966', 'rimba88', 1, 'MUL016IDR', 'CV MULTI SKINDO UTAMA', 'Jln Pangeran Jayakarta No .77 /GATEP, (NO.HP Customer belum di input di accpac)', '021-659030', '0216491264', 'Himawan Setiadi'),
	('2018-08-15 17:21:44.850050', 'rimba88', NULL, NULL, 0, 'PAR002USD', 'PT PARANTA ANUGERAH PRIMA', 'Wisma CORMIC Delta Building Blok A 4-7 l. Suryopranoto No. 1-9 Jakarta - 10160 Indonesia (No HP belum ada di isi sementara pakai no telp)', '021-3501188', '021-3501555', 'Fermin Setiawan');
/*!40000 ALTER TABLE `n_a_supplier` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_sys_privilege: ~16 rows (approximately)
DELETE FROM `n_a_sys_privilege`;
/*!40000 ALTER TABLE `n_a_sys_privilege` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_sys_privilege` ENABLE KEYS */;

-- Dumping data for table na_m_s.social_auth_association: ~0 rows (approximately)
DELETE FROM `social_auth_association`;
/*!40000 ALTER TABLE `social_auth_association` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_association` ENABLE KEYS */;

-- Dumping data for table na_m_s.social_auth_code: ~0 rows (approximately)
DELETE FROM `social_auth_code`;
/*!40000 ALTER TABLE `social_auth_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_code` ENABLE KEYS */;

-- Dumping data for table na_m_s.social_auth_nonce: ~0 rows (approximately)
DELETE FROM `social_auth_nonce`;
/*!40000 ALTER TABLE `social_auth_nonce` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_nonce` ENABLE KEYS */;

-- Dumping data for table na_m_s.social_auth_partial: ~0 rows (approximately)
DELETE FROM `social_auth_partial`;
/*!40000 ALTER TABLE `social_auth_partial` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_partial` ENABLE KEYS */;

-- Dumping data for table na_m_s.social_auth_usersocialauth: ~0 rows (approximately)
DELETE FROM `social_auth_usersocialauth`;
/*!40000 ALTER TABLE `social_auth_usersocialauth` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_usersocialauth` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
