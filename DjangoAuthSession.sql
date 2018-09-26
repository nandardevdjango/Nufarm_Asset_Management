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
