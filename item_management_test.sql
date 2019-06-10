-- MySQL dump 10.13  Distrib 8.0.16, for macos10.14 (x86_64)
--
-- Host: localhost    Database: item_management
-- ------------------------------------------------------
-- Server version	8.0.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `created_on` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_on` datetime DEFAULT CURRENT_TIMESTAMP,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Running','2019-06-04 16:16:33','2019-06-04 16:29:01',1),(2,'Climbing','2019-06-04 16:17:44','2019-06-05 04:32:59',1),(3,'Football','2019-06-04 16:18:01','2019-06-04 16:18:01',1),(21,'Football1','2019-06-05 10:21:42','2019-06-05 10:21:42',1),(22,'Foot ball','2019-06-05 10:22:14','2019-06-05 10:22:14',1),(23,'Football123','2019-06-06 12:42:21','2019-06-06 12:42:21',1);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(30) NOT NULL,
  `description` text,
  `created_on` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_on` datetime DEFAULT CURRENT_TIMESTAMP,
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `items_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (1,'Cl1',NULL,'2019-06-04 16:18:47','2019-06-04 16:18:47',2,1),(2,'Cl2',NULL,'2019-06-04 16:18:51','2019-06-04 16:18:51',2,1),(3,'Cl3',NULL,'2019-06-04 16:18:54','2019-06-04 16:18:54',2,1),(4,'dab','a gesture er','2019-06-04 16:27:52','2019-06-06 13:44:03',2,1),(5,'Cl5',NULL,'2019-06-04 16:27:56','2019-06-04 16:27:56',2,1),(6,'Cl6',NULL,'2019-06-04 16:27:59','2019-06-04 16:27:59',2,1),(7,'Ru1',NULL,'2019-06-04 16:29:43','2019-06-04 16:29:43',1,1),(8,'Ru2',NULL,'2019-06-04 16:29:47','2019-06-04 16:29:47',1,1),(9,'Ru3',NULL,'2019-06-04 16:29:53','2019-06-04 16:29:53',1,1),(10,'Cl7',NULL,'2019-06-04 16:30:10','2019-06-04 16:30:10',2,1),(11,'Sporty',NULL,'2019-06-05 03:41:24','2019-06-05 03:41:24',2,1),(12,'Skating shoe',NULL,'2019-06-05 03:41:24','2019-06-05 03:41:24',2,1),(14,'whatever1',NULL,'2019-06-05 04:02:52','2019-06-05 04:02:52',2,1),(17,'whatever2',NULL,'2019-06-05 04:11:19','2019-06-05 04:11:19',2,1);
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `password_hash` varchar(87) NOT NULL,
  `created_on` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_on` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'nam123','$pbkdf2-sha256$29000$g1BqTYkxRgghJISwttYaQw$kAPHqD/DYGoLCWjie13Z5uHPDelZSZFJVPuMn.jwINU','2019-06-04 16:09:56','2019-06-04 16:09:56'),(2,'nam1234','$pbkdf2-sha256$29000$GQPAeO89x/jfu5dyDmHMWQ$sknEvwIbCZuMzOY4EE.GduDygtKQPwdJhirwRD/tIEg','2019-06-04 16:16:16','2019-06-04 16:16:16'),(51,'nam12345','$pbkdf2-sha256$29000$FKL0XosxxjjHmHPuvXcuJQ$Qo3VWF35OErpneALKFEFj1smNlw.zTi.XpkMArhhkRY','2019-06-05 10:19:11','2019-06-05 10:19:11'),(52,'namwer','$pbkdf2-sha256$29000$ZSyFMCZkjNEao3QupVSqdQ$Tp20Tbzux.vqIuvtj4/7rnti6ecAN4tqOn7auUOgBRk','2019-06-06 13:40:02','2019-06-06 13:40:02');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-10  3:33:51
