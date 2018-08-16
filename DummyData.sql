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

-- Dumping structure for table na_m_s.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.auth_group: ~0 rows (approximately)
DELETE FROM `auth_group`;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;

-- Dumping structure for table na_m_s.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.auth_group_permissions: ~0 rows (approximately)
DELETE FROM `auth_group_permissions`;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;

-- Dumping structure for table na_m_s.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

-- Dumping structure for table na_m_s.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_N_A_Priviledge_IDApp` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_N_A_Priviledge_IDApp` FOREIGN KEY (`user_id`) REFERENCES `n_a_priviledge` (`IDApp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.django_admin_log: ~1 rows (approximately)
DELETE FROM `django_admin_log`;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2018-07-29 18:42:49.836000', '8', 'Fix Asset Form', 1, '[{"added": {}}]', 25, 1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;

-- Dumping structure for table na_m_s.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

-- Dumping structure for table na_m_s.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

-- Dumping structure for table na_m_s.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

-- Dumping structure for table na_m_s.employee
CREATE TABLE IF NOT EXISTS `employee` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `TypeApp` varchar(32) NOT NULL,
  `InActive` smallint(5) unsigned NOT NULL,
  `Descriptions` varchar(250) DEFAULT NULL,
  `NIK` varchar(50) NOT NULL,
  `Employee_Name` varchar(150) DEFAULT NULL,
  `JobType` varchar(150) DEFAULT NULL,
  `Gender` varchar(1) NOT NULL,
  `Status` varchar(1) NOT NULL,
  `TelpHP` varchar(20) DEFAULT NULL,
  `Territory` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`IDApp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.employee: ~0 rows (approximately)
DELETE FROM `employee`;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;

-- Dumping structure for table na_m_s.logevent
CREATE TABLE IF NOT EXISTS `logevent` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `NameApp` varchar(30) NOT NULL,
  `descriptions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`IDApp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.logevent: ~12 rows (approximately)
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

-- Dumping structure for table na_m_s.n_a_acc_fa
CREATE TABLE IF NOT EXISTS `n_a_acc_fa` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `SerialNumber` varchar(50) NOT NULL,
  `TypeApp` varchar(32) NOT NULL,
  `Year` decimal(10,2) NOT NULL,
  `StartDate` date NOT NULL,
  `Depr_Expense` decimal(30,4) DEFAULT NULL,
  `Depr_Accumulation` decimal(30,4) DEFAULT NULL,
  `BookValue` decimal(30,4) DEFAULT NULL,
  `LastUpdated` datetime(6) DEFAULT NULL,
  `FK_Goods` int(11) NOT NULL,
  `DateDepreciation` date DEFAULT NULL,
  `IsParent` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`IDApp`),
  KEY `n_a_acc_fa_FK_Goods_33d15428` (`FK_Goods`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_acc_fa: ~0 rows (approximately)
DELETE FROM `n_a_acc_fa`;
/*!40000 ALTER TABLE `n_a_acc_fa` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_acc_fa` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_appparams
CREATE TABLE IF NOT EXISTS `n_a_appparams` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CodeApp` varchar(64) NOT NULL,
  `NameApp` varchar(100) DEFAULT NULL,
  `TypeApp` varchar(64) DEFAULT NULL,
  `StartDate` date DEFAULT NULL,
  `EndDate` date DEFAULT NULL,
  `ValueChar` varchar(50) DEFAULT NULL,
  `FKIDApp` smallint(6) DEFAULT NULL,
  `FKCodeApp` varchar(64) DEFAULT NULL,
  `AttStrParams` varchar(20) DEFAULT NULL,
  `AttDecParams` decimal(10,3) DEFAULT NULL,
  `ValueStrParams` varchar(50) DEFAULT NULL,
  `ValueDecParams` decimal(10,3) DEFAULT NULL,
  `InActive` int(11) NOT NULL,
  `CreatedDate` datetime(6) DEFAULT NULL,
  `CreatedBy` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`IDApp`),
  UNIQUE KEY `n_a_appparams_IDApp_CodeApp_98a14be1_uniq` (`IDApp`,`CodeApp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_appparams: ~0 rows (approximately)
DELETE FROM `n_a_appparams`;
/*!40000 ALTER TABLE `n_a_appparams` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_appparams` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_disposal
CREATE TABLE IF NOT EXISTS `n_a_disposal` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` varchar(50) DEFAULT NULL,
  `TypeApp` varchar(32) NOT NULL,
  `SerialNumber` varchar(100) NOT NULL,
  `DateDisposal` date NOT NULL,
  `IsLost` tinyint(1) DEFAULT NULL,
  `IsSold` smallint(5) unsigned DEFAULT NULL,
  `SellingPrice` decimal(10,4) DEFAULT NULL,
  `Sold_To` char(1) DEFAULT NULL,
  `FK_Sold_To_Employee` int(11) DEFAULT NULL COMMENT 'di jual ke karyawan mana kalau ke orang lain isinya dbnull',
  `Sold_To_P_Other` varchar(120) DEFAULT NULL COMMENT 'di jual ke siapa bila bukan karyaawan, ke perusahaan atau perorangan',
  `FK_ProposedBy` int(11) DEFAULT NULL COMMENT 'Diajukan/Penanggung jawab',
  `FK_Acc_FA` int(11) DEFAULT NULL,
  `FK_Stock` int(11) DEFAULT NULL,
  `BookValue` decimal(10,4) NOT NULL,
  `FK_Usedemployee` int(11) DEFAULT NULL,
  `FK_Goods` int(11) NOT NULL,
  `FK_Maintenance` int(11) DEFAULT NULL,
  `FK_Lending` int(11) DEFAULT NULL,
  `FK_Outwards` int(11) DEFAULT NULL,
  `FK_Return` int(11) DEFAULT NULL,
  `FK_Lost` int(11) DEFAULT NULL,
  `FK_Acknowledge1` int(11) DEFAULT NULL COMMENT 'Diketahui sama siapa',
  `FK_Acknowledge2` int(11) DEFAULT NULL COMMENT 'Diketahui sama siapa',
  `FK_ApprovedBy` int(11) DEFAULT NULL COMMENT 'Di setujui sama siapa',
  `Descriptions` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`IDApp`),
  KEY `n_a_disposal_FK_Goods_cf1b33f3` (`FK_Goods`),
  KEY `n_a_disposal_FK_Maintenance_121b5af1` (`FK_Maintenance`),
  KEY `n_a_disposal_FK_Acc_FA_40cc05a8` (`FK_Acc_FA`),
  KEY `n_a_disposal_FK_Stock_12c9c730` (`FK_Stock`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_disposal: ~0 rows (approximately)
DELETE FROM `n_a_disposal`;
/*!40000 ALTER TABLE `n_a_disposal` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_disposal` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_ga_outwards
CREATE TABLE IF NOT EXISTS `n_a_ga_outwards` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `TypeApp` varchar(32) NOT NULL,
  `IsNew` tinyint(1) NOT NULL,
  `DateRequest` datetime(6) NOT NULL,
  `DateReleased` datetime(6) NOT NULL,
  `lastinfo` varchar(150) DEFAULT NULL,
  `Descriptions` varchar(250) DEFAULT NULL,
  `Equipment` varchar(200) DEFAULT NULL,
  `Add_Equipment` varchar(200) DEFAULT NULL,
  `fk_app` int(11) NOT NULL,
  `FK_Employee` int(11) NOT NULL,
  `FK_FromMaintenance` int(11) DEFAULT NULL,
  `FK_Goods` int(11) NOT NULL,
  `FK_Receive` int(11) DEFAULT NULL,
  `FK_ResponsiblePerson` int(11) DEFAULT NULL,
  `FK_Return` int(11) DEFAULT NULL,
  `FK_Sender` int(11) DEFAULT NULL,
  `FK_Stock` int(11) DEFAULT NULL,
  `FK_UsedEmployee` int(11) DEFAULT NULL,
  PRIMARY KEY (`IDApp`),
  KEY `n_a_ga_outwards_fk_app_4077b959` (`fk_app`),
  KEY `n_a_ga_outwards_FK_Employee_0da7476b` (`FK_Employee`),
  KEY `n_a_ga_outwards_FK_FromMaintenance_2693f00b` (`FK_FromMaintenance`),
  KEY `n_a_ga_outwards_FK_Goods_f16c0690` (`FK_Goods`),
  KEY `n_a_ga_outwards_FK_Receive_3639c96c` (`FK_Receive`),
  KEY `n_a_ga_outwards_FK_ResponsiblePerson_56377345` (`FK_ResponsiblePerson`),
  KEY `n_a_ga_outwards_FK_Return_2e0ad370` (`FK_Return`),
  KEY `n_a_ga_outwards_FK_Sender_60cd0d89` (`FK_Sender`),
  KEY `n_a_ga_outwards_FK_Stock_f0370f3a` (`FK_Stock`),
  KEY `n_a_ga_outwards_FK_UsedEmployee_42a485ea` (`FK_UsedEmployee`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_ga_outwards: ~0 rows (approximately)
DELETE FROM `n_a_ga_outwards`;
/*!40000 ALTER TABLE `n_a_ga_outwards` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_outwards` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_ga_receive
CREATE TABLE IF NOT EXISTS `n_a_ga_receive` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `DateReceived` datetime(6) NOT NULL,
  `Brand` varchar(100) NOT NULL,
  `Invoice_No` varchar(100) DEFAULT NULL,
  `TypeApp` varchar(64) DEFAULT NULL,
  `Machine_No` varchar(50) NOT NULL,
  `Chassis_No` varchar(50) NOT NULL,
  `Year_Made` date NOT NULL,
  `colour` varchar(20) NOT NULL,
  `Model` varchar(100) DEFAULT NULL,
  `Kind` varchar(30) DEFAULT NULL,
  `Cylinder` varchar(20) DEFAULT NULL,
  `Fuel` varchar(20) DEFAULT NULL,
  `Descriptions` varchar(200) DEFAULT NULL,
  `FK_Goods` int(11) NOT NULL,
  `FK_P_R_By` int(11) DEFAULT NULL,
  `FK_ReceivedBy` int(11) NOT NULL,
  `FK_Suplier` varchar(30) NOT NULL,
  `Price` decimal(30,4) NOT NULL,
  PRIMARY KEY (`IDApp`),
  UNIQUE KEY `Machine_No` (`Machine_No`),
  KEY `na_ga_receive_FK_Goods_ea3fe5b7` (`FK_Goods`),
  KEY `na_ga_receive_FK_P_R_By_0309c1e4` (`FK_P_R_By`),
  KEY `na_ga_receive_FK_ReceivedBy_826d3802` (`FK_ReceivedBy`),
  KEY `na_ga_receive_FK_Suplier_a5d877fb` (`FK_Suplier`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_ga_receive: ~0 rows (approximately)
DELETE FROM `n_a_ga_receive`;
/*!40000 ALTER TABLE `n_a_ga_receive` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_receive` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_ga_return
CREATE TABLE IF NOT EXISTS `n_a_ga_return` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `TypeApp` varchar(32) NOT NULL,
  `SerialNumber` varchar(100) NOT NULL,
  `DateReturn` datetime(6) NOT NULL,
  `Conditions` char(1) NOT NULL,
  `IsCompleted` smallint(5) unsigned NOT NULL,
  `MinusDesc` varchar(100) DEFAULT NULL,
  `Descriptions` varchar(250) DEFAULT NULL,
  `FK_FromEmployee` int(11) DEFAULT NULL,
  `FK_GA_Outwards` int(11) DEFAULT NULL,
  `FK_Goods` int(11) NOT NULL,
  `FK_UsedEmployee` int(11) DEFAULT NULL,
  PRIMARY KEY (`IDApp`),
  KEY `n_a_ga_return_FK_FromEmployee_df523e5c_fk_employee_IDApp` (`FK_FromEmployee`),
  KEY `n_a_ga_return_fk_ga_outwards_7ab80f54_fk_n_a_ga_outwards_IDApp` (`FK_GA_Outwards`),
  KEY `n_a_ga_return_FK_Goods_83ba304b_fk_n_a_goods_IDApp` (`FK_Goods`),
  KEY `n_a_ga_return_FK_UsedEmployee_77110b41_fk_employee_IDApp` (`FK_UsedEmployee`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_ga_return: ~0 rows (approximately)
DELETE FROM `n_a_ga_return`;
/*!40000 ALTER TABLE `n_a_ga_return` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_return` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_ga_vn_history
CREATE TABLE IF NOT EXISTS `n_a_ga_vn_history` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `Reg_No` varchar(50) NOT NULL,
  `FK_App` int(11) NOT NULL,
  `Expired_Reg` date NOT NULL,
  `Date_Reg` date DEFAULT NULL,
  `BPKP_Expired` date NOT NULL,
  `Descriptions` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`IDApp`),
  UNIQUE KEY `Reg_No` (`Reg_No`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_ga_vn_history: ~0 rows (approximately)
DELETE FROM `n_a_ga_vn_history`;
/*!40000 ALTER TABLE `n_a_ga_vn_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_ga_vn_history` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_goods
CREATE TABLE IF NOT EXISTS `n_a_goods` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `InActive` smallint(5) unsigned NOT NULL,
  `Descriptions` varchar(250) DEFAULT NULL,
  `ItemCode` varchar(30) NOT NULL,
  `GoodsName` varchar(150) NOT NULL,
  `BrandName` varchar(100) DEFAULT NULL,
  `PricePerUnit` decimal(30,4) NOT NULL,
  `DepreciationMethod` varchar(3) NOT NULL,
  `Unit` varchar(30) NOT NULL,
  `EconomicLife` decimal(10,2) NOT NULL,
  `Placement` varchar(50) DEFAULT NULL,
  `typeapp` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`IDApp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_goods: ~9 rows (approximately)
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

-- Dumping structure for table na_m_s.n_a_goods_history
CREATE TABLE IF NOT EXISTS `n_a_goods_history` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `TypeApp` varchar(32) NOT NULL,
  `SerialNumber` varchar(100) NOT NULL,
  `FK_Disposal` int(11) DEFAULT NULL,
  `FK_Goods` int(11) NOT NULL,
  `FK_Lending` int(11) DEFAULT NULL,
  `FK_Lost` int(11) DEFAULT NULL,
  `FK_Maintenance` int(11) DEFAULT NULL,
  `FK_Outwards` int(11) DEFAULT NULL,
  `FK_Return` int(11) DEFAULT NULL,
  PRIMARY KEY (`IDApp`),
  KEY `n_a_goods_history_FK_Disposal_be00d0e5` (`FK_Disposal`),
  KEY `n_a_goods_history_FK_Goods_80352120` (`FK_Goods`),
  KEY `n_a_goods_history_FK_Lending_d51d8c56` (`FK_Lending`),
  KEY `n_a_goods_history_FK_Lost_93f237b1` (`FK_Lost`),
  KEY `n_a_goods_history_FK_Maintenance_d088f2bf` (`FK_Maintenance`),
  KEY `n_a_goods_history_FK_Outwards_cc041cd2` (`FK_Outwards`),
  KEY `n_a_goods_history_FK_Return_2dc8ca11` (`FK_Return`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_goods_history: ~0 rows (approximately)
DELETE FROM `n_a_goods_history`;
/*!40000 ALTER TABLE `n_a_goods_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_history` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_goods_lending
CREATE TABLE IF NOT EXISTS `n_a_goods_lending` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `TypeApp` varchar(32) NOT NULL,
  `SerialNumber` varchar(100) NOT NULL,
  `IsNew` int(11) NOT NULL,
  `DateLending` date DEFAULT NULL,
  `DateReturn` datetime(6) DEFAULT NULL,
  `interests` varchar(150) DEFAULT NULL,
  `Status` varchar(10) DEFAULT NULL,
  `lastinfo` varchar(150) DEFAULT NULL,
  `Descriptions` varchar(200) DEFAULT NULL,
  `FK_CurrentApp` int(11) DEFAULT NULL,
  `FK_Employee` int(11) NOT NULL,
  `FK_Goods` int(11) NOT NULL,
  `FK_Maintenance` int(11) DEFAULT NULL,
  `FK_Receive` int(11) DEFAULT NULL,
  `FK_ResponsiblePerson` int(11) DEFAULT NULL,
  `FK_RETURN` int(11) DEFAULT NULL,
  `FK_Sender` int(11) DEFAULT NULL,
  `FK_Stock` int(11) NOT NULL,
  PRIMARY KEY (`IDApp`),
  KEY `n_a_goods_lending_FK_CurrentApp_cf8c1075` (`FK_CurrentApp`),
  KEY `n_a_goods_lending_FK_Employee_5672e138` (`FK_Employee`),
  KEY `n_a_goods_lending_FK_Goods_87b3dd65` (`FK_Goods`),
  KEY `n_a_goods_lending_FK_Maintenance_2b617461` (`FK_Maintenance`),
  KEY `n_a_goods_lending_FK_Receive_fddbc65e` (`FK_Receive`),
  KEY `n_a_goods_lending_FK_ResponsiblePerson_39f17dad` (`FK_ResponsiblePerson`),
  KEY `n_a_goods_lending_FK_RETURN_6aa8be52` (`FK_RETURN`),
  KEY `n_a_goods_lending_FK_Sender_036a0f94` (`FK_Sender`),
  KEY `n_a_goods_lending_FK_Stock_1394e31c` (`FK_Stock`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_goods_lending: ~0 rows (approximately)
DELETE FROM `n_a_goods_lending`;
/*!40000 ALTER TABLE `n_a_goods_lending` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_lending` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_goods_lost
CREATE TABLE IF NOT EXISTS `n_a_goods_lost` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `TypeApp` varchar(32) NOT NULL,
  `SerialNumber` varchar(100) NOT NULL,
  `DateLost` datetime(6) NOT NULL,
  `FromGoods` varchar(10) NOT NULL,
  `Status` varchar(5) NOT NULL,
  `Descriptions` varchar(250) DEFAULT NULL,
  `Reason` varchar(250) DEFAULT NULL,
  `FK_Goods` int(11) NOT NULL,
  `FK_Goods_Lending` int(11) DEFAULT NULL,
  `FK_Goods_Outwards` int(11) DEFAULT NULL,
  `FK_LostBy` int(11) DEFAULT NULL,
  `FK_Maintenance` int(11) DEFAULT NULL,
  `FK_ResponsiblePerson` int(11) DEFAULT NULL,
  `FK_UsedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`IDApp`),
  KEY `n_a_goods_lost_FK_Goods_aba92f90` (`FK_Goods`),
  KEY `n_a_goods_lost_FK_Goods_Lending_6b337643` (`FK_Goods_Lending`),
  KEY `n_a_goods_lost_FK_Goods_Outwards_6acbc701` (`FK_Goods_Outwards`),
  KEY `n_a_goods_lost_FK_LostBy_6bc2cae8` (`FK_LostBy`),
  KEY `n_a_goods_lost_FK_Maintenance_282c0f2a` (`FK_Maintenance`),
  KEY `n_a_goods_lost_FK_ResponsiblePerson_0768f0a8` (`FK_ResponsiblePerson`),
  KEY `n_a_goods_lost_FK_UsedBy_610b0e23` (`FK_UsedBy`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_goods_lost: ~0 rows (approximately)
DELETE FROM `n_a_goods_lost`;
/*!40000 ALTER TABLE `n_a_goods_lost` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_lost` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_goods_outwards
CREATE TABLE IF NOT EXISTS `n_a_goods_outwards` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `TypeApp` varchar(32) NOT NULL,
  `SerialNumber` varchar(100) NOT NULL,
  `IsNew` tinyint(1) NOT NULL,
  `DateRequest` datetime(6) NOT NULL,
  `DateReleased` datetime(6) NOT NULL,
  `lastinfo` varchar(150) DEFAULT NULL,
  `Descriptions` varchar(250) DEFAULT NULL,
  `FK_Employee` int(11) NOT NULL,
  `FK_FromMaintenance` int(11) DEFAULT NULL,
  `FK_Goods` int(11) NOT NULL,
  `FK_Lending` int(11) DEFAULT NULL,
  `FK_Receive` int(11) DEFAULT NULL,
  `FK_ResponsiblePerson` int(11) DEFAULT NULL,
  `FK_Return` int(11) DEFAULT NULL,
  `FK_Sender` int(11) DEFAULT NULL,
  `FK_Stock` int(11) DEFAULT NULL,
  `FK_UsedEmployee` int(11) DEFAULT NULL,
  PRIMARY KEY (`IDApp`),
  KEY `n_a_goods_outwards_FK_Employee_51e71d5e` (`FK_Employee`),
  KEY `n_a_goods_outwards_FK_FromMaintenance_98e98e30` (`FK_FromMaintenance`),
  KEY `n_a_goods_outwards_FK_Goods_f99be397` (`FK_Goods`),
  KEY `n_a_goods_outwards_FK_Lending_e9c36a17` (`FK_Lending`),
  KEY `n_a_goods_outwards_FK_Receive_42ad46a3` (`FK_Receive`),
  KEY `n_a_goods_outwards_FK_ResponsiblePerson_d1d69b26` (`FK_ResponsiblePerson`),
  KEY `n_a_goods_outwards_FK_Return_cc0724e3` (`FK_Return`),
  KEY `n_a_goods_outwards_FK_Sender_7cda2779` (`FK_Sender`),
  KEY `n_a_goods_outwards_FK_Stock_d4374e2a` (`FK_Stock`),
  KEY `n_a_goods_outwards_FK_UsedEmployee_eb2057f8` (`FK_UsedEmployee`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_goods_outwards: ~0 rows (approximately)
DELETE FROM `n_a_goods_outwards`;
/*!40000 ALTER TABLE `n_a_goods_outwards` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_outwards` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_goods_receive
CREATE TABLE IF NOT EXISTS `n_a_goods_receive` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `DateReceived` datetime(6) NOT NULL,
  `TotalPurchase` smallint(6) NOT NULL,
  `TotalReceived` smallint(6) NOT NULL,
  `Descriptions` varchar(250) DEFAULT NULL,
  `DescBySystem` varchar(250) DEFAULT NULL,
  `REFNO` varchar(50) NOT NULL,
  `FK_Suplier` varchar(30) NOT NULL,
  `fk_goods` int(11) NOT NULL,
  `FK_P_R_By` int(11) DEFAULT NULL,
  `FK_ReceivedBy` int(11) NOT NULL,
  PRIMARY KEY (`IDApp`),
  KEY `n_a_goods_receive_FK_Suplier_27c38e4b` (`FK_Suplier`),
  KEY `n_a_goods_receive_fk_goods_4d3aed25` (`fk_goods`),
  KEY `n_a_goods_receive_FK_P_R_By_4e6fdf1f` (`FK_P_R_By`),
  KEY `n_a_goods_receive_FK_ReceivedBy_42f8bb5d` (`FK_ReceivedBy`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_goods_receive: ~0 rows (approximately)
DELETE FROM `n_a_goods_receive`;
/*!40000 ALTER TABLE `n_a_goods_receive` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_receive` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_goods_receive_detail
CREATE TABLE IF NOT EXISTS `n_a_goods_receive_detail` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `BrandName` varchar(100) NOT NULL,
  `PricePerUnit` decimal(30,4) NOT NULL,
  `TypeApp` varchar(32) NOT NULL,
  `Warranty` decimal(6,2) NOT NULL,
  `EndOfWarranty` datetime(6) DEFAULT NULL,
  `SerialNumber` varchar(100) NOT NULL,
  `FK_App` int(11) NOT NULL,
  PRIMARY KEY (`IDApp`),
  KEY `n_a_goods_receive_detail_FK_App_dc14d9df` (`FK_App`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_goods_receive_detail: ~0 rows (approximately)
DELETE FROM `n_a_goods_receive_detail`;
/*!40000 ALTER TABLE `n_a_goods_receive_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_receive_detail` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_goods_receive_other
CREATE TABLE IF NOT EXISTS `n_a_goods_receive_other` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `DateReceived` datetime(6) NOT NULL,
  `TotalPurchase` smallint(6) NOT NULL,
  `TotalReceived` smallint(6) NOT NULL,
  `Descriptions` varchar(250) DEFAULT NULL,
  `DescBySystem` varchar(250) DEFAULT NULL,
  `REFNO` varchar(50) NOT NULL,
  `fk_goods` int(11) NOT NULL,
  `FK_P_R_By` int(11) DEFAULT NULL,
  `FK_ReceivedBy` int(11) NOT NULL,
  `FK_Suplier` varchar(30) NOT NULL,
  PRIMARY KEY (`IDApp`),
  KEY `n_a_goods_receive_other_fk_goods_5aac0bf5` (`fk_goods`),
  KEY `n_a_goods_receive_other_FK_P_R_By_5cc1a1af` (`FK_P_R_By`),
  KEY `n_a_goods_receive_other_FK_ReceivedBy_5e2fd3a8` (`FK_ReceivedBy`),
  KEY `n_a_goods_receive_other_FK_Suplier_ffa95ef8` (`FK_Suplier`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_goods_receive_other: ~0 rows (approximately)
DELETE FROM `n_a_goods_receive_other`;
/*!40000 ALTER TABLE `n_a_goods_receive_other` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_receive_other` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_goods_return
CREATE TABLE IF NOT EXISTS `n_a_goods_return` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `TypeApp` varchar(32) NOT NULL,
  `SerialNumber` varchar(100) NOT NULL,
  `DateReturn` datetime(6) NOT NULL,
  `Conditions` varchar(1) NOT NULL,
  `IsCompleted` smallint(5) unsigned NOT NULL,
  `MinusDesc` varchar(100) DEFAULT NULL,
  `Descriptions` varchar(250) DEFAULT NULL,
  `FK_FromEmployee` int(11) DEFAULT NULL,
  `FK_Goods` int(11) NOT NULL,
  `FK_Goods_Lend` int(11) DEFAULT NULL,
  `FK_Goods_Outwards` int(11) DEFAULT NULL,
  `FK_UsedEmployee` int(11) DEFAULT NULL,
  PRIMARY KEY (`IDApp`),
  KEY `n_a_goods_return_FK_FromEmployee_1394a31e` (`FK_FromEmployee`),
  KEY `n_a_goods_return_FK_Goods_84da38a6` (`FK_Goods`),
  KEY `n_a_goods_return_FK_Goods_Lend_7d936056` (`FK_Goods_Lend`),
  KEY `n_a_goods_return_FK_Goods_Outwards_ec9d9728` (`FK_Goods_Outwards`),
  KEY `n_a_goods_return_FK_UsedEmployee_bf92cae7` (`FK_UsedEmployee`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_goods_return: ~0 rows (approximately)
DELETE FROM `n_a_goods_return`;
/*!40000 ALTER TABLE `n_a_goods_return` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_goods_return` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_maintenance
CREATE TABLE IF NOT EXISTS `n_a_maintenance` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `SerialNumber` varchar(100) NOT NULL,
  `RequestDate` date DEFAULT NULL,
  `StartDate` date NOT NULL,
  `IsStillGuarantee` longtext NOT NULL,
  `Expense` decimal(10,4) NOT NULL,
  `MaintenanceBy` varchar(100) NOT NULL,
  `PersonalName` varchar(100) DEFAULT NULL,
  `EndDate` date DEFAULT NULL,
  `TypeApp` varchar(32) NOT NULL,
  `IsSucced` int(11) DEFAULT NULL,
  `IsFinished` tinyint(1) NOT NULL,
  `Descriptions` varchar(250) DEFAULT NULL,
  `FK_Goods` int(11) NOT NULL,
  PRIMARY KEY (`IDApp`),
  KEY `n_a_maintenance_FK_Goods_605ee195` (`FK_Goods`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_maintenance: ~0 rows (approximately)
DELETE FROM `n_a_maintenance`;
/*!40000 ALTER TABLE `n_a_maintenance` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_maintenance` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_priviledge
CREATE TABLE IF NOT EXISTS `n_a_priviledge` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Email` varchar(254) NOT NULL,
  `Divisi` varchar(5) NOT NULL,
  `Password` varchar(128) NOT NULL,
  `Picture` varchar(100) DEFAULT NULL,
  `Last_login` datetime(6) DEFAULT NULL,
  `Last_form` varchar(50) DEFAULT NULL,
  `Computer_Name` varchar(50) NOT NULL,
  `IP_Address` varchar(20) NOT NULL,
  `Role` int(11) DEFAULT NULL,
  `Is_SuperUser` tinyint(1) NOT NULL,
  `Is_Staff` tinyint(1) NOT NULL,
  `Is_Active` tinyint(1) NOT NULL,
  `Date_Joined` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`IDApp`),
  UNIQUE KEY `UserName` (`UserName`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_priviledge: ~1 rows (approximately)
DELETE FROM `n_a_priviledge`;
/*!40000 ALTER TABLE `n_a_priviledge` DISABLE KEYS */;
INSERT INTO `n_a_priviledge` (`IDApp`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `first_name`, `last_name`, `UserName`, `Email`, `Divisi`, `Password`, `Picture`, `Last_login`, `Last_form`, `Computer_Name`, `IP_Address`, `Role`, `Is_SuperUser`, `Is_Staff`, `Is_Active`, `Date_Joined`) VALUES
	(1, '', NULL, NULL, '', '', 'rimba88', 'rimba@88spares.com', 'IT', 'pbkdf2_sha256$36000$vACo7Q3KBjS5$UOEFP68Os1qQVdFh5PlbOOC8WpFufG8MGnrtP/pXQKA=', 'dir_for_rimba88\\20180515_100310.jpg', '2018-08-14 19:13:18.553285', NULL, '', '', 1, 1, 0, 1, NULL);
/*!40000 ALTER TABLE `n_a_priviledge` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_priviledge_form
CREATE TABLE IF NOT EXISTS `n_a_priviledge_form` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `Form_id` varchar(20) NOT NULL,
  `Form_name` varchar(30) NOT NULL,
  `Form_name_ori` varchar(50) NOT NULL,
  PRIMARY KEY (`IDApp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

-- Dumping structure for table na_m_s.n_a_priviledge_groups
CREATE TABLE IF NOT EXISTS `n_a_priviledge_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `napriviledge_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `N_A_Priviledge_groups_napriviledge_id_group_id_1fc422ce_uniq` (`napriviledge_id`,`group_id`),
  KEY `N_A_Priviledge_groups_group_id_064198b1_fk_auth_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_priviledge_groups: ~0 rows (approximately)
DELETE FROM `n_a_priviledge_groups`;
/*!40000 ALTER TABLE `n_a_priviledge_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_priviledge_groups` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_priviledge_user_permissions
CREATE TABLE IF NOT EXISTS `n_a_priviledge_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `napriviledge_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `N_A_Priviledge_user_perm_napriviledge_id_permissi_f33eb8e5_uniq` (`napriviledge_id`,`permission_id`),
  KEY `N_A_Priviledge_user__permission_id_ac512c4c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `N_A_Priviledge_user__napriviledge_id_d800ea12_fk_N_A_Privi` FOREIGN KEY (`napriviledge_id`) REFERENCES `n_a_priviledge` (`IDApp`),
  CONSTRAINT `N_A_Priviledge_user__permission_id_ac512c4c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_priviledge_user_permissions: ~0 rows (approximately)
DELETE FROM `n_a_priviledge_user_permissions`;
/*!40000 ALTER TABLE `n_a_priviledge_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_priviledge_user_permissions` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_stock
CREATE TABLE IF NOT EXISTS `n_a_stock` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `T_Goods_Spare` smallint(5) unsigned DEFAULT NULL COMMENT 'column ini untuk menampilkan spare barang yang ada untuk peminjaman saja, ',
  `TotalQty` int(11) DEFAULT NULL,
  `TIsUsed` int(11) DEFAULT NULL,
  `TIsNew` smallint(6) DEFAULT NULL COMMENT 'hanya menampilkan total barang baru, data akan berkurang bila ada peminjaman atau pengeluaran',
  `TIsRenew` smallint(6) DEFAULT NULL COMMENT 'menampilkan total barang yang di perbaiki dan berhasil di perbaiki saja',
  `TIsBroken` int(11) DEFAULT NULL COMMENT 'column ini untuk menampilkan total barang rusak,di peroleh dari return atau sesudah maitenance (static)',
  `TGoods_Return` smallint(6) DEFAULT NULL COMMENT 'menampilkan total barang di return saja',
  `TGoods_Received` int(11) DEFAULT NULL,
  `TDisposal` int(11) DEFAULT NULL COMMENT 'Menampilkan total barang yang sudah di jual/ di hapuskan assetnya',
  `TIsLost` int(11) DEFAULT NULL COMMENT 'Menampikan barang yang hilang saja',
  `TMaintenance` smallint(6) DEFAULT NULL COMMENT 'menampilkan total barang yang di perbaiki, masih di bengkel',
  `FK_Goods` int(11) unsigned zerofill NOT NULL,
  PRIMARY KEY (`IDApp`),
  KEY `n_a_stock_FK_Goods_33dba749` (`FK_Goods`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_stock: ~0 rows (approximately)
DELETE FROM `n_a_stock`;
/*!40000 ALTER TABLE `n_a_stock` DISABLE KEYS */;
/*!40000 ALTER TABLE `n_a_stock` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_suplier
CREATE TABLE IF NOT EXISTS `n_a_suplier` (
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `InActive` smallint(5) unsigned NOT NULL,
  `SuplierCode` varchar(30) NOT NULL,
  `SuplierName` varchar(100) DEFAULT NULL,
  `Address` varchar(150) DEFAULT NULL,
  `Telp` varchar(20) DEFAULT NULL,
  `HP` varchar(20) DEFAULT NULL,
  `ContactPerson` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`SuplierCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.n_a_suplier: ~6 rows (approximately)
DELETE FROM `n_a_suplier`;
/*!40000 ALTER TABLE `n_a_suplier` DISABLE KEYS */;
INSERT INTO `n_a_suplier` (`CreatedDate`, `CreatedBy`, `ModifiedDate`, `ModifiedBy`, `InActive`, `SuplierCode`, `SuplierName`, `Address`, `Telp`, `HP`, `ContactPerson`) VALUES
	('2018-08-15 17:47:02.807019', 'rimba88', '2018-08-15 17:47:17.653669', 'rimba88', 1, 'AST002IDR', 'PT. ASTRA HONDA MOTOR', 'Jl. Laksda Yos Sudarso – Sunter I Jakarta 14350, Indonesia Tel. 0811-9-500-989', '021-7252000', '021-7252000', 'ASTRA'),
	('2018-08-15 17:38:21.108955', 'rimba88', NULL, NULL, 0, 'AST007IDR', 'PT. ASTRA INTERNATIONAL TBK', 'Jl. Pangeran Jayakarta no 28', '021-65906060', '021-6522555', 'Eko'),
	('2018-08-15 17:00:31.272246', 'rimba88', NULL, NULL, 0, 'CHA001IDR', 'CV CHA-CHA KARYA', 'JLn Sultan Agung Prokyek Pasar Rumput', '021-8033870', '081288725559', 'Rudi'),
	('2018-08-15 17:08:39.503456', 'rimba88', NULL, NULL, 0, 'ERA004IDR', 'PT. ERAPOINT GLOBALINDO', 'Jl. KH. Hasyim Azhari No.125 Komp. Niaga Roxy Mas Blok D4/21-22 JakartaPusat 10150', '021-6322555', '082111188729', 'Debby Cintya Dewi'),
	('2018-08-15 16:50:03.851840', 'rimba88', '2018-08-15 17:09:32.926966', 'rimba88', 1, 'MUL016IDR', 'CV MULTI SKINDO UTAMA', 'Jln Pangeran Jayakarta No .77 /GATEP, (NO.HP Customer belum di input di accpac)', '021-659030', '0216491264', 'Himawan Setiadi'),
	('2018-08-15 17:21:44.850050', 'rimba88', NULL, NULL, 0, 'PAR002USD', 'PT PARANTA ANUGERAH PRIMA', 'Wisma CORMIC Delta Building Blok A 4-7 l. Suryopranoto No. 1-9 Jakarta - 10160 Indonesia (No HP belum ada di isi sementara pakai no telp)', '021-3501188', '021-3501555', 'Fermin Setiawan');
/*!40000 ALTER TABLE `n_a_suplier` ENABLE KEYS */;

-- Dumping structure for table na_m_s.n_a_sys_priviledge
CREATE TABLE IF NOT EXISTS `n_a_sys_priviledge` (
  `IDApp` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDate` datetime(6) NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime(6) DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL,
  `Permission` varchar(50) NOT NULL,
  `InActive` int(11) DEFAULT NULL,
  `FK_PForm` int(11) NOT NULL,
  `User_id` int(11) NOT NULL,
  PRIMARY KEY (`IDApp`),
  UNIQUE KEY `N_A_Sys_Priviledge_FK_PForm_Permission_User_id_a02f6fa1_uniq` (`FK_PForm`,`Permission`,`User_id`),
  KEY `N_A_Sys_Priviledge_FK_PForm_84e902b7` (`FK_PForm`),
  KEY `N_A_Sys_Priviledge_User_id_6374718d` (`User_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

-- Dumping structure for table na_m_s.social_auth_association
CREATE TABLE IF NOT EXISTS `social_auth_association` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` varchar(255) NOT NULL,
  `issued` int(11) NOT NULL,
  `lifetime` int(11) NOT NULL,
  `assoc_type` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_association_server_url_handle_078befa2_uniq` (`server_url`,`handle`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.social_auth_association: ~0 rows (approximately)
DELETE FROM `social_auth_association`;
/*!40000 ALTER TABLE `social_auth_association` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_association` ENABLE KEYS */;

-- Dumping structure for table na_m_s.social_auth_code
CREATE TABLE IF NOT EXISTS `social_auth_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `code` varchar(32) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_code_email_code_801b2d02_uniq` (`email`,`code`),
  KEY `social_auth_code_code_a2393167` (`code`),
  KEY `social_auth_code_timestamp_176b341f` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.social_auth_code: ~0 rows (approximately)
DELETE FROM `social_auth_code`;
/*!40000 ALTER TABLE `social_auth_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_code` ENABLE KEYS */;

-- Dumping structure for table na_m_s.social_auth_nonce
CREATE TABLE IF NOT EXISTS `social_auth_nonce` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `salt` varchar(65) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_nonce_server_url_timestamp_salt_f6284463_uniq` (`server_url`,`timestamp`,`salt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.social_auth_nonce: ~0 rows (approximately)
DELETE FROM `social_auth_nonce`;
/*!40000 ALTER TABLE `social_auth_nonce` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_nonce` ENABLE KEYS */;

-- Dumping structure for table na_m_s.social_auth_partial
CREATE TABLE IF NOT EXISTS `social_auth_partial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(32) NOT NULL,
  `next_step` smallint(5) unsigned NOT NULL,
  `backend` varchar(32) NOT NULL,
  `data` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `social_auth_partial_token_3017fea3` (`token`),
  KEY `social_auth_partial_timestamp_50f2119f` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.social_auth_partial: ~0 rows (approximately)
DELETE FROM `social_auth_partial`;
/*!40000 ALTER TABLE `social_auth_partial` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_partial` ENABLE KEYS */;

-- Dumping structure for table na_m_s.social_auth_usersocialauth
CREATE TABLE IF NOT EXISTS `social_auth_usersocialauth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(32) NOT NULL,
  `uid` varchar(255) NOT NULL,
  `extra_data` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_usersocialauth_provider_uid_e6b5e668_uniq` (`provider`,`uid`),
  KEY `social_auth_usersoci_user_id_17d28448_fk_N_A_Privi` (`user_id`),
  CONSTRAINT `social_auth_usersoci_user_id_17d28448_fk_N_A_Privi` FOREIGN KEY (`user_id`) REFERENCES `n_a_priviledge` (`IDApp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table na_m_s.social_auth_usersocialauth: ~0 rows (approximately)
DELETE FROM `social_auth_usersocialauth`;
/*!40000 ALTER TABLE `social_auth_usersocialauth` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_usersocialauth` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
