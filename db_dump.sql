# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.18)
# Database: vinna_main
# Generation Time: 2017-07-28 15:30:31 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table account_account
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account_account`;

CREATE TABLE `account_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `phone` varchar(25) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(1) NOT NULL,
  `profile_photo_url` varchar(100) NOT NULL,
  `last_modified_date` datetime(6) NOT NULL,
  `language_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `referral_account_id` int(11),
  `email_verified` varchar(50) NOT NULL,
  `phone_verified` varchar(50) NOT NULL,
  `country_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `account_account_language_id_b20e6fc3_fk_core_language_id` (`language_id`),
  KEY `account_accou_referral_account_id_a64507e0_fk_account_account_id` (`referral_account_id`),
  KEY `account_account_country_id_89d10c39_fk_core_country_id` (`country_id`),
  CONSTRAINT `account_accou_referral_account_id_a64507e0_fk_account_account_id` FOREIGN KEY (`referral_account_id`) REFERENCES `account_account` (`id`),
  CONSTRAINT `account_account_country_id_89d10c39_fk_core_country_id` FOREIGN KEY (`country_id`) REFERENCES `core_country` (`id`),
  CONSTRAINT `account_account_language_id_b20e6fc3_fk_core_language_id` FOREIGN KEY (`language_id`) REFERENCES `core_language` (`id`),
  CONSTRAINT `account_account_user_id_8d4f4816_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table account_accountpartnerrole
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account_accountpartnerrole`;

CREATE TABLE `account_accountpartnerrole` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(10) NOT NULL,
  `description` varchar(100) NOT NULL,
  `account_id` int(11) NOT NULL,
  `business_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_accountpartner_account_id_ba85fb70_fk_account_account_id` (`account_id`),
  KEY `account_accountpart_business_id_d0f178c6_fk_business_business_id` (`business_id`),
  CONSTRAINT `account_accountpart_business_id_d0f178c6_fk_business_business_id` FOREIGN KEY (`business_id`) REFERENCES `business_business` (`id`),
  CONSTRAINT `account_accountpartner_account_id_ba85fb70_fk_account_account_id` FOREIGN KEY (`account_id`) REFERENCES `account_account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table account_accountreferral
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account_accountreferral`;

CREATE TABLE `account_accountreferral` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `friend_email_or_phone` varchar(40) NOT NULL,
  `friend_ip` varchar(15) DEFAULT NULL,
  `friend_user_agent` varchar(200) DEFAULT NULL,
  `friend_referrer` varchar(200) DEFAULT NULL,
  `connected` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `account_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_accountreferra_account_id_1d34fa67_fk_account_account_id` (`account_id`),
  CONSTRAINT `account_accountreferra_account_id_1d34fa67_fk_account_account_id` FOREIGN KEY (`account_id`) REFERENCES `account_account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_group
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_group_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_permission
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`)
VALUES
	(1,'Can add log entry',1,'add_logentry'),
	(2,'Can change log entry',1,'change_logentry'),
	(3,'Can delete log entry',1,'delete_logentry'),
	(4,'Can add permission',2,'add_permission'),
	(5,'Can change permission',2,'change_permission'),
	(6,'Can delete permission',2,'delete_permission'),
	(7,'Can add group',3,'add_group'),
	(8,'Can change group',3,'change_group'),
	(9,'Can delete group',3,'delete_group'),
	(10,'Can add user',4,'add_user'),
	(11,'Can change user',4,'change_user'),
	(12,'Can delete user',4,'delete_user'),
	(13,'Can add content type',5,'add_contenttype'),
	(14,'Can change content type',5,'change_contenttype'),
	(15,'Can delete content type',5,'delete_contenttype'),
	(16,'Can add session',6,'add_session'),
	(17,'Can change session',6,'change_session'),
	(18,'Can delete session',6,'delete_session'),
	(19,'Can add Token',7,'add_token'),
	(20,'Can change Token',7,'change_token'),
	(21,'Can delete Token',7,'delete_token'),
	(22,'Can add state',8,'add_state'),
	(23,'Can change state',8,'change_state'),
	(24,'Can delete state',8,'delete_state'),
	(25,'Can add user log',9,'add_userlog'),
	(26,'Can change user log',9,'change_userlog'),
	(27,'Can delete user log',9,'delete_userlog'),
	(28,'Can add language',10,'add_language'),
	(29,'Can change language',10,'change_language'),
	(30,'Can delete language',10,'delete_language'),
	(31,'Can add country',11,'add_country'),
	(32,'Can change country',11,'change_country'),
	(33,'Can delete country',11,'delete_country'),
	(34,'Can add notification',12,'add_notification'),
	(35,'Can change notification',12,'change_notification'),
	(36,'Can delete notification',12,'delete_notification'),
	(37,'Can add video',13,'add_video'),
	(38,'Can change video',13,'change_video'),
	(39,'Can delete video',13,'delete_video'),
	(40,'Can add business video',14,'add_businessvideo'),
	(41,'Can change business video',14,'change_businessvideo'),
	(42,'Can delete business video',14,'delete_businessvideo'),
	(43,'Can add image',15,'add_image'),
	(44,'Can change image',15,'change_image'),
	(45,'Can delete image',15,'delete_image'),
	(46,'Can add business image',16,'add_businessimage'),
	(47,'Can change business image',16,'change_businessimage'),
	(48,'Can delete business image',16,'delete_businessimage'),
	(49,'Can add category',17,'add_category'),
	(50,'Can change category',17,'change_category'),
	(51,'Can delete category',17,'delete_category'),
	(52,'Can add business billing info',18,'add_businessbillinginfo'),
	(53,'Can change business billing info',18,'change_businessbillinginfo'),
	(54,'Can delete business billing info',18,'delete_businessbillinginfo'),
	(55,'Can add sub category',19,'add_subcategory'),
	(56,'Can change sub category',19,'change_subcategory'),
	(57,'Can delete sub category',19,'delete_subcategory'),
	(58,'Can add invitation',20,'add_invitation'),
	(59,'Can change invitation',20,'change_invitation'),
	(60,'Can delete invitation',20,'delete_invitation'),
	(61,'Can add business',21,'add_business'),
	(62,'Can change business',21,'change_business'),
	(63,'Can delete business',21,'delete_business'),
	(64,'Can add purchase',22,'add_purchase'),
	(65,'Can change purchase',22,'change_purchase'),
	(66,'Can delete purchase',22,'delete_purchase'),
	(67,'Can add account referral',23,'add_accountreferral'),
	(68,'Can change account referral',23,'change_accountreferral'),
	(69,'Can delete account referral',23,'delete_accountreferral'),
	(70,'Can add account partner role',24,'add_accountpartnerrole'),
	(71,'Can change account partner role',24,'change_accountpartnerrole'),
	(72,'Can delete account partner role',24,'delete_accountpartnerrole'),
	(73,'Can add account',25,'add_account'),
	(74,'Can change account',25,'change_account'),
	(75,'Can delete account',25,'delete_account'),
	(76,'Can add member payment info',26,'add_memberpaymentinfo'),
	(77,'Can change member payment info',26,'change_memberpaymentinfo'),
	(78,'Can delete member payment info',26,'delete_memberpaymentinfo'),
	(79,'Can add member',27,'add_member'),
	(80,'Can change member',27,'change_member'),
	(81,'Can delete member',27,'delete_member'),
	(82,'Can add review',28,'add_review'),
	(83,'Can change review',28,'change_review'),
	(84,'Can delete review',28,'delete_review');

/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table auth_user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user`;

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`)
VALUES
	(1,'pbkdf2_sha256$30000$dQD7ONZEAvvr$6fdkHIkFqgS+JfiPz2smElxvH4AaVcrL1kVEq3zZrbo=','2017-07-28 15:18:17.437307',1,'admin','','','',1,1,'2017-07-28 15:18:01.491617');

/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table auth_user_groups
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user_groups`;

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_user_user_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user_user_permissions`;

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table authtoken_token
# ------------------------------------------------------------

DROP TABLE IF EXISTS `authtoken_token`;

CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table business_business
# ------------------------------------------------------------

DROP TABLE IF EXISTS `business_business`;

CREATE TABLE `business_business` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(50) NOT NULL,
  `taxid` varchar(15) NOT NULL,
  `city` varchar(20) NOT NULL,
  `zip` varchar(20) NOT NULL,
  `address1` varchar(40) NOT NULL,
  `address2` varchar(40) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` varchar(25) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `facebook_link` varchar(50) NOT NULL,
  `twitter_link` varchar(50) NOT NULL,
  `instagram_link` varchar(50) NOT NULL,
  `linkedin_link` varchar(50) NOT NULL,
  `customer_token` varchar(50) NOT NULL,
  `security_hash` varchar(32) NOT NULL,
  `ssn_token` varchar(10) NOT NULL,
  `last_modified_date` datetime(6) NOT NULL,
  `account_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `state_id` int(11) NOT NULL,
  `sub_category_id` int(11) NOT NULL,
  `picture1` varchar(100) NOT NULL,
  `picture2` varchar(100),
  `picture3` varchar(100),
  `picture4` varchar(100),
  `rating` double,
  `hours` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `business_business_account_id_11bf9bce_fk_account_account_id` (`account_id`),
  KEY `business_business_category_id_7657be0e_fk_business_category_id` (`category_id`),
  KEY `business_business_country_id_cc2e1c86_fk_core_country_id` (`country_id`),
  KEY `business_business_state_id_a7d41959_fk_core_state_id` (`state_id`),
  KEY `business_bus_sub_category_id_e219a128_fk_business_subcategory_id` (`sub_category_id`),
  CONSTRAINT `business_bus_sub_category_id_e219a128_fk_business_subcategory_id` FOREIGN KEY (`sub_category_id`) REFERENCES `business_subcategory` (`id`),
  CONSTRAINT `business_business_account_id_11bf9bce_fk_account_account_id` FOREIGN KEY (`account_id`) REFERENCES `account_account` (`id`),
  CONSTRAINT `business_business_category_id_7657be0e_fk_business_category_id` FOREIGN KEY (`category_id`) REFERENCES `business_category` (`id`),
  CONSTRAINT `business_business_country_id_cc2e1c86_fk_core_country_id` FOREIGN KEY (`country_id`) REFERENCES `core_country` (`id`),
  CONSTRAINT `business_business_state_id_a7d41959_fk_core_state_id` FOREIGN KEY (`state_id`) REFERENCES `core_state` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table business_businessbillinginfo
# ------------------------------------------------------------

DROP TABLE IF EXISTS `business_businessbillinginfo`;

CREATE TABLE `business_businessbillinginfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `type` varchar(10) NOT NULL,
  `text` varchar(4) NOT NULL,
  `token` varchar(70) NOT NULL,
  `zip` varchar(20) NOT NULL,
  `address1` varchar(40) NOT NULL,
  `address2` varchar(40) NOT NULL,
  `business_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `state_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `business_businessbi_business_id_7a00691c_fk_business_business_id` (`business_id`),
  KEY `business_businessbillingi_country_id_4ff34b9c_fk_core_country_id` (`country_id`),
  KEY `business_businessbillinginfo_state_id_ab5c62bd_fk_core_state_id` (`state_id`),
  CONSTRAINT `business_businessbi_business_id_7a00691c_fk_business_business_id` FOREIGN KEY (`business_id`) REFERENCES `business_business` (`id`),
  CONSTRAINT `business_businessbillingi_country_id_4ff34b9c_fk_core_country_id` FOREIGN KEY (`country_id`) REFERENCES `core_country` (`id`),
  CONSTRAINT `business_businessbillinginfo_state_id_ab5c62bd_fk_core_state_id` FOREIGN KEY (`state_id`) REFERENCES `core_state` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table business_category
# ------------------------------------------------------------

DROP TABLE IF EXISTS `business_category`;

CREATE TABLE `business_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `business_category` WRITE;
/*!40000 ALTER TABLE `business_category` DISABLE KEYS */;

INSERT INTO `business_category` (`id`, `text`)
VALUES
	(1,'Consulting services'),
	(2,'Educational services');

/*!40000 ALTER TABLE `business_category` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table business_invitation
# ------------------------------------------------------------

DROP TABLE IF EXISTS `business_invitation`;

CREATE TABLE `business_invitation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `type` varchar(10) NOT NULL,
  `business_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `business_invitation_business_id_d9467b0b_fk_business_business_id` (`business_id`),
  CONSTRAINT `business_invitation_business_id_d9467b0b_fk_business_business_id` FOREIGN KEY (`business_id`) REFERENCES `business_business` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table business_subcategory
# ------------------------------------------------------------

DROP TABLE IF EXISTS `business_subcategory`;

CREATE TABLE `business_subcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(50) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `business_subcategor_category_id_d7f71ebf_fk_business_category_id` (`category_id`),
  CONSTRAINT `business_subcategor_category_id_d7f71ebf_fk_business_category_id` FOREIGN KEY (`category_id`) REFERENCES `business_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `business_subcategory` WRITE;
/*!40000 ALTER TABLE `business_subcategory` DISABLE KEYS */;

INSERT INTO `business_subcategory` (`id`, `text`, `category_id`)
VALUES
	(1,'Safety and health',1),
	(2,'Digital art',2);

/*!40000 ALTER TABLE `business_subcategory` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table core_country
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_country`;

CREATE TABLE `core_country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone_country_code` varchar(5) NOT NULL,
  `abbrev` varchar(5) NOT NULL,
  `text` varchar(50) NOT NULL,
  `english_text` varchar(50) NOT NULL,
  `default_language_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_country_default_language_id_2bc6b649_fk_core_language_id` (`default_language_id`),
  CONSTRAINT `core_country_default_language_id_2bc6b649_fk_core_language_id` FOREIGN KEY (`default_language_id`) REFERENCES `core_language` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `core_country` WRITE;
/*!40000 ALTER TABLE `core_country` DISABLE KEYS */;

INSERT INTO `core_country` (`id`, `phone_country_code`, `abbrev`, `text`, `english_text`, `default_language_id`)
VALUES
	(1,'1','US','United States','United States',1),
	(2,'1','CA','Canada','Canada',1);

/*!40000 ALTER TABLE `core_country` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table core_language
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_language`;

CREATE TABLE `core_language` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(4) NOT NULL,
  `text` varchar(50) NOT NULL,
  `english_text` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `core_language` WRITE;
/*!40000 ALTER TABLE `core_language` DISABLE KEYS */;

INSERT INTO `core_language` (`id`, `code`, `text`, `english_text`)
VALUES
	(1,'EN','English','English');

/*!40000 ALTER TABLE `core_language` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table core_state
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_state`;

CREATE TABLE `core_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `abbrev` varchar(5) NOT NULL,
  `text` varchar(50) NOT NULL,
  `country_id` int(11) NOT NULL,
  `language_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_state_country_id_5a16f697_fk_core_country_id` (`country_id`),
  KEY `core_state_language_id_89a158ff_fk_core_language_id` (`language_id`),
  CONSTRAINT `core_state_country_id_5a16f697_fk_core_country_id` FOREIGN KEY (`country_id`) REFERENCES `core_country` (`id`),
  CONSTRAINT `core_state_language_id_89a158ff_fk_core_language_id` FOREIGN KEY (`language_id`) REFERENCES `core_language` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `core_state` WRITE;
/*!40000 ALTER TABLE `core_state` DISABLE KEYS */;

INSERT INTO `core_state` (`id`, `abbrev`, `text`, `country_id`, `language_id`)
VALUES
	(1,'NY','New York',1,1),
	(2,'CL','California',1,1),
	(3,'ON','Ontario',2,1),
	(4,'BC','British Columbia',2,1);

/*!40000 ALTER TABLE `core_state` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table core_userlog
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_userlog`;

CREATE TABLE `core_userlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(40) NOT NULL,
  `last_login_time` datetime(6) NOT NULL,
  `current_token` varchar(1000) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `core_userlog_user_id_9012a4b6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table django_admin_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`)
VALUES
	(1,'2017-07-28 15:21:32.603076','1','English',1,'[{\"added\": {}}]',10,1),
	(2,'2017-07-28 15:21:34.016447','1','United States (US)',1,'[{\"added\": {}}]',11,1),
	(3,'2017-07-28 15:21:49.542207','2','Canada (CA)',1,'[{\"added\": {}}]',11,1),
	(4,'2017-07-28 15:22:06.052516','1','New York (NY)',1,'[{\"added\": {}}]',8,1),
	(5,'2017-07-28 15:22:20.969156','2','California (CL)',1,'[{\"added\": {}}]',8,1),
	(6,'2017-07-28 15:22:30.066037','3','Ontario (ON)',1,'[{\"added\": {}}]',8,1),
	(7,'2017-07-28 15:22:38.743651','4','British Columbia (BC)',1,'[{\"added\": {}}]',8,1),
	(8,'2017-07-28 15:28:37.665034','1','Consulting services',1,'[{\"added\": {}}]',17,1),
	(9,'2017-07-28 15:28:46.579577','2','Educational services',1,'[{\"added\": {}}]',17,1),
	(10,'2017-07-28 15:29:24.738145','1','Safety and health',1,'[{\"added\": {}}]',19,1),
	(11,'2017-07-28 15:30:01.114171','2','Digital art',1,'[{\"added\": {}}]',19,1);

/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table django_content_type
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;

INSERT INTO `django_content_type` (`id`, `app_label`, `model`)
VALUES
	(25,'account','account'),
	(24,'account','accountpartnerrole'),
	(23,'account','accountreferral'),
	(1,'admin','logentry'),
	(3,'auth','group'),
	(2,'auth','permission'),
	(4,'auth','user'),
	(7,'authtoken','token'),
	(21,'business','business'),
	(18,'business','businessbillinginfo'),
	(17,'business','category'),
	(20,'business','invitation'),
	(19,'business','subcategory'),
	(5,'contenttypes','contenttype'),
	(11,'core','country'),
	(10,'core','language'),
	(8,'core','state'),
	(9,'core','userlog'),
	(16,'media','businessimage'),
	(14,'media','businessvideo'),
	(15,'media','image'),
	(13,'media','video'),
	(27,'member','member'),
	(26,'member','memberpaymentinfo'),
	(12,'notification','notification'),
	(22,'purchase','purchase'),
	(28,'review','review'),
	(6,'sessions','session');

/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table django_migrations
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`)
VALUES
	(1,'contenttypes','0001_initial','2017-07-28 15:12:34.122015'),
	(2,'auth','0001_initial','2017-07-28 15:12:36.878338'),
	(3,'core','0001_initial','2017-07-28 15:12:38.400220'),
	(4,'core','0002_auto_20170708_1846','2017-07-28 15:12:38.536579'),
	(5,'account','0001_initial','2017-07-28 15:12:39.014985'),
	(6,'business','0001_initial','2017-07-28 15:12:42.616711'),
	(7,'media','0001_initial','2017-07-28 15:12:43.614274'),
	(8,'account','0002_auto_20170705_0408','2017-07-28 15:12:44.497261'),
	(9,'member','0001_initial','2017-07-28 15:12:45.908760'),
	(10,'account','0003_auto_20170705_0408','2017-07-28 15:12:46.875042'),
	(11,'account','0004_auto_20170708_2038','2017-07-28 15:12:48.353532'),
	(12,'account','0005_auto_20170710_0300','2017-07-28 15:12:48.825073'),
	(13,'account','0006_auto_20170714_0319','2017-07-28 15:12:48.990651'),
	(14,'account','0007_auto_20170721_0121','2017-07-28 15:12:49.175896'),
	(15,'account','0008_account_verified','2017-07-28 15:12:49.499740'),
	(16,'account','0009_auto_20170724_0247','2017-07-28 15:12:50.507919'),
	(17,'account','0010_account_country','2017-07-28 15:12:50.967821'),
	(18,'admin','0001_initial','2017-07-28 15:12:51.477937'),
	(19,'admin','0002_logentry_remove_auto_add','2017-07-28 15:12:51.829958'),
	(20,'contenttypes','0002_remove_content_type_name','2017-07-28 15:12:52.195298'),
	(21,'auth','0002_alter_permission_name_max_length','2017-07-28 15:12:52.387167'),
	(22,'auth','0003_alter_user_email_max_length','2017-07-28 15:12:52.557167'),
	(23,'auth','0004_alter_user_username_opts','2017-07-28 15:12:52.593675'),
	(24,'auth','0005_alter_user_last_login_null','2017-07-28 15:12:52.744678'),
	(25,'auth','0006_require_contenttypes_0002','2017-07-28 15:12:52.748436'),
	(26,'auth','0007_alter_validators_add_error_messages','2017-07-28 15:12:52.789483'),
	(27,'auth','0008_alter_user_username_max_length','2017-07-28 15:12:52.936577'),
	(28,'authtoken','0001_initial','2017-07-28 15:12:53.261531'),
	(29,'authtoken','0002_auto_20160226_1747','2017-07-28 15:12:53.999454'),
	(30,'business','0002_auto_20170710_0052','2017-07-28 15:12:58.303798'),
	(31,'business','0003_auto_20170714_0319','2017-07-28 15:12:59.716801'),
	(32,'business','0004_auto_20170716_0712','2017-07-28 15:12:59.906511'),
	(33,'business','0005_business_rating','2017-07-28 15:13:00.320137'),
	(34,'business','0006_auto_20170717_1633','2017-07-28 15:13:00.488986'),
	(35,'business','0007_auto_20170718_0039','2017-07-28 15:13:00.857865'),
	(36,'business','0008_business_hours','2017-07-28 15:13:01.228297'),
	(37,'business','0009_auto_20170721_2013','2017-07-28 15:13:01.398301'),
	(38,'business','0010_auto_20170721_2013','2017-07-28 15:13:01.610460'),
	(39,'media','0002_auto_20170708_1302','2017-07-28 15:13:01.939169'),
	(40,'media','0003_auto_20170710_0052','2017-07-28 15:13:04.041248'),
	(41,'media','0004_auto_20170712_1434','2017-07-28 15:13:04.723942'),
	(42,'media','0005_auto_20170712_1737','2017-07-28 15:13:04.770317'),
	(43,'media','0006_businessimage_ref','2017-07-28 15:13:05.108742'),
	(44,'member','0002_auto_20170706_1518','2017-07-28 15:13:05.348422'),
	(45,'member','0003_auto_20170708_2038','2017-07-28 15:13:05.689822'),
	(46,'member','0004_auto_20170710_0300','2017-07-28 15:13:07.223288'),
	(47,'member','0005_auto_20170711_0412','2017-07-28 15:13:07.560336'),
	(48,'member','0006_remove_memberpaymentinfo_type','2017-07-28 15:13:07.724985'),
	(49,'notification','0001_initial','2017-07-28 15:13:07.926302'),
	(50,'notification','0002_auto_20170707_1643','2017-07-28 15:13:10.033048'),
	(51,'notification','0003_auto_20170710_0117','2017-07-28 15:13:10.760739'),
	(52,'notification','0004_auto_20170712_1635','2017-07-28 15:13:11.232099'),
	(53,'notification','0005_auto_20170714_0319','2017-07-28 15:13:12.221170'),
	(54,'notification','0006_auto_20170717_0047','2017-07-28 15:13:12.417686'),
	(55,'notification','0007_auto_20170721_0121','2017-07-28 15:13:13.104926'),
	(56,'purchase','0001_initial','2017-07-28 15:13:13.957804'),
	(57,'purchase','0002_auto_20170710_0052','2017-07-28 15:13:19.929741'),
	(58,'review','0001_initial','2017-07-28 15:13:20.609538'),
	(59,'sessions','0001_initial','2017-07-28 15:13:21.005883');

/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table django_session
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`)
VALUES
	('nvz22ih1wawylo47fy2710gtpb22oiui','YmE2YzVjMzEzMDY4NmM2YzVlYzM2NTg0YzdiMTRkZGZlZGZiMTQ3MTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxMjVjMWQ5MjY0ODE4NWYxMWZkMTRmODViN2RmYjZiYzgyNmUzZmM4In0=','2017-08-11 15:18:17.440866');

/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table media_businessimage
# ------------------------------------------------------------

DROP TABLE IF EXISTS `media_businessimage`;

CREATE TABLE `media_businessimage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hash` varchar(100) NOT NULL,
  `s3_url` varchar(100) NOT NULL,
  `title` varchar(100) NOT NULL,
  `description` varchar(500) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `business_id` int(11) NOT NULL,
  `type` varchar(12) NOT NULL,
  `ref` int(11),
  PRIMARY KEY (`id`),
  KEY `media_businessimage_business_id_5ff66ef4_fk_business_business_id` (`business_id`),
  CONSTRAINT `media_businessimage_business_id_5ff66ef4_fk_business_business_id` FOREIGN KEY (`business_id`) REFERENCES `business_business` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table media_businessvideo
# ------------------------------------------------------------

DROP TABLE IF EXISTS `media_businessvideo`;

CREATE TABLE `media_businessvideo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link` varchar(100) NOT NULL,
  `unique_code` varchar(100) NOT NULL,
  `platform` varchar(1) NOT NULL,
  `business_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_code` (`unique_code`),
  UNIQUE KEY `business_id` (`business_id`),
  CONSTRAINT `media_businessvideo_business_id_521a268b_fk_business_business_id` FOREIGN KEY (`business_id`) REFERENCES `business_business` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table media_image
# ------------------------------------------------------------

DROP TABLE IF EXISTS `media_image`;

CREATE TABLE `media_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hash` varchar(100) NOT NULL,
  `s3_url` varchar(100) NOT NULL,
  `title` varchar(100) NOT NULL,
  `description` varchar(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table media_video
# ------------------------------------------------------------

DROP TABLE IF EXISTS `media_video`;

CREATE TABLE `media_video` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link` varchar(100) NOT NULL,
  `unique_code` varchar(100) NOT NULL,
  `platform` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_code` (`unique_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table member_member
# ------------------------------------------------------------

DROP TABLE IF EXISTS `member_member`;

CREATE TABLE `member_member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mailing_address_1` varchar(40) NOT NULL,
  `mailing_address_2` varchar(40) NOT NULL,
  `mailing_address_city` varchar(50) NOT NULL,
  `mailing_address_zip` varchar(20) NOT NULL,
  `managed_account_token` varchar(50) NOT NULL,
  `security_hash` varchar(32) NOT NULL,
  `ssn_token` varchar(9) NOT NULL,
  `last_modified_date` datetime(6) NOT NULL,
  `account_id` int(11) NOT NULL,
  `mailing_address_country_id` int(11) NOT NULL,
  `mailing_address_state_id` int(11) NOT NULL,
  `profile_image_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_id` (`account_id`),
  KEY `member_me_mailing_address_country_id_d2f19f5d_fk_core_country_id` (`mailing_address_country_id`),
  KEY `member_member_mailing_address_state_id_27f3305e_fk_core_state_id` (`mailing_address_state_id`),
  KEY `member_member_profile_image_id_239300d8_fk_media_image_id` (`profile_image_id`),
  CONSTRAINT `member_me_mailing_address_country_id_d2f19f5d_fk_core_country_id` FOREIGN KEY (`mailing_address_country_id`) REFERENCES `core_country` (`id`),
  CONSTRAINT `member_member_account_id_da2773d3_fk_account_account_id` FOREIGN KEY (`account_id`) REFERENCES `account_account` (`id`),
  CONSTRAINT `member_member_mailing_address_state_id_27f3305e_fk_core_state_id` FOREIGN KEY (`mailing_address_state_id`) REFERENCES `core_state` (`id`),
  CONSTRAINT `member_member_profile_image_id_239300d8_fk_media_image_id` FOREIGN KEY (`profile_image_id`) REFERENCES `media_image` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table member_memberpaymentinfo
# ------------------------------------------------------------

DROP TABLE IF EXISTS `member_memberpaymentinfo`;

CREATE TABLE `member_memberpaymentinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(15) NOT NULL,
  `token` varchar(70) NOT NULL,
  `routing_number` varchar(20) NOT NULL,
  `member_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `member_memberpaymentinfo_member_id_e116a0a2_fk_member_member_id` (`member_id`),
  CONSTRAINT `member_memberpaymentinfo_member_id_e116a0a2_fk_member_member_id` FOREIGN KEY (`member_id`) REFERENCES `member_member` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table notification_notification
# ------------------------------------------------------------

DROP TABLE IF EXISTS `notification_notification`;

CREATE TABLE `notification_notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(140) NOT NULL,
  `category` varchar(50) NOT NULL,
  `state` tinyint(1) NOT NULL,
  `account_id` int(11) DEFAULT NULL,
  `business_id` int(11) NOT NULL,
  `end` datetime(6) DEFAULT NULL,
  `link` varchar(150) DEFAULT NULL,
  `start` datetime(6) DEFAULT NULL,
  `description` varchar(140) NOT NULL,
  `picture` varchar(100) NOT NULL,
  `create_date` datetime(6) NOT NULL,
  `last_modified_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notification_notifi_business_id_caeb145c_fk_business_business_id` (`business_id`),
  KEY `notification_notificat_account_id_82338c6d_fk_account_account_id` (`account_id`),
  CONSTRAINT `notification_notifi_business_id_caeb145c_fk_business_business_id` FOREIGN KEY (`business_id`) REFERENCES `business_business` (`id`),
  CONSTRAINT `notification_notificat_account_id_82338c6d_fk_account_account_id` FOREIGN KEY (`account_id`) REFERENCES `account_account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table purchase_purchase
# ------------------------------------------------------------

DROP TABLE IF EXISTS `purchase_purchase`;

CREATE TABLE `purchase_purchase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` decimal(9,2) NOT NULL,
  `post_date` datetime(6) NOT NULL,
  `balance` decimal(9,2) NOT NULL,
  `posted` tinyint(1) NOT NULL,
  `business_percent` decimal(9,2) NOT NULL,
  `business_amount` decimal(9,2) NOT NULL,
  `business_amount_processed` tinyint(1) NOT NULL,
  `business_amount_processed_date` datetime(6) NOT NULL,
  `member_percent` decimal(9,2) NOT NULL,
  `member_amount` decimal(9,2) NOT NULL,
  `member_amount_processed` tinyint(1) NOT NULL,
  `member_amount_processed_date` datetime(6) NOT NULL,
  `member_ref_percent` decimal(9,2) NOT NULL,
  `member_ref_amount` decimal(9,2) NOT NULL,
  `member_ref_amount_processed` tinyint(1) NOT NULL,
  `member_ref_amount_processed_date` datetime(6) NOT NULL,
  `void_date` datetime(6) NOT NULL,
  `account_id` int(11) NOT NULL,
  `business_id` int(11) NOT NULL,
  `cashier_account_id` int(11) NOT NULL,
  `member_referral_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_purchase_account_id_9d420e8c_fk_account_account_id` (`account_id`),
  KEY `purchase_purchase_business_id_726cf9f7_fk_business_business_id` (`business_id`),
  KEY `purchase_purch_cashier_account_id_201dc9c6_fk_account_account_id` (`cashier_account_id`),
  KEY `purchase_purchas_member_referral_id_b9480892_fk_member_member_id` (`member_referral_id`),
  CONSTRAINT `purchase_purch_cashier_account_id_201dc9c6_fk_account_account_id` FOREIGN KEY (`cashier_account_id`) REFERENCES `account_account` (`id`),
  CONSTRAINT `purchase_purchas_member_referral_id_b9480892_fk_member_member_id` FOREIGN KEY (`member_referral_id`) REFERENCES `member_member` (`id`),
  CONSTRAINT `purchase_purchase_account_id_9d420e8c_fk_account_account_id` FOREIGN KEY (`account_id`) REFERENCES `account_account` (`id`),
  CONSTRAINT `purchase_purchase_business_id_726cf9f7_fk_business_business_id` FOREIGN KEY (`business_id`) REFERENCES `business_business` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table review_review
# ------------------------------------------------------------

DROP TABLE IF EXISTS `review_review`;

CREATE TABLE `review_review` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rating` int(11) NOT NULL,
  `review` varchar(100) DEFAULT NULL,
  `approved` tinyint(1) NOT NULL,
  `approved_date` datetime(6) DEFAULT NULL,
  `account_id` int(11) NOT NULL,
  `business_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `review_review_account_id_4fdea940_uniq` (`account_id`,`business_id`),
  KEY `review_review_business_id_75f10eec_fk_business_business_id` (`business_id`),
  CONSTRAINT `review_review_account_id_b0069e3a_fk_account_account_id` FOREIGN KEY (`account_id`) REFERENCES `account_account` (`id`),
  CONSTRAINT `review_review_business_id_75f10eec_fk_business_business_id` FOREIGN KEY (`business_id`) REFERENCES `business_business` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
