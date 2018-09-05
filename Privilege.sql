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

-- Dumping data for table na_m_s_old.n_a_priviledge: ~1 rows (approximately)
/*!40000 ALTER TABLE `n_a_priviledge` DISABLE KEYS */;
INSERT INTO `n_a_privilege` (`IDApp`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `first_name`, `last_name`, `UserName`, `Email`, `Divisi`, `Password`, `Picture`, `Last_login`, `Last_form`, `Computer_Name`, `IP_Address`, `Role`, `Is_SuperUser`, `Is_Staff`, `Is_Active`, `Date_Joined`) VALUES
	(1, '', NULL, NULL, '', '', 'rimba88', 'rimba@88spares.com', 'IT', 'pbkdf2_sha256$36000$vACo7Q3KBjS5$UOEFP68Os1qQVdFh5PlbOOC8WpFufG8MGnrtP/pXQKA=', 'dir_for_rimba88\\20180515_100310.jpg', '2018-08-29 11:55:12.414875', NULL, '', '', 1, 1, 0, 1, NULL);
/*!40000 ALTER TABLE `n_a_priviledge` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_priviledge_form: ~6 rows (approximately)
/*!40000 ALTER TABLE `n_a_priviledge_form` DISABLE KEYS */;
INSERT INTO `n_a_privilege_form` (`IDApp`, `Form_id`, `Form_name`, `Form_name_ori`) VALUES
	(1, '0001M', 'Suplier Form', 'n_a_suplier'),
	(2, '0002M', 'Employee Form', 'employee'),
	(3, '0003M', 'Goods Form', 'goods'),
	(6, '0001T', 'Goods Receive', 'n_a_goods_receive'),
	(7, '0004M', 'User Priviledge', 'n_a_priviledge'),
	(8, '0001O', 'Fix Asset Form', 'n_a_acc_fa');
/*!40000 ALTER TABLE `n_a_priviledge_form` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_priviledge_groups: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_priviledge_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_priviledge_groups` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_priviledge_user_permissions: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_priviledge_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_priviledge_user_permissions` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_sys_priviledge: ~20 rows (approximately)
/*!40000 ALTER TABLE `n_a_sys_priviledge` DISABLE KEYS */;
INSERT INTO `n_a_sys_privilege` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `Permission`, `InActive`, `FK_PForm`, `User_id`) VALUES
	(1, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow View', 0, 1, 1),
	(2, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow Add', 0, 1, 1),
	(3, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow Edit', 0, 1, 1),
	(4, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow Delete', 0, 1, 1),
	(5, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow View', 0, 2, 1),
	(6, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow Add', 0, 2, 1),
	(7, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow Edit', 0, 2, 1),
	(8, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow Delete', 0, 2, 1),
	(9, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow View', 0, 3, 1),
	(10, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow Add', 0, 3, 1),
	(11, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow Edit', 0, 3, 1),
	(12, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow Delete', 0, 3, 1),
	(13, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow View', 0, 7, 1),
	(14, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow Add', 0, 7, 1),
	(15, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow Edit', 0, 7, 1),
	(16, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow Delete', 0, 7, 1),
	(17, '2018-08-22 15:33:58.826717', 'rimba88', NULL, NULL, 'Allow View', 0, 6, 1),
	(18, '2018-08-22 15:33:58.826717', 'rimba88', NULL, NULL, 'Allow Add', 0, 6, 1),
	(20, '2018-08-22 15:33:58.826717', 'rimba88', NULL, NULL, 'Allow Delete', 0, 6, 1),
	(21, '2018-08-22 15:35:43.457500', 'rimba88', NULL, NULL, 'Allow Edit', 0, 6, 1);
/*!40000 ALTER TABLE `n_a_sys_priviledge` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
