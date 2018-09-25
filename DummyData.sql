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

-- Dumping data for table na_m_s.auth_group: ~0 rows (approximately)
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;

-- Dumping data for table na_m_s.auth_group_permissions: ~0 rows (approximately)
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;

-- Dumping data for table na_m_s.auth_permission: ~114 rows (approximately)
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
REPLACE INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add association', 1, 'add_association'),
	(2, 'Can change association', 1, 'change_association'),
	(3, 'Can delete association', 1, 'delete_association'),
	(4, 'Can add code', 2, 'add_code'),
	(5, 'Can change code', 2, 'change_code'),
	(6, 'Can delete code', 2, 'delete_code'),
	(7, 'Can add nonce', 3, 'add_nonce'),
	(8, 'Can change nonce', 3, 'change_nonce'),
	(9, 'Can delete nonce', 3, 'delete_nonce'),
	(10, 'Can add user social auth', 4, 'add_usersocialauth'),
	(11, 'Can change user social auth', 4, 'change_usersocialauth'),
	(12, 'Can delete user social auth', 4, 'delete_usersocialauth'),
	(13, 'Can add partial', 5, 'add_partial'),
	(14, 'Can change partial', 5, 'change_partial'),
	(15, 'Can delete partial', 5, 'delete_partial'),
	(16, 'Can add employee', 6, 'add_employee'),
	(17, 'Can change employee', 6, 'change_employee'),
	(18, 'Can delete employee', 6, 'delete_employee'),
	(19, 'Can add goods', 7, 'add_goods'),
	(20, 'Can change goods', 7, 'change_goods'),
	(21, 'Can delete goods', 7, 'delete_goods'),
	(22, 'Can add log event', 8, 'add_logevent'),
	(23, 'Can change log event', 8, 'change_logevent'),
	(24, 'Can delete log event', 8, 'delete_logevent'),
	(25, 'Can add n a_ goods receive_detail', 9, 'add_na_goodsreceive_detail'),
	(26, 'Can change n a_ goods receive_detail', 9, 'change_na_goodsreceive_detail'),
	(27, 'Can delete n a_ goods receive_detail', 9, 'delete_na_goodsreceive_detail'),
	(28, 'Can add na acc fa', 10, 'add_naaccfa'),
	(29, 'Can change na acc fa', 10, 'change_naaccfa'),
	(30, 'Can delete na acc fa', 10, 'delete_naaccfa'),
	(31, 'Can add na appparams', 11, 'add_naappparams'),
	(32, 'Can change na appparams', 11, 'change_naappparams'),
	(33, 'Can delete na appparams', 11, 'delete_naappparams'),
	(34, 'Can add na disposal', 12, 'add_nadisposal'),
	(35, 'Can change na disposal', 12, 'change_nadisposal'),
	(36, 'Can delete na disposal', 12, 'delete_nadisposal'),
	(37, 'Can add naga maintenance', 13, 'add_nagamaintenance'),
	(38, 'Can change naga maintenance', 13, 'change_nagamaintenance'),
	(39, 'Can delete naga maintenance', 13, 'delete_nagamaintenance'),
	(40, 'Can add na ga outwards', 14, 'add_nagaoutwards'),
	(41, 'Can change na ga outwards', 14, 'change_nagaoutwards'),
	(42, 'Can delete na ga outwards', 14, 'delete_nagaoutwards'),
	(43, 'Can add na ga receive', 15, 'add_nagareceive'),
	(44, 'Can change na ga receive', 15, 'change_nagareceive'),
	(45, 'Can delete na ga receive', 15, 'delete_nagareceive'),
	(46, 'Can add naga return', 16, 'add_nagareturn'),
	(47, 'Can change naga return', 16, 'change_nagareturn'),
	(48, 'Can delete naga return', 16, 'delete_nagareturn'),
	(49, 'Can add na ga vn history', 17, 'add_nagavnhistory'),
	(50, 'Can change na ga vn history', 17, 'change_nagavnhistory'),
	(51, 'Can delete na ga vn history', 17, 'delete_nagavnhistory'),
	(52, 'Can add na goods equipment', 18, 'add_nagoodsequipment'),
	(53, 'Can change na goods equipment', 18, 'change_nagoodsequipment'),
	(54, 'Can delete na goods equipment', 18, 'delete_nagoodsequipment'),
	(55, 'Can add na goods history', 19, 'add_nagoodshistory'),
	(56, 'Can change na goods history', 19, 'change_nagoodshistory'),
	(57, 'Can delete na goods history', 19, 'delete_nagoodshistory'),
	(58, 'Can add na goods lending', 20, 'add_nagoodslending'),
	(59, 'Can change na goods lending', 20, 'change_nagoodslending'),
	(60, 'Can delete na goods lending', 20, 'delete_nagoodslending'),
	(61, 'Can add na goods lost', 21, 'add_nagoodslost'),
	(62, 'Can change na goods lost', 21, 'change_nagoodslost'),
	(63, 'Can delete na goods lost', 21, 'delete_nagoodslost'),
	(64, 'Can add na goods outwards', 22, 'add_nagoodsoutwards'),
	(65, 'Can change na goods outwards', 22, 'change_nagoodsoutwards'),
	(66, 'Can delete na goods outwards', 22, 'delete_nagoodsoutwards'),
	(67, 'Can add na goods receive', 23, 'add_nagoodsreceive'),
	(68, 'Can change na goods receive', 23, 'change_nagoodsreceive'),
	(69, 'Can delete na goods receive', 23, 'delete_nagoodsreceive'),
	(70, 'Can add na goods receive_other', 24, 'add_nagoodsreceive_other'),
	(71, 'Can change na goods receive_other', 24, 'change_nagoodsreceive_other'),
	(72, 'Can delete na goods receive_other', 24, 'delete_nagoodsreceive_other'),
	(73, 'Can add na goods return', 25, 'add_nagoodsreturn'),
	(74, 'Can change na goods return', 25, 'change_nagoodsreturn'),
	(75, 'Can delete na goods return', 25, 'delete_nagoodsreturn'),
	(76, 'Can add na maintenance', 26, 'add_namaintenance'),
	(77, 'Can change na maintenance', 26, 'change_namaintenance'),
	(78, 'Can delete na maintenance', 26, 'delete_namaintenance'),
	(79, 'Can add na privilege_form', 27, 'add_naprivilege_form'),
	(80, 'Can change na privilege_form', 27, 'change_naprivilege_form'),
	(81, 'Can delete na privilege_form', 27, 'delete_naprivilege_form'),
	(82, 'Can add na stock', 28, 'add_nastock'),
	(83, 'Can change na stock', 28, 'change_nastock'),
	(84, 'Can delete na stock', 28, 'delete_nastock'),
	(85, 'Can add na supplier', 29, 'add_nasupplier'),
	(86, 'Can change na supplier', 29, 'change_nasupplier'),
	(87, 'Can delete na supplier', 29, 'delete_nasupplier'),
	(88, 'Can add na sys privilege', 30, 'add_nasysprivilege'),
	(89, 'Can change na sys privilege', 30, 'change_nasysprivilege'),
	(90, 'Can delete na sys privilege', 30, 'delete_nasysprivilege'),
	(91, 'Can add na privilege', 31, 'add_naprivilege'),
	(92, 'Can change na privilege', 31, 'change_naprivilege'),
	(93, 'Can delete na privilege', 31, 'delete_naprivilege'),
	(94, 'Can add log entry', 32, 'add_logentry'),
	(95, 'Can change log entry', 32, 'change_logentry'),
	(96, 'Can delete log entry', 32, 'delete_logentry'),
	(97, 'Can add permission', 33, 'add_permission'),
	(98, 'Can change permission', 33, 'change_permission'),
	(99, 'Can delete permission', 33, 'delete_permission'),
	(100, 'Can add group', 34, 'add_group'),
	(101, 'Can change group', 34, 'change_group'),
	(102, 'Can delete group', 34, 'delete_group'),
	(103, 'Can add content type', 35, 'add_contenttype'),
	(104, 'Can change content type', 35, 'change_contenttype'),
	(105, 'Can delete content type', 35, 'delete_contenttype'),
	(106, 'Can add session', 36, 'add_session'),
	(107, 'Can change session', 36, 'change_session'),
	(108, 'Can delete session', 36, 'delete_session'),
	(109, 'Can add na notifications', 37, 'add_nanotifications'),
	(110, 'Can change na notifications', 37, 'change_nanotifications'),
	(111, 'Can delete na notifications', 37, 'delete_nanotifications'),
	(112, 'Can add session', 38, 'add_nasession'),
	(113, 'Can change session', 38, 'change_nasession'),
	(114, 'Can delete session', 38, 'delete_nasession');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;

-- Dumping data for table na_m_s.django_admin_log: ~1 rows (approximately)
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
REPLACE INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2018-07-29 18:42:49.836000', '8', 'Fix Asset Form', 1, '[{"added": {}}]', 25, 1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;

-- Dumping data for table na_m_s.django_content_type: ~38 rows (approximately)
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
REPLACE INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(32, 'admin', 'logentry'),
	(38, 'app', 'nasession'),
	(34, 'auth', 'group'),
	(33, 'auth', 'permission'),
	(35, 'contenttypes', 'contenttype'),
	(6, 'NA_Models', 'employee'),
	(7, 'NA_Models', 'goods'),
	(8, 'NA_Models', 'logevent'),
	(10, 'NA_Models', 'naaccfa'),
	(11, 'NA_Models', 'naappparams'),
	(12, 'NA_Models', 'nadisposal'),
	(13, 'NA_Models', 'nagamaintenance'),
	(14, 'NA_Models', 'nagaoutwards'),
	(15, 'NA_Models', 'nagareceive'),
	(16, 'NA_Models', 'nagareturn'),
	(17, 'NA_Models', 'nagavnhistory'),
	(18, 'NA_Models', 'nagoodsequipment'),
	(19, 'NA_Models', 'nagoodshistory'),
	(20, 'NA_Models', 'nagoodslending'),
	(21, 'NA_Models', 'nagoodslost'),
	(22, 'NA_Models', 'nagoodsoutwards'),
	(23, 'NA_Models', 'nagoodsreceive'),
	(24, 'NA_Models', 'nagoodsreceive_other'),
	(25, 'NA_Models', 'nagoodsreturn'),
	(26, 'NA_Models', 'namaintenance'),
	(31, 'NA_Models', 'naprivilege'),
	(27, 'NA_Models', 'naprivilege_form'),
	(28, 'NA_Models', 'nastock'),
	(29, 'NA_Models', 'nasupplier'),
	(30, 'NA_Models', 'nasysprivilege'),
	(9, 'NA_Models', 'na_goodsreceive_detail'),
	(37, 'NA_Notifications', 'nanotifications'),
	(36, 'sessions', 'session'),
	(1, 'social_django', 'association'),
	(2, 'social_django', 'code'),
	(3, 'social_django', 'nonce'),
	(5, 'social_django', 'partial'),
	(4, 'social_django', 'usersocialauth');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;

-- Dumping data for table na_m_s.django_session: ~9 rows (approximately)
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
REPLACE INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('4smkhb6s9g3co7i9m9r4pmguzvcswh2d', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-07-22 22:43:49.085896'),
	('775lo3x9wsokqi8r4qx5xz1296u8zxg7', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-08-21 19:21:51.317133'),
	('9yxz8d0s6du2pnx6jwcr3n114kc6rkwx', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-08-28 19:13:18.579303'),
	('obqjsmh8deccxvyb6l9tj26eyjp9mqfx', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-08-07 17:07:30.005363'),
	('ojwa5k07dj3ldld811smujxvxl1bzl56', 'N2I1OWUyMThhNzJhN2I3ZDMzZWRjYTYyZGU3NWYxZjEzYzZmODc2Nzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwYWM3YTJmMGFmNjMwNDg4MGIzNDVlYmExMDYwNTY1NmJkOWRiNzQyIn0=', '2018-08-07 22:07:21.378000'),
	('q7g44p2rbzp1ngswptg2ojv4dlj1mnrt', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-09-12 11:55:12.464925'),
	('qw93t46a024okacw41qglroqwm1zn46b', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-09-26 18:15:19.600617'),
	('s5ks3lch8odtt94dyz7hd2zzjwqea6wd', 'N2I1OWUyMThhNzJhN2I3ZDMzZWRjYTYyZGU3NWYxZjEzYzZmODc2Nzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwYWM3YTJmMGFmNjMwNDg4MGIzNDVlYmExMDYwNTY1NmJkOWRiNzQyIn0=', '2018-08-06 22:32:34.274000'),
	('wo4rqimlfz8wr2uxw8v9q4uq36vl0w32', 'N2I1OWUyMThhNzJhN2I3ZDMzZWRjYTYyZGU3NWYxZjEzYzZmODc2Nzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwYWM3YTJmMGFmNjMwNDg4MGIzNDVlYmExMDYwNTY1NmJkOWRiNzQyIn0=', '2018-08-12 19:48:15.585000');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;

-- Dumping data for table na_m_s.employee: ~9 rows (approximately)
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
REPLACE INTO `employee` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `InActive`, `Descriptions`, `NIK`, `Employee_Name`, `TypeApp`, `JobType`, `Gender`, `Status`, `TelpHP`, `Territory`) VALUES
	(1, '2018-08-20 16:45:37.409544', 'rimba88', NULL, NULL, 0, 'Nufarm IT Manager', '2011131', 'Tandry Adrian Hartanto', 'P', 'IT Bussines Developmen Manager', 'M', 'M', '0818925270', 'JAKARTA'),
	(2, '2018-08-20 16:49:27.557851', 'rimba88', '2018-08-20 17:28:46.990922', 'rimba88', 0, 'Pak suroto asalnya Office Boy menggantikan Ridho', 'C020', 'Suroto', 'P', 'RECEPTIONIST', 'M', 'M', '087808451709', 'JAKARTA'),
	(3, '2018-08-20 16:56:03.069993', 'rimba88', NULL, NULL, 0, 'Luther Juan pengganti Muhammad Syahwil', '2017457', 'Luther Juan Sanda', 'P', 'Purchasing Executif', 'M', 'S', '08992474947', 'JAKARTA'),
	(4, '2018-08-20 17:09:48.969665', 'rimba88', '2018-08-20 17:28:41.245768', 'rimba88', 0, 'pak iman naik jabatan sekarang jafi GA Supervisor menggantikan Tri Wahyudi', '20050201', 'Iman Utomo', 'P', 'GA Supervisor', 'M', 'M', '085693330550', 'JAKARTA'),
	(5, '2018-08-20 17:18:33.601710', 'rimba88', NULL, NULL, 0, 'Wahyu bima karyawan menggantikan posisi surya sofianto', '2016367', 'R. Wahyoe Bima D.K', 'P', 'Purchasing Executif', 'M', 'M', '082123326963', 'JAKARTA'),
	(6, '2018-08-20 17:24:45.145917', 'rimba88', '2018-08-20 17:28:33.328118', 'rimba88', 0, 'SENIOR IT NUFARM', '990642', 'Indradjaja Tjandra Poernama', 'P', 'IT SUPERVISOR', 'M', 'M', '08129239707', 'JAKARTA'),
	(7, '2018-08-20 17:27:55.332142', 'rimba88', '2018-08-20 17:28:29.206281', 'rimba88', 0, 'Nandar memulai karir di nufarm sebagai programmer di bagian sales retailer dan distributor', '201311', 'Kusnandar', 'P', 'IT PROGRAMMER', 'M', 'M', '08118855107', 'JAKARTA'),
	(8, '2018-08-20 18:29:16.104895', 'rimba88', NULL, NULL, 0, 'Sudah keluar di ganti sama Luther Juan', 'F212014512', 'Junaid syahwil', 'P', 'PURCHASING EXECUTIVE', 'M', 'M', '083876640037', 'JAKARTA'),
	(9, '2018-08-20 18:48:14.723854', 'rimba88', NULL, NULL, 0, 'Sidik sebelumnya menjabat sebagai IT technical support, mula tahun 2016 berpindah ke divisi marketing sebagai marketing digital', '20040903', 'SIDIK HARTADI', 'P', 'MARKETING DIGITAL', 'M', 'M', '08118855106', 'JAKARTA');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;

-- Dumping data for table na_m_s.logevent: ~14 rows (approximately)
/*!40000 ALTER TABLE `logevent` DISABLE KEYS */;
REPLACE INTO `logevent` (`IDApp`, `CreatedDate`, `CreatedBy`, `NameApp`, `Model`, `descriptions`) VALUES
	(1, '2018-05-05 20:39:49.000000', 'Admin', 'Deleted Suplier', '', '{"deleted": ["AF122FHJ", "Rimba P", "Cimahi", "0221122331144", "0895322085649", "Mang Nandar", 1, "2018-01-06", "admin"]}'),
	(2, '2018-05-05 20:47:28.000000', 'rimba47prayoga', 'Deleted Suplier', '', '{"deleted": ["AF122uui", "Rimba", "Cimahi", "0221122331144", "0895322085649", "Mang Nandar", 0, "2018-01-01", "admin"]}'),
	(3, '2018-05-10 19:20:55.000000', 'rimba47prayoga', 'Deleted Suplier', '', '{"deleted": ["AF122fg", "Rimba", "Cimahi", "0221122331144", "0895322085649", "Mang Nandar", 0, "2018-01-01", "admin"]}'),
	(4, '2018-05-13 12:54:16.000000', 'rimba47prayoga', 'Deleted Suplier', '', '{"deleted": ["AF343534", "Teja", "Unknown", "0898985968", "0875764786545", "Rimba", 1, "2018-05-13", "rimba47prayoga"]}'),
	(5, '2018-05-24 22:13:40.000000', 'rimba47prayoga', 'Deleted Suplier', '', '{"deleted": ["AF1229", "Rimba", "Cimahi", "0221122331144", "0895322085649", "Mang Nandar", 0, "2018-01-01", "admin"]}'),
	(6, '2018-05-27 21:28:08.000000', 'rimba47prayoga', 'Deleted Employee', '', '{"C": "C", "M": "S", "Descriptions": "rimba47prayoga", "0895322085649": "Cimahi", "011247487875411": "Rimba"}'),
	(7, '2018-06-23 18:02:21.000000', 'admin', 'Deleted Employee', '', '{"deleted": ["00111234887898", "Rimba", "C", "C", "M", "S", "08984512313574", "Cimahi", "Employee", "27 January 2018 00:00:00", "rimba47prayoga"]}'),
	(8, '2018-06-23 18:05:27.000000', 'admin', 'Deleted Employee', '', '{"deleted": ["1121246345", "Rimba P", "P", "P", "M", "M", "0895322085649", "Citeureup", "There\'s No Descriptions", 0, "28 January 2018 00:00:00", "rimba47prayoga"]}'),
	(9, '2018-06-23 18:05:59.000000', 'admin', 'Deleted Suplier', '', '{"deleted": ["AF1223", "Rimba", "Cimahi", "0221122331144", "0895322085649", "Mang Nandar", 0, "06 January 2018 00:00:00", "admin"]}'),
	(10, '2018-06-23 18:06:06.000000', 'admin', 'Deleted Suplier', '', '{"deleted": ["AD3323", "Teja", "Unknown", "0223544464", "0223544464", "Rimba", 1, "13 May 2018 00:00:00", "rimba47prayoga"]}'),
	(11, '2018-06-23 18:31:19.000000', 'admin', 'Deleted Employee', '', '{"deleted": ["11223445", "Rimba P", "K", "K", "M", "S", "08953320215121", "Cisurupan", "There\'s No Descriptions", 1, "25 January 2018 00:00:00", "rimba47prayoga"]}'),
	(12, '2018-08-16 16:46:39.068477', 'rimba88', 'Deleted Goods', '', '{"deleted": ["it-008", "EKSTERNAL HARDISK", "SEAGATE", "0.0000", "SL", "Pcs", "5.00", "Gudang IT", "Price tidak di input di sini", 0, "16 August 2018 00:00:00", "rimba88", null, null]}'),
	(13, '2018-08-16 17:22:11.039349', 'rimba88', 'Deleted Goods', '', '{"deleted": ["it-008", "EKSTERNAL HARDISK", "SEAGATE", "0.0000", "SL", "Pcs", "5.00", "Gudang IT", "Price tidak di input di sini", 0, "16 August 2018 00:00:00", "rimba88", null, null]}'),
	(14, '2018-08-16 18:16:15.616851', 'rimba88', 'Deleted Goods', '', '{"deleted": ["GA_003", "HP High End", "SAMSUNG", "0.0000", "SL", "Unit", "5.00", "Gudang IT", "untuk HP yang mempunyai nila tinggi di masukan dalam FA GA", 0, "16 August 2018 00:00:00", "rimba88", null, null]}');
/*!40000 ALTER TABLE `logevent` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_acc_fa: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_acc_fa` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_acc_fa` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_appparams: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_appparams` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_appparams` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_disposal: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_disposal` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_disposal` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_equipment: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_equipment` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_equipment` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_ga_maintenance: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_ga_maintenance` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_maintenance` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_ga_outwards: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_ga_outwards` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_outwards` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_ga_outwards_add_equipment: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_ga_outwards_add_equipment` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_outwards_add_equipment` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_ga_outwards_equipment: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_ga_outwards_equipment` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_outwards_equipment` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_ga_receive: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_ga_receive` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_receive` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_ga_return: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_ga_return` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_return` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_ga_vn_history: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_ga_vn_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_vn_history` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods: ~26 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods` DISABLE KEYS */;
REPLACE INTO `n_a_goods` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `InActive`, `Descriptions`, `ItemCode`, `GoodsName`, `BrandName`, `PricePerUnit`, `DepreciationMethod`, `Unit`, `EconomicLife`, `Placement`, `typeapp`) VALUES
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
/*!40000 ALTER TABLE `n_a_goods_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_history` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_lending: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_lending` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_lending` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_lost: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_lost` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_lost` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_outwards: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_outwards` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_outwards` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_receive: ~6 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_receive` DISABLE KEYS */;
REPLACE INTO `n_a_goods_receive` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `DateReceived`, `TotalPurchase`, `TotalReceived`, `Descriptions`, `DescBySystem`, `REFNO`, `FK_Supplier`, `fk_goods`, `FK_P_R_By`, `FK_ReceivedBy`) VALUES
	(1, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, '2016-03-04 00:00:00.000000', 8, 8, 'Pembelian HP J5 tahap pertama untuk IT dan marketing, dan IConcept dan kepentingan FMS lainnya', '(SAMSUNG, Type : J5, SN : 357005072234246-357004072234249, SAMSUNG, Type : J5, SN : 357004071145081-357005071145088, SAMSUNG, Type : J5, SN : 357005071145054-357004071145057, SAMSUNG, Type : J5, SN : 357004071145024-357005071145021, SAMSUNG, Type : J5, SN : 357004071144027-357005071144024, SAMSUNG, Type : J5, SN : 357004072234249-357005072234246, SAMSUNG, Type : J5, SN : 357004071145115-357004071145115, SAMSUNG, Type : J5, SN : ICONCEPT)', '15/16-000128-01', 'ERA004IDR', 3, 8, 9),
	(2, '2018-08-28 00:00:00.000000', 'nandar', NULL, NULL, '2015-07-30 00:00:00.000000', 6, 6, '', '(DELL, Type : LATITUDE E5440, SN : 7SOGWZ1/0001402, DELL, Type : LATITUDE E5440, SN : 3L4Z062/0001403, DELL, Type : LATITUDE E5440, SN :  3S30l32/0001404, DELL, Type : LATITUDE E5440, SN : HHS2F12/0001405, DELL, Type : LATITUDE E5440, SN : 1V1GWZ1/0001406, DELL, Type : LATITUDE E5440, SN : 3K65P12/0001407)', '14/15-000141-01', 'PAR002USD', 2, 8, 9),
	(3, '2018-08-30 00:00:00.000000', 'rimba88', NULL, NULL, '2015-05-07 00:00:00.000000', 10, 10, '', '(DELL, Type : Latitude E5450, SN : G1KFN32/0001385, DELL, Type : Latitude E5450, SN : 81NZFRF2/0001386, DELL, Type : Latitude E5450, SN : 3HSJN32/0001387, DELL, Type : Latitude E5450, SN : F6JHN32/0001388, DELL, Type : Latitude E5450, SN : 8VT2F12/0001389, DELL, Type : Latitude E5450, SN : 6HSJN32/0001390, DELL, Type : Latitude E5450, SN : G1KFN32/0001391, DELL, Type : Latitude E5450, SN : 4T2WR32/0001392, DELL, Type : Latitude E5450, SN : F03WR32/0001393, DELL, Type : Latitude E5450, SN : G1KFN', '14/15-000186-01', 'PAR002USD', 2, 8, 9),
	(4, '2018-08-31 00:00:00.000000', 'rimba88', NULL, NULL, '2017-07-06 00:00:00.000000', 6, 6, '', '(NEC, Type : VE 303 G, SN : 6Y41310CD/0001561, NEC, Type : VE 303 G, SN : 6X41082CD/0001562, NEC, Type : VE 303 G, SN : 6Y41296CD/0001563, NEC, Type : VE 303 G, SN : GX41075CD/0001564, NEC, Type : VE 303 G, SN : GX41127CD/0001565, NEC, Type : VE 303 G, SN : 0001566/RMeeting)', '16/17-000183-01', 'WID001IDR', 4, 5, 6),
	(5, '2018-09-05 00:00:00.000000', 'rimba88', NULL, NULL, '2017-07-03 00:00:00.000000', 1, 1, '', '(SAMSUNG, Type : S7, SN : 0001567)', '16/17-000177-01', 'ERA004IDR', 3, 5, 4),
	(6, '2018-09-11 00:00:00.000000', 'rimba88', '2018-09-13 00:00:00.000000', 'rimba88', '2017-05-02 00:00:00.000000', 4, 4, 'Reg no merefer ke PO number', '(WESTERN DIGITAL, Type : 3.5 MM, SN : 0001549, WESTERN DIGITAL, Type : 3.5 MM, SN : 0001547, WESTERN DIGITAL, Type : 3.5 MM, SN : 0001548, WESTERN DIGITAL, Type : 3.5 MM, SN : 0001546)', 'PO17093104', 'MUL016IDR', 10, 5, 6);
/*!40000 ALTER TABLE `n_a_goods_receive` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_receive_detail: ~35 rows (approximately)
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
	(14, '2018-08-28 00:00:00.000000', 'nandar', NULL, NULL, 'DELL', 15001875.0000, 'LATITUDE E5440', 5.00, '2020-07-28 00:00:00.000000', '3K65P12/0001407', 2),
	(15, '2018-08-30 00:00:00.000000', 'rimba88', '2018-09-06 00:00:00.000000', 'rimba88', 'DELL', 14585625.0000, 'LATITUDE E5450', 1.00, '2016-05-06 00:00:00.000000', 'G1KFN32/0001385', 3),
	(16, '2018-08-30 00:00:00.000000', 'rimba88', '2018-09-06 00:00:00.000000', 'rimba88', 'DELL', 14585625.0000, 'LATITUDE E5450', 1.00, '2016-05-06 00:00:00.000000', '81NZFRF2/0001386', 3),
	(17, '2018-08-30 00:00:00.000000', 'rimba88', '2018-09-06 00:00:00.000000', 'rimba88', 'DELL', 14585625.0000, 'LATITUDE E5450', 1.00, '2016-05-06 00:00:00.000000', '3HSJN32/0001387', 3),
	(18, '2018-08-30 00:00:00.000000', 'rimba88', '2018-09-06 00:00:00.000000', 'rimba88', 'DELL', 14585625.0000, 'LATITUDE E5450', 1.00, '2016-05-06 00:00:00.000000', 'F6JHN32/0001388', 3),
	(19, '2018-08-30 00:00:00.000000', 'rimba88', '2018-09-06 00:00:00.000000', 'rimba88', 'DELL', 14585625.0000, 'LATITUDE E5450', 1.00, '2016-05-06 00:00:00.000000', '8VT2F12/0001389', 3),
	(20, '2018-08-30 00:00:00.000000', 'rimba88', '2018-09-06 00:00:00.000000', 'rimba88', 'DELL', 14585625.0000, 'LATITUDE E5450', 1.00, '2016-05-06 00:00:00.000000', '6HSJN32/0001390', 3),
	(21, '2018-08-30 00:00:00.000000', 'rimba88', '2018-09-06 00:00:00.000000', 'rimba88', 'DELL', 14585625.0000, 'LATITUDE E5450', 1.00, '2016-05-06 00:00:00.000000', 'G1KFN32/0001391', 3),
	(22, '2018-08-30 00:00:00.000000', 'rimba88', '2018-09-06 00:00:00.000000', 'rimba88', 'DELL', 14585625.0000, 'LATITUDE E5450', 1.00, '2016-05-06 00:00:00.000000', '4T2WR32/0001392', 3),
	(23, '2018-08-30 00:00:00.000000', 'rimba88', '2018-09-06 00:00:00.000000', 'rimba88', 'DELL', 14585625.0000, 'LATITUDE E5450', 1.00, '2016-05-06 00:00:00.000000', 'F03WR32/0001393', 3),
	(24, '2018-08-30 00:00:00.000000', 'rimba88', '2018-09-06 00:00:00.000000', 'rimba88', 'DELL', 14585625.0000, 'LATITUDE E5450', 1.00, '2016-05-06 00:00:00.000000', 'G1KFN32/0001395', 3),
	(25, '2018-08-31 00:00:00.000000', 'rimba88', '2018-09-03 00:00:00.000000', 'rimba88', 'NEC', 4400000.0000, 'VE 303 G', 1.00, '2018-07-06 00:00:00.000000', '6Y41310CD/0001561', 4),
	(26, '2018-08-31 00:00:00.000000', 'rimba88', '2018-09-03 00:00:00.000000', 'rimba88', 'NEC', 4400000.0000, 'VE 303 G', 1.00, '2018-07-06 00:00:00.000000', '6X41082CD/0001562', 4),
	(27, '2018-08-31 00:00:00.000000', 'rimba88', '2018-09-03 00:00:00.000000', 'rimba88', 'NEC', 4400000.0000, 'VE 303 G', 1.00, '2018-07-06 00:00:00.000000', '6Y41296CD/0001563', 4),
	(28, '2018-08-31 00:00:00.000000', 'rimba88', '2018-09-03 00:00:00.000000', 'rimba88', 'NEC', 4400000.0000, 'VE 303 G', 1.00, '2018-07-06 00:00:00.000000', 'GX41075CD/0001564', 4),
	(29, '2018-08-31 00:00:00.000000', 'rimba88', '2018-09-03 00:00:00.000000', 'rimba88', 'NEC', 4400000.0000, 'VE 303 G', 1.00, '2018-07-06 00:00:00.000000', 'GX41127CD/0001565', 4),
	(30, '2018-08-31 00:00:00.000000', 'rimba88', '2018-09-03 00:00:00.000000', 'rimba88', 'NEC', 4400000.0000, 'VE 303 G', 1.00, '2018-07-06 00:00:00.000000', '0001566/RM', 4),
	(31, '2018-09-05 00:00:00.000000', 'rimba88', NULL, NULL, 'SAMSUNG', 7227273.0000, 'S7', 1.00, '2018-07-03 00:00:00.000000', '0001567', 5),
	(35, '2018-09-11 00:00:00.000000', 'rimba88', '2018-09-13 00:00:00.000000', 'rimba88', 'WESTERN DIGITAL', 1815000.0000, '3.5 MM', 1.00, '2018-05-02 00:00:00.000000', '0001549', 6),
	(39, '2018-09-13 00:00:00.000000', 'rimba88', NULL, NULL, 'WESTERN DIGITAL', 1815000.0000, '3.5 MM', 1.00, '2018-05-02 00:00:00.000000', '0001547', 6),
	(40, '2018-09-13 00:00:00.000000', 'rimba88', NULL, NULL, 'WESTERN DIGITAL', 1815000.0000, '3.5 MM', 1.00, '2018-05-02 00:00:00.000000', '0001548', 6),
	(41, '2018-09-13 00:00:00.000000', 'rimba88', NULL, NULL, 'WESTERN DIGITAL', 1815000.0000, '3.5 MM', 1.00, '2018-05-02 00:00:00.000000', '0001546', 6);
/*!40000 ALTER TABLE `n_a_goods_receive_detail` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_receive_other: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_receive_other` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_receive_other` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_goods_return: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_return` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_return` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_maintenance: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_maintenance` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_maintenance` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_notifications: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_notifications` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_notifications_user: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_notifications_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_notifications_user` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_privilege: ~1 rows (approximately)
/*!40000 ALTER TABLE `n_a_privilege` DISABLE KEYS */;
REPLACE INTO `n_a_privilege` (`IDApp`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `first_name`, `last_name`, `UserName`, `Email`, `Divisi`, `Password`, `Picture`, `Last_login`, `Last_form`, `Computer_Name`, `IP_Address`, `Role`, `Is_SuperUser`, `Is_Staff`, `Is_Active`, `Date_Joined`) VALUES
	(1, '', NULL, NULL, '', '', 'rimba88', 'rimba@88spares.com', 'IT', 'pbkdf2_sha256$36000$vACo7Q3KBjS5$UOEFP68Os1qQVdFh5PlbOOC8WpFufG8MGnrtP/pXQKA=', 'dir_for_rimba88\\20180515_100310.jpg', '2018-09-19 17:24:33.258169', NULL, '', '', 1, 1, 0, 1, NULL);
/*!40000 ALTER TABLE `n_a_privilege` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_privilege_form: ~6 rows (approximately)
/*!40000 ALTER TABLE `n_a_privilege_form` DISABLE KEYS */;
REPLACE INTO `n_a_privilege_form` (`IDApp`, `Form_id`, `Form_name`, `Form_name_ori`) VALUES
	(1, '0001M', 'Suplier Form', 'n_a_suplier'),
	(2, '0002M', 'Employee Form', 'employee'),
	(3, '0003M', 'Goods Form', 'goods'),
	(6, '0001T', 'Goods Receive', 'n_a_goods_receive'),
	(7, '0004M', 'User Priviledge', 'n_a_priviledge'),
	(8, '0001O', 'Fix Asset Form', 'n_a_acc_fa');
/*!40000 ALTER TABLE `n_a_privilege_form` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_privilege_groups: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_privilege_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_privilege_groups` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_privilege_user_permissions: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_privilege_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_privilege_user_permissions` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_session: ~1 rows (approximately)
/*!40000 ALTER TABLE `n_a_session` DISABLE KEYS */;
REPLACE INTO `n_a_session` (`session_key`, `session_data`, `expire_date`, `user_id`) VALUES
	('jmco0b2jkf1ofsy3y4ykf4ol16npebsn', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-10-03 17:24:33.341849', 1);
/*!40000 ALTER TABLE `n_a_session` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_stock: ~4 rows (approximately)
/*!40000 ALTER TABLE `n_a_stock` DISABLE KEYS */;
REPLACE INTO `n_a_stock` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `T_Goods_Spare`, `TotalQty`, `TIsUsed`, `TIsNew`, `TIsRenew`, `TIsBroken`, `TGoods_Return`, `TGoods_Received`, `TMaintenance`, `TDisposal`, `TIsLost`, `FK_Goods`) VALUES
	(1, '2018-08-21 17:04:53.000000', 'rimba88', '2018-09-05 19:03:15.000000', 'rimba88', 0, NULL, 0, 9, 0, NULL, 0, 9, 0, NULL, NULL, 3),
	(2, '2018-08-28 23:21:55.000000', 'nandar', '2018-09-06 19:55:57.000000', 'rimba88', 0, NULL, 0, 16, 0, NULL, 0, 16, 0, NULL, NULL, 2),
	(3, '2018-08-31 16:55:32.000000', 'rimba88', '2018-09-03 15:36:53.000000', 'rimba88', 0, NULL, 0, 6, 0, NULL, 0, 6, 0, NULL, NULL, 4),
	(4, '2018-09-11 11:53:56.000000', 'rimba88', '2018-09-13 18:46:19.000000', 'rimba88', 0, NULL, 0, 1, 0, NULL, 0, 4, 0, NULL, NULL, 10);
/*!40000 ALTER TABLE `n_a_stock` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_supplier: ~10 rows (approximately)
/*!40000 ALTER TABLE `n_a_supplier` DISABLE KEYS */;
REPLACE INTO `n_a_supplier` (`CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `InActive`, `SupplierCode`, `SupplierName`, `Address`, `Telp`, `HP`, `ContactPerson`) VALUES
	('2018-08-20 18:53:37.355965', 'rimba88', NULL, NULL, 0, 'ALD002IDR', 'ALDI JAYA', 'Mangga Dua Mall Lt. IV/A-106 jakarta 10730', '0216018430', '08888099312', 'Bambang'),
	('2018-08-15 17:47:02.807019', 'rimba88', '2018-08-31 17:19:29.719188', 'rimba88', 0, 'AST002IDR', 'PT. ASTRA HONDA MOTOR', 'Jl. Laksda Yos Sudarso – Sunter I Jakarta 14350, Indonesia Tel. 0811-9-500-989', '021-7252000', '021-7252000', 'ASTRA'),
	('2018-08-15 17:38:21.108955', 'rimba88', NULL, NULL, 0, 'AST007IDR', 'PT. ASTRA INTERNATIONAL TBK', 'Jl. Pangeran Jayakarta no 28', '021-65906060', '021-6522555', 'Eko'),
	('2018-08-15 17:00:31.272246', 'rimba88', NULL, NULL, 0, 'CHA001IDR', 'CV CHA-CHA KARYA', 'JLn Sultan Agung Prokyek Pasar Rumput', '021-8033870', '081288725559', 'Rudi'),
	('2018-08-15 17:08:39.503456', 'rimba88', NULL, NULL, 0, 'ERA004IDR', 'PT. ERAPOINT GLOBALINDO', 'Jl. KH. Hasyim Azhari No.125 Komp. Niaga Roxy Mas Blok D4/21-22 JakartaPusat 10150', '021-6322555', '082111188729', 'Debby Cintya Dewi'),
	('2018-08-15 16:50:03.851840', 'rimba88', '2018-08-31 17:19:36.046638', 'rimba88', 0, 'MUL016IDR', 'CV MULTI SKINDO UTAMA', 'Jln Pangeran Jayakarta No .77 /GATEP, (NO.HP Customer belum di input di accpac)', '021-659030', '0216491264', 'Himawan Setiadi'),
	('2018-08-31 16:06:39.188711', 'rimba88', NULL, NULL, 0, 'OT001', 'Mall', '- Untuk PO PO yang tidak ada supliernya', '000000', '00000', '-'),
	('2018-08-31 16:17:48.750403', 'rimba88', '2018-08-31 16:22:13.437793', 'rimba88', 0, 'OT002', 'Beli Online', '-', '0000000', '0000000', '-'),
	('2018-08-15 17:21:44.850050', 'rimba88', NULL, NULL, 0, 'PAR002USD', 'PT PARANTA ANUGERAH PRIMA', 'Wisma CORMIC Delta Building Blok A 4-7 l. Suryopranoto No. 1-9 Jakarta - 10160 Indonesia (No HP belum ada di isi sementara pakai no telp)', '021-3501188', '021-3501555', 'Fermin Setiawan'),
	('2018-08-31 16:26:10.595000', 'rimba88', NULL, NULL, 0, 'WID001IDR', 'Widepro, Toko', 'Poins square LT. 2 NO.41 H, Jln. R.A kartini no 41', '02175920177/78', '00000000', 'Iwan / Syamsul');
/*!40000 ALTER TABLE `n_a_supplier` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_sys_privilege: ~20 rows (approximately)
/*!40000 ALTER TABLE `n_a_sys_privilege` DISABLE KEYS */;
REPLACE INTO `n_a_sys_privilege` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `Permission`, `InActive`, `FK_PForm`, `User_id`) VALUES
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
/*!40000 ALTER TABLE `n_a_sys_privilege` ENABLE KEYS */;

-- Dumping data for table na_m_s.social_auth_association: ~0 rows (approximately)
/*!40000 ALTER TABLE `social_auth_association` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_association` ENABLE KEYS */;

-- Dumping data for table na_m_s.social_auth_code: ~0 rows (approximately)
/*!40000 ALTER TABLE `social_auth_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_code` ENABLE KEYS */;

-- Dumping data for table na_m_s.social_auth_nonce: ~0 rows (approximately)
/*!40000 ALTER TABLE `social_auth_nonce` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_nonce` ENABLE KEYS */;

-- Dumping data for table na_m_s.social_auth_partial: ~0 rows (approximately)
/*!40000 ALTER TABLE `social_auth_partial` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_partial` ENABLE KEYS */;

-- Dumping data for table na_m_s.social_auth_usersocialauth: ~0 rows (approximately)
/*!40000 ALTER TABLE `social_auth_usersocialauth` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_usersocialauth` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
