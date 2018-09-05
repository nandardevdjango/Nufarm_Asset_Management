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

-- Dumping data for table na_m_s_old.auth_group: ~0 rows (approximately)
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.auth_group_permissions: ~0 rows (approximately)
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;



-- Dumping data for table na_m_s_old.django_admin_log: ~1 rows (approximately)
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2018-07-29 18:42:49.836000', '8', 'Fix Asset Form', 1, '[{"added": {}}]', 25, 1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.django_content_type: ~40 rows (approximately)
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
	(35, 'NA_Models', 'nagamaintenance'),
	(33, 'NA_Models', 'nagaoutwards'),
	(13, 'NA_Models', 'nagareceive'),
	(34, 'NA_Models', 'nagareturn'),
	(14, 'NA_Models', 'nagavnhistory'),
	(36, 'NA_Models', 'nagoodsequipment'),
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
	(40, 'NA_Models', 'naprivilege'),
	(37, 'NA_Models', 'naprivilege_form'),
	(24, 'NA_Models', 'nastock'),
	(25, 'NA_Models', 'nasuplier'),
	(38, 'NA_Models', 'nasupplier'),
	(26, 'NA_Models', 'nasyspriviledge'),
	(39, 'NA_Models', 'nasysprivilege'),
	(9, 'NA_Models', 'na_goodsreceive_detail'),
	(32, 'sessions', 'session'),
	(1, 'social_django', 'association'),
	(2, 'social_django', 'code'),
	(3, 'social_django', 'nonce'),
	(5, 'social_django', 'partial'),
	(4, 'social_django', 'usersocialauth');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.django_migrations: ~37 rows (approximately)
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

-- Dumping data for table na_m_s_old.django_session: ~8 rows (approximately)
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('4smkhb6s9g3co7i9m9r4pmguzvcswh2d', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-07-22 22:43:49.085896'),
	('775lo3x9wsokqi8r4qx5xz1296u8zxg7', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-08-21 19:21:51.317133'),
	('9yxz8d0s6du2pnx6jwcr3n114kc6rkwx', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-08-28 19:13:18.579303'),
	('obqjsmh8deccxvyb6l9tj26eyjp9mqfx', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-08-07 17:07:30.005363'),
	('ojwa5k07dj3ldld811smujxvxl1bzl56', 'N2I1OWUyMThhNzJhN2I3ZDMzZWRjYTYyZGU3NWYxZjEzYzZmODc2Nzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwYWM3YTJmMGFmNjMwNDg4MGIzNDVlYmExMDYwNTY1NmJkOWRiNzQyIn0=', '2018-08-07 22:07:21.378000'),
	('q7g44p2rbzp1ngswptg2ojv4dlj1mnrt', 'Y2JhMWU1OGFjODgyOTAzNTY1ZjA2M2RlMDMyZDlmYTdmMmVhYzg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNmQyYWQwNWYyYzc5NGM3ZjYxOTk3ZjZhODU3MTI5YjcwODJkYWY0In0=', '2018-09-12 11:55:12.464925'),
	('s5ks3lch8odtt94dyz7hd2zzjwqea6wd', 'N2I1OWUyMThhNzJhN2I3ZDMzZWRjYTYyZGU3NWYxZjEzYzZmODc2Nzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwYWM3YTJmMGFmNjMwNDg4MGIzNDVlYmExMDYwNTY1NmJkOWRiNzQyIn0=', '2018-08-06 22:32:34.274000'),
	('wo4rqimlfz8wr2uxw8v9q4uq36vl0w32', 'N2I1OWUyMThhNzJhN2I3ZDMzZWRjYTYyZGU3NWYxZjEzYzZmODc2Nzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwYWM3YTJmMGFmNjMwNDg4MGIzNDVlYmExMDYwNTY1NmJkOWRiNzQyIn0=', '2018-08-12 19:48:15.585000');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.employee: ~9 rows (approximately)
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

-- Dumping data for table na_m_s_old.logevent: ~14 rows (approximately)
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

-- Dumping data for table na_m_s_old.n_a_acc_fa: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_acc_fa` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_acc_fa` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_appparams: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_appparams` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_appparams` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_disposal: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_disposal` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_disposal` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_ga_maintenance: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_ga_maintenance` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_maintenance` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_ga_outwards: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_ga_outwards` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_outwards` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_ga_receive: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_ga_receive` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_receive` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_ga_return: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_ga_return` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_return` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_ga_vn_history: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_ga_vn_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_vn_history` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_goods: ~26 rows (approximately)
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

-- Dumping data for table na_m_s_old.n_a_goods_history: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_history` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_goods_lending: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_lending` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_lending` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_goods_lost: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_lost` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_lost` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_goods_outwards: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_outwards` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_outwards` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_goods_receive: ~4 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_receive` DISABLE KEYS */;
INSERT INTO `n_a_goods_receive` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `DateReceived`, `TotalPurchase`, `TotalReceived`, `Descriptions`, `DescBySystem`, `REFNO`, `FK_Supplier`, `fk_goods`, `FK_P_R_By`, `FK_ReceivedBy`) VALUES
	(1, '2018-08-21 00:00:00.000000', 'rimba88', NULL, NULL, '2016-03-04 00:00:00.000000', 8, 8, 'Pembelian HP J5 tahap pertama untuk IT dan marketing, dan IConcept dan kepentingan FMS lainnya', '(SAMSUNG, Type : J5, SN : 357005072234246-357004072234249, SAMSUNG, Type : J5, SN : 357004071145081-357005071145088, SAMSUNG, Type : J5, SN : 357005071145054-357004071145057, SAMSUNG, Type : J5, SN : 357004071145024-357005071145021, SAMSUNG, Type : J5, SN : 357004071144027-357005071144024, SAMSUNG, Type : J5, SN : 357004072234249-357005072234246, SAMSUNG, Type : J5, SN : 357004071145115-357004071145115, SAMSUNG, Type : J5, SN : ICONCEPT)', '15/16-000128-01', 'ERA004IDR', 3, 8, 9),
	(2, '2018-08-28 00:00:00.000000', 'nandar', NULL, NULL, '2015-07-30 00:00:00.000000', 6, 6, '', '(DELL, Type : LATITUDE E5440, SN : 7SOGWZ1/0001402, DELL, Type : LATITUDE E5440, SN : 3L4Z062/0001403, DELL, Type : LATITUDE E5440, SN :  3S30l32/0001404, DELL, Type : LATITUDE E5440, SN : HHS2F12/0001405, DELL, Type : LATITUDE E5440, SN : 1V1GWZ1/0001406, DELL, Type : LATITUDE E5440, SN : 3K65P12/0001407)', '14/15-000141-01', 'PAR002USD', 2, 8, 9),
	(3, '2018-08-30 00:00:00.000000', 'rimba88', NULL, NULL, '2015-05-07 00:00:00.000000', 10, 10, '', '(DELL, Type : Latitude E5450, SN : G1KFN32/0001385, DELL, Type : Latitude E5450, SN : 81NZFRF2/0001386, DELL, Type : Latitude E5450, SN : 3HSJN32/0001387, DELL, Type : Latitude E5450, SN : F6JHN32/0001388, DELL, Type : Latitude E5450, SN : 8VT2F12/0001389, DELL, Type : Latitude E5450, SN : 6HSJN32/0001390, DELL, Type : Latitude E5450, SN : G1KFN32/0001391, DELL, Type : Latitude E5450, SN : 4T2WR32/0001392, DELL, Type : Latitude E5450, SN : F03WR32/0001393, DELL, Type : Latitude E5450, SN : G1KFN32/0001395)', '14/15-000186-01', 'PAR002USD', 2, 8, 9),
	(4, '2018-08-31 00:00:00.000000', 'rimba88', NULL, NULL, '2017-07-06 00:00:00.000000', 6, 6, '', '(NEC, Type : VE 303 G, SN : 6Y41310CD/0001561, NEC, Type : VE 303 G, SN : 6X41082CD/0001562, NEC, Type : VE 303 G, SN : 6Y41296CD/0001563, NEC, Type : VE 303 G, SN : GX41075CD/0001564, NEC, Type : VE 303 G, SN : GX41127CD/0001565, NEC, Type : VE 303 G, SN : 0001566/RMeeting)', '16/17-000183-01', 'WID001IDR', 4, 5, 6);
/*!40000 ALTER TABLE `n_a_goods_receive` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_goods_receive_detail: ~30 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_receive_detail` DISABLE KEYS */;
INSERT INTO `n_a_goods_receive_detail` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `BrandName`, `PricePerUnit`, `TypeApp`, `Warranty`, `EndOfWarranty`, `SerialNumber`, `FK_App`) VALUES
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
	(15, '2018-08-30 00:00:00.000000', 'rimba88', NULL, NULL, 'DELL', 14585625.0000, 'Latitude E5450', 5.00, '2020-05-05 00:00:00.000000', 'G1KFN32/0001385', 3),
	(16, '2018-08-30 00:00:00.000000', 'rimba88', NULL, NULL, 'DELL', 14585625.0000, 'Latitude E5450', 5.00, '2020-05-05 00:00:00.000000', '81NZFRF2/0001386', 3),
	(17, '2018-08-30 00:00:00.000000', 'rimba88', NULL, NULL, 'DELL', 14585625.0000, 'Latitude E5450', 5.00, '2020-05-05 00:00:00.000000', '3HSJN32/0001387', 3),
	(18, '2018-08-30 00:00:00.000000', 'rimba88', NULL, NULL, 'DELL', 14585625.0000, 'Latitude E5450', 5.00, '2020-05-05 00:00:00.000000', 'F6JHN32/0001388', 3),
	(19, '2018-08-30 00:00:00.000000', 'rimba88', NULL, NULL, 'DELL', 14585625.0000, 'Latitude E5450', 5.00, '2020-05-05 00:00:00.000000', '8VT2F12/0001389', 3),
	(20, '2018-08-30 00:00:00.000000', 'rimba88', NULL, NULL, 'DELL', 14585625.0000, 'Latitude E5450', 5.00, '2020-05-05 00:00:00.000000', '6HSJN32/0001390', 3),
	(21, '2018-08-30 00:00:00.000000', 'rimba88', NULL, NULL, 'DELL', 14585625.0000, 'Latitude E5450', 5.00, '2020-05-05 00:00:00.000000', 'G1KFN32/0001391', 3),
	(22, '2018-08-30 00:00:00.000000', 'rimba88', NULL, NULL, 'DELL', 14585625.0000, 'Latitude E5450', 5.00, '2020-05-05 00:00:00.000000', '4T2WR32/0001392', 3),
	(23, '2018-08-30 00:00:00.000000', 'rimba88', NULL, NULL, 'DELL', 14585625.0000, 'Latitude E5450', 5.00, '2020-05-05 00:00:00.000000', 'F03WR32/0001393', 3),
	(24, '2018-08-30 00:00:00.000000', 'rimba88', NULL, NULL, 'DELL', 14585625.0000, 'Latitude E5450', 5.00, '2020-05-05 00:00:00.000000', 'G1KFN32/0001395', 3),
	(25, '2018-08-31 00:00:00.000000', 'rimba88', '2018-09-03 00:00:00.000000', 'rimba88', 'NEC', 4400000.0000, 'VE 303 G', 1.00, '2018-07-06 00:00:00.000000', '6Y41310CD/0001561', 4),
	(26, '2018-08-31 00:00:00.000000', 'rimba88', '2018-09-03 00:00:00.000000', 'rimba88', 'NEC', 4400000.0000, 'VE 303 G', 1.00, '2018-07-06 00:00:00.000000', '6X41082CD/0001562', 4),
	(27, '2018-08-31 00:00:00.000000', 'rimba88', '2018-09-03 00:00:00.000000', 'rimba88', 'NEC', 4400000.0000, 'VE 303 G', 1.00, '2018-07-06 00:00:00.000000', '6Y41296CD/0001563', 4),
	(28, '2018-08-31 00:00:00.000000', 'rimba88', '2018-09-03 00:00:00.000000', 'rimba88', 'NEC', 4400000.0000, 'VE 303 G', 1.00, '2018-07-06 00:00:00.000000', 'GX41075CD/0001564', 4),
	(29, '2018-08-31 00:00:00.000000', 'rimba88', '2018-09-03 00:00:00.000000', 'rimba88', 'NEC', 4400000.0000, 'VE 303 G', 1.00, '2018-07-06 00:00:00.000000', 'GX41127CD/0001565', 4),
	(30, '2018-08-31 00:00:00.000000', 'rimba88', '2018-09-03 00:00:00.000000', 'rimba88', 'NEC', 4400000.0000, 'VE 303 G', 1.00, '2018-07-06 00:00:00.000000', '0001566/RM', 4);
/*!40000 ALTER TABLE `n_a_goods_receive_detail` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_goods_receive_other: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_receive_other` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_receive_other` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_goods_return: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_goods_return` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_return` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_maintenance: ~0 rows (approximately)
/*!40000 ALTER TABLE `n_a_maintenance` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_maintenance` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_stock: ~3 rows (approximately)
/*!40000 ALTER TABLE `n_a_stock` DISABLE KEYS */;
INSERT INTO `n_a_stock` (`IDApp`, `CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `T_Goods_Spare`, `TotalQty`, `TIsUsed`, `TIsNew`, `TIsRenew`, `TIsBroken`, `TGoods_Return`, `TGoods_Received`, `TDisposal`, `TIsLost`, `TMaintenance`, `FK_Goods`) VALUES
	(1, '2018-08-21 17:04:53.000000', 'rimba88', NULL, NULL, 0, NULL, 0, 8, 0, NULL, 0, 8, NULL, NULL, 0, 00000000003),
	(2, '2018-08-28 23:21:55.000000', 'nandar', '2018-08-30 19:44:09.000000', 'rimba88', 0, NULL, 0, 16, 0, NULL, 0, 16, NULL, NULL, 0, 00000000002),
	(3, '2018-08-31 16:55:32.000000', 'rimba88', '2018-09-03 15:36:53.000000', 'rimba88', 0, NULL, 0, 6, 0, NULL, 0, 6, NULL, NULL, 0, 00000000004);
/*!40000 ALTER TABLE `n_a_stock` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.n_a_suplier: ~10 rows (approximately)
/*!40000 ALTER TABLE `n_a_suplier` DISABLE KEYS */;
INSERT INTO `n_a_supplier` (`CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `InActive`, `SupplierCode`, `SupplierName`, `Address`, `Telp`, `HP`, `ContactPerson`) VALUES
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
/*!40000 ALTER TABLE `n_a_suplier` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.social_auth_association: ~0 rows (approximately)
/*!40000 ALTER TABLE `social_auth_association` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_association` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.social_auth_code: ~0 rows (approximately)
/*!40000 ALTER TABLE `social_auth_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_code` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.social_auth_nonce: ~0 rows (approximately)
/*!40000 ALTER TABLE `social_auth_nonce` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_nonce` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.social_auth_partial: ~0 rows (approximately)
/*!40000 ALTER TABLE `social_auth_partial` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_partial` ENABLE KEYS */;

-- Dumping data for table na_m_s_old.social_auth_usersocialauth: ~0 rows (approximately)
/*!40000 ALTER TABLE `social_auth_usersocialauth` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_usersocialauth` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
