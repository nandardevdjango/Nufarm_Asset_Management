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
DELETE FROM `auth_group`;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;

-- Dumping data for table na_m_s.auth_group_permissions: ~0 rows (approximately)
DELETE FROM `auth_group_permissions`;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;

-- Dumping data for table na_m_s.auth_permission: ~102 rows (approximately)
DELETE FROM `auth_permission`;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
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
	(37, 'Can add na ga outwards', 13, 'add_nagaoutwards'),
	(38, 'Can change na ga outwards', 13, 'change_nagaoutwards'),
	(39, 'Can delete na ga outwards', 13, 'delete_nagaoutwards'),
	(40, 'Can add na ga receive', 14, 'add_nagareceive'),
	(41, 'Can change na ga receive', 14, 'change_nagareceive'),
	(42, 'Can delete na ga receive', 14, 'delete_nagareceive'),
	(43, 'Can add naga return', 15, 'add_nagareturn'),
	(44, 'Can change naga return', 15, 'change_nagareturn'),
	(45, 'Can delete naga return', 15, 'delete_nagareturn'),
	(46, 'Can add na ga vn history', 16, 'add_nagavnhistory'),
	(47, 'Can change na ga vn history', 16, 'change_nagavnhistory'),
	(48, 'Can delete na ga vn history', 16, 'delete_nagavnhistory'),
	(49, 'Can add na goods history', 17, 'add_nagoodshistory'),
	(50, 'Can change na goods history', 17, 'change_nagoodshistory'),
	(51, 'Can delete na goods history', 17, 'delete_nagoodshistory'),
	(52, 'Can add na goods lending', 18, 'add_nagoodslending'),
	(53, 'Can change na goods lending', 18, 'change_nagoodslending'),
	(54, 'Can delete na goods lending', 18, 'delete_nagoodslending'),
	(55, 'Can add na goods lost', 19, 'add_nagoodslost'),
	(56, 'Can change na goods lost', 19, 'change_nagoodslost'),
	(57, 'Can delete na goods lost', 19, 'delete_nagoodslost'),
	(58, 'Can add na goods outwards', 20, 'add_nagoodsoutwards'),
	(59, 'Can change na goods outwards', 20, 'change_nagoodsoutwards'),
	(60, 'Can delete na goods outwards', 20, 'delete_nagoodsoutwards'),
	(61, 'Can add na goods receive', 21, 'add_nagoodsreceive'),
	(62, 'Can change na goods receive', 21, 'change_nagoodsreceive'),
	(63, 'Can delete na goods receive', 21, 'delete_nagoodsreceive'),
	(64, 'Can add na goods receive_other', 22, 'add_nagoodsreceive_other'),
	(65, 'Can change na goods receive_other', 22, 'change_nagoodsreceive_other'),
	(66, 'Can delete na goods receive_other', 22, 'delete_nagoodsreceive_other'),
	(67, 'Can add na goods return', 23, 'add_nagoodsreturn'),
	(68, 'Can change na goods return', 23, 'change_nagoodsreturn'),
	(69, 'Can delete na goods return', 23, 'delete_nagoodsreturn'),
	(70, 'Can add na maintenance', 24, 'add_namaintenance'),
	(71, 'Can change na maintenance', 24, 'change_namaintenance'),
	(72, 'Can delete na maintenance', 24, 'delete_namaintenance'),
	(73, 'Can add na priviledge_form', 25, 'add_napriviledge_form'),
	(74, 'Can change na priviledge_form', 25, 'change_napriviledge_form'),
	(75, 'Can delete na priviledge_form', 25, 'delete_napriviledge_form'),
	(76, 'Can add na stock', 26, 'add_nastock'),
	(77, 'Can change na stock', 26, 'change_nastock'),
	(78, 'Can delete na stock', 26, 'delete_nastock'),
	(79, 'Can add na suplier', 27, 'add_nasuplier'),
	(80, 'Can change na suplier', 27, 'change_nasuplier'),
	(81, 'Can delete na suplier', 27, 'delete_nasuplier'),
	(82, 'Can add na sys priviledge', 28, 'add_nasyspriviledge'),
	(83, 'Can change na sys priviledge', 28, 'change_nasyspriviledge'),
	(84, 'Can delete na sys priviledge', 28, 'delete_nasyspriviledge'),
	(85, 'Can add na priviledge', 29, 'add_napriviledge'),
	(86, 'Can change na priviledge', 29, 'change_napriviledge'),
	(87, 'Can delete na priviledge', 29, 'delete_napriviledge'),
	(88, 'Can add log entry', 30, 'add_logentry'),
	(89, 'Can change log entry', 30, 'change_logentry'),
	(90, 'Can delete log entry', 30, 'delete_logentry'),
	(91, 'Can add permission', 31, 'add_permission'),
	(92, 'Can change permission', 31, 'change_permission'),
	(93, 'Can delete permission', 31, 'delete_permission'),
	(94, 'Can add group', 32, 'add_group'),
	(95, 'Can change group', 32, 'change_group'),
	(96, 'Can delete group', 32, 'delete_group'),
	(97, 'Can add content type', 33, 'add_contenttype'),
	(98, 'Can change content type', 33, 'change_contenttype'),
	(99, 'Can delete content type', 33, 'delete_contenttype'),
	(100, 'Can add session', 34, 'add_session'),
	(101, 'Can change session', 34, 'change_session'),
	(102, 'Can delete session', 34, 'delete_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;

-- Dumping data for table na_m_s.django_admin_log: ~1 rows (approximately)
DELETE FROM `django_admin_log`;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2018-07-29 18:42:49.836000', '8', 'Fix Asset Form', 1, '[{"added": {}}]', 25, 1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;

-- Dumping data for table na_m_s.django_content_type: ~34 rows (approximately)
DELETE FROM `django_content_type`;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(28, 'admin', 'logentry'),
	(30, 'auth', 'group'),
	(29, 'auth', 'permission'),
	(31, 'contenttypes', 'contenttype'),
	(6, 'NA_Models', 'employee'),
	(7, 'NA_Models', 'goods'),
	(8, 'NA_Models', 'logevent'),
	(10, 'NA_Models', 'naaccfa'),
	(11, 'NA_Models', 'naappparams'),
	(12, 'NA_Models', 'nadisposal'),
	(33, 'NA_Models', 'nagaoutwards'),
	(13, 'NA_Models', 'nagareceive'),
	(34, 'NA_Models', 'nagareturn'),
	(14, 'NA_Models', 'nagavnhistory'),
	(15, 'NA_Models', 'nagoodshistory'),
	(16, 'NA_Models', 'nagoodslending'),
	(17, 'NA_Models', 'nagoodslost'),
	(18, 'NA_Models', 'nagoodsoutwards'),
	(19, 'NA_Models', 'nagoodsreceive'),
	(20, 'NA_Models', 'nagoodsreceive_other'),
	(21, 'NA_Models', 'nagoodsreturn'),
	(22, 'NA_Models', 'namaintenance'),
	(27, 'NA_Models', 'napriviledge'),
	(23, 'NA_Models', 'napriviledge_form'),
	(24, 'NA_Models', 'nastock'),
	(25, 'NA_Models', 'nasuplier'),
	(26, 'NA_Models', 'nasyspriviledge'),
	(9, 'NA_Models', 'na_goodsreceive_detail'),
	(32, 'sessions', 'session'),
	(1, 'social_django', 'association'),
	(2, 'social_django', 'code'),
	(3, 'social_django', 'nonce'),
	(5, 'social_django', 'partial'),
	(4, 'social_django', 'usersocialauth');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;

-- Dumping data for table na_m_s.django_migrations: ~37 rows (approximately)
DELETE FROM `django_migrations`;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2018-07-08 22:21:38.908017'),
	(2, 'contenttypes', '0002_remove_content_type_name', '2018-07-08 22:21:39.330266'),
	(3, 'auth', '0001_initial', '2018-07-08 22:21:40.909845'),
	(4, 'auth', '0002_alter_permission_name_max_length', '2018-07-08 22:21:41.195197'),
	(5, 'auth', '0003_alter_user_email_max_length', '2018-07-08 22:21:41.248583'),
	(6, 'auth', '0004_alter_user_username_opts', '2018-07-08 22:21:41.279817'),
	(7, 'auth', '0005_alter_user_last_login_null', '2018-07-08 22:21:41.311169'),
	(8, 'auth', '0006_require_contenttypes_0002', '2018-07-08 22:21:41.348285'),
	(9, 'auth', '0007_alter_validators_add_error_messages', '2018-07-08 22:21:41.395242'),
	(10, 'auth', '0008_alter_user_username_max_length', '2018-07-08 22:21:41.433134'),
	(11, 'NA_Models', '0001_initial', '2018-07-08 22:21:59.685919'),
	(12, 'admin', '0001_initial', '2018-07-08 22:22:00.672146'),
	(13, 'admin', '0002_logentry_remove_auto_add', '2018-07-08 22:22:00.719020'),
	(14, 'sessions', '0001_initial', '2018-07-08 22:22:01.035105'),
	(15, 'default', '0001_initial', '2018-07-08 22:22:02.373933'),
	(16, 'social_auth', '0001_initial', '2018-07-08 22:22:02.420801'),
	(17, 'default', '0002_add_related_name', '2018-07-08 22:22:02.774067'),
	(18, 'social_auth', '0002_add_related_name', '2018-07-08 22:22:02.820954'),
	(19, 'default', '0003_alter_email_max_length', '2018-07-08 22:22:03.089601'),
	(20, 'social_auth', '0003_alter_email_max_length', '2018-07-08 22:22:03.120863'),
	(21, 'default', '0004_auto_20160423_0400', '2018-07-08 22:22:03.221419'),
	(22, 'social_auth', '0004_auto_20160423_0400', '2018-07-08 22:22:03.259066'),
	(23, 'social_auth', '0005_auto_20160727_2333', '2018-07-08 22:22:03.391054'),
	(24, 'social_django', '0006_partial', '2018-07-08 22:22:03.659611'),
	(25, 'social_django', '0007_code_timestamp', '2018-07-08 22:22:04.006670'),
	(26, 'social_django', '0008_partial_timestamp', '2018-07-08 22:22:04.290840'),
	(27, 'social_django', '0003_alter_email_max_length', '2018-07-08 22:22:04.337738'),
	(28, 'social_django', '0005_auto_20160727_2333', '2018-07-08 22:22:04.407266'),
	(29, 'social_django', '0002_add_related_name', '2018-07-08 22:22:04.454670'),
	(30, 'social_django', '0004_auto_20160423_0400', '2018-07-08 22:22:04.475975'),
	(31, 'social_django', '0001_initial', '2018-07-08 22:22:04.522834'),
	(32, 'NA_Models', '0002_auto_20180710_2239', '2018-07-10 22:40:01.557742'),
	(33, 'NA_Models', '0003_auto_20180714_1451', '2018-07-18 10:21:48.057779'),
	(34, 'NA_Models', '0004_auto_20180718_0954', '2018-07-18 10:28:05.932586'),
	(35, 'NA_Models', '0005_auto_20180719_1051', '2018-07-19 11:02:40.247598'),
	(36, 'NA_Models', '0005_auto_20180719_1117', '2018-07-19 11:18:09.932672'),
	(37, 'NA_Models', '0002_naaccfa_is_parent', '2018-07-25 14:44:44.867695');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;

-- Dumping data for table na_m_s.django_session: ~7 rows (approximately)
DELETE FROM `django_session`;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('4smkhb6s9g3co7i9m9r4pmguzvcswh2d', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-07-22 22:43:49.085896'),
	('775lo3x9wsokqi8r4qx5xz1296u8zxg7', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-08-21 19:21:51.317133'),
	('9yxz8d0s6du2pnx6jwcr3n114kc6rkwx', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-08-28 19:13:18.579303'),
	('obqjsmh8deccxvyb6l9tj26eyjp9mqfx', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-08-07 17:07:30.005363'),
	('ojwa5k07dj3ldld811smujxvxl1bzl56', 'N2I1OWUyMThhNzJhN2I3ZDMzZWRjYTYyZGU3NWYxZjEzYzZmODc2Nzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwYWM3YTJmMGFmNjMwNDg4MGIzNDVlYmExMDYwNTY1NmJkOWRiNzQyIn0=', '2018-08-07 22:07:21.378000'),
	('s5ks3lch8odtt94dyz7hd2zzjwqea6wd', 'N2I1OWUyMThhNzJhN2I3ZDMzZWRjYTYyZGU3NWYxZjEzYzZmODc2Nzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwYWM3YTJmMGFmNjMwNDg4MGIzNDVlYmExMDYwNTY1NmJkOWRiNzQyIn0=', '2018-08-06 22:32:34.274000'),
	('wo4rqimlfz8wr2uxw8v9q4uq36vl0w32', 'N2I1OWUyMThhNzJhN2I3ZDMzZWRjYTYyZGU3NWYxZjEzYzZmODc2Nzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwYWM3YTJmMGFmNjMwNDg4MGIzNDVlYmExMDYwNTY1NmJkOWRiNzQyIn0=', '2018-08-12 19:48:15.585000');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;

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
INSERT INTO `logevent` (`IDApp`, `CreatedDate`, `CreatedBy`, `NameApp`, `descriptions`) VALUES
	(1, '2018-05-05 20:39:49.000000', 'Admin', 'Deleted Suplier', '{"deleted": ["AF122FHJ", "Rimba P", "Cimahi", "0221122331144", "0895322085649", "Mang Nandar", 1, "2018-01-06", "admin"]}'),
	(2, '2018-05-05 20:47:28.000000', 'rimba47prayoga', 'Deleted Suplier', '{"deleted": ["AF122uui", "Rimba", "Cimahi", "0221122331144", "0895322085649", "Mang Nandar", 0, "2018-01-01", "admin"]}'),
	(3, '2018-05-10 19:20:55.000000', 'rimba47prayoga', 'Deleted Suplier', '{"deleted": ["AF122fg", "Rimba", "Cimahi", "0221122331144", "0895322085649", "Mang Nandar", 0, "2018-01-01", "admin"]}'),
	(4, '2018-05-13 12:54:16.000000', 'rimba47prayoga', 'Deleted Suplier', '{"deleted": ["AF343534", "Teja", "Unknown", "0898985968", "0875764786545", "Rimba", 1, "2018-05-13", "rimba47prayoga"]}'),
	(5, '2018-05-24 22:13:40.000000', 'rimba47prayoga', 'Deleted Suplier', '{"deleted": ["AF1229", "Rimba", "Cimahi", "0221122331144", "0895322085649", "Mang Nandar", 0, "2018-01-01", "admin"]}'),
	(6, '2018-05-27 21:28:08.000000', 'rimba47prayoga', 'Deleted Employee', '{"C": "C", "M": "S", "Descriptions": "rimba47prayoga", "0895322085649": "Cimahi", "011247487875411": "Rimba"}'),
	(7, '2018-06-23 18:02:21.000000', 'admin', 'Deleted Employee', '{"deleted": ["00111234887898", "Rimba", "C", "C", "M", "S", "08984512313574", "Cimahi", "Employee", "27 January 2018 00:00:00", "rimba47prayoga"]}'),
	(8, '2018-06-23 18:05:27.000000', 'admin', 'Deleted Employee', '{"deleted": ["1121246345", "Rimba P", "P", "P", "M", "M", "0895322085649", "Citeureup", "There\'s No Descriptions", 0, "28 January 2018 00:00:00", "rimba47prayoga"]}'),
	(9, '2018-06-23 18:05:59.000000', 'admin', 'Deleted Suplier', '{"deleted": ["AF1223", "Rimba", "Cimahi", "0221122331144", "0895322085649", "Mang Nandar", 0, "06 January 2018 00:00:00", "admin"]}'),
	(10, '2018-06-23 18:06:06.000000', 'admin', 'Deleted Suplier', '{"deleted": ["AD3323", "Teja", "Unknown", "0223544464", "0223544464", "Rimba", 1, "13 May 2018 00:00:00", "rimba47prayoga"]}'),
	(11, '2018-06-23 18:31:19.000000', 'admin', 'Deleted Employee', '{"deleted": ["11223445", "Rimba P", "K", "K", "M", "S", "08953320215121", "Cisurupan", "There\'s No Descriptions", 1, "25 January 2018 00:00:00", "rimba47prayoga"]}'),
	(12, '2018-08-16 16:46:39.068477', 'rimba88', 'Deleted Goods', '{"deleted": ["it-008", "EKSTERNAL HARDISK", "SEAGATE", "0.0000", "SL", "Pcs", "5.00", "Gudang IT", "Price tidak di input di sini", 0, "16 August 2018 00:00:00", "rimba88", null, null]}'),
	(13, '2018-08-16 17:22:11.039349', 'rimba88', 'Deleted Goods', '{"deleted": ["it-008", "EKSTERNAL HARDISK", "SEAGATE", "0.0000", "SL", "Pcs", "5.00", "Gudang IT", "Price tidak di input di sini", 0, "16 August 2018 00:00:00", "rimba88", null, null]}'),
	(14, '2018-08-16 18:16:15.616851', 'rimba88', 'Deleted Goods', '{"deleted": ["GA_003", "HP High End", "SAMSUNG", "0.0000", "SL", "Unit", "5.00", "Gudang IT", "untuk HP yang mempunyai nila tinggi di masukan dalam FA GA", 0, "16 August 2018 00:00:00", "rimba88", null, null]}');
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
INSERT INTO `n_a_goods_receive` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `DateReceived`, `TotalPurchase`, `TotalReceived`, `Descriptions`, `DescBySystem`, `REFNO`, `FK_Suplier`, `fk_goods`, `FK_P_R_By`, `FK_ReceivedBy`) VALUES
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

-- Dumping data for table na_m_s.n_a_priviledge: ~1 rows (approximately)
DELETE FROM `n_a_priviledge`;
/*!40000 ALTER TABLE `n_a_priviledge` DISABLE KEYS */;
INSERT INTO `n_a_priviledge` (`IDApp`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `first_name`, `last_name`, `UserName`, `Email`, `Divisi`, `Password`, `Picture`, `Last_login`, `Last_form`, `Computer_Name`, `IP_Address`, `Role`, `Is_SuperUser`, `Is_Staff`, `Is_Active`, `Date_Joined`) VALUES
	(1, '', NULL, NULL, '', '', 'rimba88', 'rimba@88spares.com', 'IT', 'pbkdf2_sha256$36000$vACo7Q3KBjS5$UOEFP68Os1qQVdFh5PlbOOC8WpFufG8MGnrtP/pXQKA=', 'dir_for_rimba88\\20180515_100310.jpg', '2018-08-14 19:13:18.553285', NULL, '', '', 1, 1, 0, 1, NULL);
/*!40000 ALTER TABLE `n_a_priviledge` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_priviledge_form: ~6 rows (approximately)
DELETE FROM `n_a_priviledge_form`;
/*!40000 ALTER TABLE `n_a_priviledge_form` DISABLE KEYS */;
INSERT INTO `n_a_priviledge_form` (`IDApp`, `Form_id`, `Form_name`, `Form_name_ori`) VALUES
	(1, '0001M', 'Suplier Form', 'n_a_suplier'),
	(2, '0002M', 'Employee Form', 'employee'),
	(3, '0003M', 'Goods Form', 'goods'),
	(6, '0001T', 'Goods Receive', 'n_a_goods_receive'),
	(7, '0004M', 'User Priviledge', 'n_a_priviledge'),
	(8, '0001O', 'Fix Asset Form', 'n_a_acc_fa');
/*!40000 ALTER TABLE `n_a_priviledge_form` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_priviledge_groups: ~0 rows (approximately)
DELETE FROM `n_a_priviledge_groups`;
/*!40000 ALTER TABLE `n_a_priviledge_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_priviledge_groups` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_priviledge_user_permissions: ~0 rows (approximately)
DELETE FROM `n_a_priviledge_user_permissions`;
/*!40000 ALTER TABLE `n_a_priviledge_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_priviledge_user_permissions` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_stock: ~0 rows (approximately)
DELETE FROM `n_a_stock`;
/*!40000 ALTER TABLE `n_a_stock` DISABLE KEYS */;
INSERT INTO `n_a_stock` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `T_Goods_Spare`, `TotalQty`, `TIsUsed`, `TIsNew`, `TIsRenew`, `TIsBroken`, `TGoods_Return`, `TGoods_Received`, `TDisposal`, `TIsLost`, `TMaintenance`, `FK_Goods`) VALUES
	(1, '2018-08-21 17:04:53.000000', 'rimba88', NULL, NULL, 0, NULL, 0, 8, 0, NULL, 0, 8, NULL, NULL, 0, 00000000003);
/*!40000 ALTER TABLE `n_a_stock` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_suplier: ~7 rows (approximately)
DELETE FROM `n_a_suplier`;
/*!40000 ALTER TABLE `n_a_suplier` DISABLE KEYS */;
INSERT INTO `n_a_suplier` (`CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `InActive`, `SuplierCode`, `SuplierName`, `Address`, `Telp`, `HP`, `ContactPerson`) VALUES
	('2018-08-20 18:53:37.355965', 'rimba88', NULL, NULL, 0, 'ALD002IDR', 'ALDI JAYA', 'Mangga Dua Mall Lt. IV/A-106 jakarta 10730', '0216018430', '08888099312', 'Bambang'),
	('2018-08-15 17:47:02.807019', 'rimba88', '2018-08-15 17:47:17.653669', 'rimba88', 1, 'AST002IDR', 'PT. ASTRA HONDA MOTOR', 'Jl. Laksda Yos Sudarso – Sunter I Jakarta 14350, Indonesia Tel. 0811-9-500-989', '021-7252000', '021-7252000', 'ASTRA'),
	('2018-08-15 17:38:21.108955', 'rimba88', NULL, NULL, 0, 'AST007IDR', 'PT. ASTRA INTERNATIONAL TBK', 'Jl. Pangeran Jayakarta no 28', '021-65906060', '021-6522555', 'Eko'),
	('2018-08-15 17:00:31.272246', 'rimba88', NULL, NULL, 0, 'CHA001IDR', 'CV CHA-CHA KARYA', 'JLn Sultan Agung Prokyek Pasar Rumput', '021-8033870', '081288725559', 'Rudi'),
	('2018-08-15 17:08:39.503456', 'rimba88', NULL, NULL, 0, 'ERA004IDR', 'PT. ERAPOINT GLOBALINDO', 'Jl. KH. Hasyim Azhari No.125 Komp. Niaga Roxy Mas Blok D4/21-22 JakartaPusat 10150', '021-6322555', '082111188729', 'Debby Cintya Dewi'),
	('2018-08-15 16:50:03.851840', 'rimba88', '2018-08-15 17:09:32.926966', 'rimba88', 1, 'MUL016IDR', 'CV MULTI SKINDO UTAMA', 'Jln Pangeran Jayakarta No .77 /GATEP, (NO.HP Customer belum di input di accpac)', '021-659030', '0216491264', 'Himawan Setiadi'),
	('2018-08-15 17:21:44.850050', 'rimba88', NULL, NULL, 0, 'PAR002USD', 'PT PARANTA ANUGERAH PRIMA', 'Wisma CORMIC Delta Building Blok A 4-7 l. Suryopranoto No. 1-9 Jakarta - 10160 Indonesia (No HP belum ada di isi sementara pakai no telp)', '021-3501188', '021-3501555', 'Fermin Setiawan');
/*!40000 ALTER TABLE `n_a_suplier` ENABLE KEYS */;

-- Dumping data for table na_m_s.n_a_sys_priviledge: ~16 rows (approximately)
DELETE FROM `n_a_sys_priviledge`;
/*!40000 ALTER TABLE `n_a_sys_priviledge` DISABLE KEYS */;
INSERT INTO `n_a_sys_priviledge` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `Permission`, `InActive`, `FK_PForm`, `User_id`) VALUES
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
	(16, '2018-07-08 22:28:25.668736', '', NULL, NULL, 'Allow Delete', 0, 7, 1);
/*!40000 ALTER TABLE `n_a_sys_priviledge` ENABLE KEYS */;

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
