-- Create database if it does not exist
CREATE DATABASE IF NOT EXISTS video;

-- Use the video database
USE video;

-- Create tables if they do not exist

-- video.auth_group definition
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- video.django_content_type definition
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(12,'comment','comment'),(4,'contenttypes','contenttype'),(11,'myadmin','mychunkedupload'),(5,'sessions','session'),(6,'thumbnail','kvstore'),(10,'users','feedback'),(9,'users','user'),(8,'video','classification'),(7,'video','video');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
-- video.django_migrations definition
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4;

-- video.django_session definition
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- video.myadmin_mychunkedupload definition
CREATE TABLE IF NOT EXISTS `myadmin_mychunkedupload` (
  `id` int NOT NULL AUTO_INCREMENT,
  `upload_id` varchar(32) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `offset` bigint NOT NULL,
  `created_on` datetime NOT NULL,
  `status` int NOT NULL,
  `completed_on` datetime DEFAULT NULL,
  `file` varchar(255) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `upload_id` (`upload_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;

-- video.thumbnail_kvstore definition
CREATE TABLE IF NOT EXISTS `thumbnail_kvstore` (
  `key` varchar(200) NOT NULL,
  `value` longtext NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- video.v_classification definition
CREATE TABLE IF NOT EXISTS `v_classification` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8mb4;

-- video.v_comment definition
CREATE TABLE IF NOT EXISTS `v_comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `nickname` varchar(30) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `video_id` int NOT NULL,
  `content` varchar(100) NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

-- video.v_feedback definition
CREATE TABLE IF NOT EXISTS `v_feedback` (
  `id` int NOT NULL AUTO_INCREMENT,
  `contact` varchar(20) DEFAULT NULL,
  `content` varchar(200) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- video.v_user definition
CREATE TABLE IF NOT EXISTS `v_user` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
      `password` varchar(128) NOT NULL,
      `last_login` datetime(6) DEFAULT NULL,
      `is_superuser` tinyint(1) NOT NULL,
      `username` varchar(150) NOT NULL,
      `first_name` varchar(150) NOT NULL,
      `last_name` varchar(150) NOT NULL,
      `email` varchar(254) NOT NULL,
      `is_staff` tinyint(1) NOT NULL,
      `is_active` tinyint(1) NOT NULL,
      `date_joined` datetime(6) NOT NULL,
      `nickname` varchar(20) DEFAULT NULL,
      `avatar` varchar(100) NOT NULL,
      `mobile` varchar(13) DEFAULT NULL,
      `gender` varchar(1) DEFAULT NULL,
      `subscribe` tinyint(1) NOT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
LOCK TABLES `v_user` WRITE;
INSERT INTO `v_user` VALUES (1,'pbkdf2_sha256$260000$dCqfoXVN93jSb9P9ZYjv8l$xa6yPaQRmVx+c3H1OYCDa4M066iSZAtnQdxrnB/SBMA=','2023-07-07 13:22:36.445833',0,'admin123','','','1225262920@qq.com',1,1,'2023-03-06 21:14:52.296156','用户','','15917143157','M',0);
UNLOCK TABLES;

-- video.v_video definition
CREATE TABLE IF NOT EXISTS `v_video` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `desc` varchar(4096) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `classification_id` int DEFAULT NULL,
  `file` varchar(255) NOT NULL,
  `cover` varchar(255) DEFAULT NULL,
  `status` char(1) DEFAULT NULL,
  `view_count` int DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4;

-- video.v_video_collected definition
CREATE TABLE IF NOT EXISTS `v_video_collected` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `video_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

-- video.v_video_liked definition
CREATE TABLE IF NOT EXISTS `v_video_liked` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `video_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

-- video.auth_permission definition
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
LOCK TABLES `auth_permission` WRITE;

INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add kv store',6,'add_kvstore'),(22,'Can change kv store',6,'change_kvstore'),(23,'Can delete kv store',6,'delete_kvstore'),(24,'Can view kv store',6,'view_kvstore'),(25,'Can add video',7,'add_video'),(26,'Can change video',7,'change_video'),(27,'Can delete video',7,'delete_video'),(28,'Can view video',7,'view_video'),(29,'Can add classification',8,'add_classification'),(30,'Can change classification',8,'change_classification'),(31,'Can delete classification',8,'delete_classification'),(32,'Can view classification',8,'view_classification'),(33,'Can add user',9,'add_user'),(34,'Can change user',9,'change_user'),(35,'Can delete user',9,'delete_user'),(36,'Can view user',9,'view_user'),(37,'Can add feedback',10,'add_feedback'),(38,'Can change feedback',10,'change_feedback'),(39,'Can delete feedback',10,'delete_feedback'),(40,'Can view feedback',10,'view_feedback'),(41,'Can add my chunked upload',11,'add_mychunkedupload'),(42,'Can change my chunked upload',11,'change_mychunkedupload'),(43,'Can delete my chunked upload',11,'delete_mychunkedupload'),(44,'Can view my chunked upload',11,'view_mychunkedupload'),(45,'Can add comment',12,'add_comment'),(46,'Can change comment',12,'change_comment'),(47,'Can delete comment',12,'delete_comment'),(48,'Can view comment',12,'view_comment');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

-- video.django_admin_log definition
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_v_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_v_user_id` FOREIGN KEY (`user_id`) REFERENCES `v_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4;

-- video.auth_group_permissions definition
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;