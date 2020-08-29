-- MySQL dump 10.13  Distrib 5.7.31, for Linux (x86_64)
--
-- Host: localhost    Database: dcjeil_prod
-- ------------------------------------------------------
-- Server version	5.7.31-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `data_submenu`
--

DROP TABLE IF EXISTS `data_submenu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_submenu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `order` int(11) NOT NULL,
  `mainmenu_id` int(11) NOT NULL,
  `m_type` varchar(50) NOT NULL,
  `is_allowed_to_not_superuser` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `data_submenu_mainmenu_id_0279633b_fk_data_mainmenu_id` (`mainmenu_id`),
  CONSTRAINT `data_submenu_mainmenu_id_0279633b_fk_data_mainmenu_id` FOREIGN KEY (`mainmenu_id`) REFERENCES `data_mainmenu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_submenu`
--

LOCK TABLES `data_submenu` WRITE;
/*!40000 ALTER TABLE `data_submenu` DISABLE KEYS */;
INSERT INTO `data_submenu` VALUES (1,'인사말',1,1,'fixed',0),(2,'교회연혁',2,1,'fixed',0),(3,'우리의 비젼',3,1,'fixed',0),(4,'담임목사소개',4,1,'fixed',0),(5,'섬기는 사람들',5,1,'fixed',0),(6,'찾아오시는 길',6,1,'fixed',0),(7,'금주의 말씀',1,2,'list',0),(8,'주일오후예배',2,2,'list',0),(9,'수요예배',3,2,'list',0),(10,'금요철야예배',4,2,'list',0),(11,'새벽기도',5,2,'list',0),(12,'부흥회',6,2,'list',0),(13,'예배안내',7,2,'fixed',0),(14,'할렐루야 찬양대',1,3,'list',0),(15,'호산나 찬양대',2,3,'list',0),(16,'찬양, 간증 집회',3,3,'list',0),(17,'공지사항',1,4,'list',0),(18,'교회소식',2,4,'list',0),(19,'교우소식',3,4,'list',0),(20,'새가족소개',4,4,'piclist',0),(21,'교회앨범',5,4,'piclist',0),(22,'자유게시판',6,4,'list',0),(23,'기도요청',7,4,'list',0),(24,'행사동영상',8,4,'list',0),(25,'큐티나눔방',9,4,'list',0),(26,'영아부',1,5,'fixed',0),(27,'유치부',2,5,'fixed',0),(28,'유년부',3,5,'fixed',0),(29,'초등부',4,5,'fixed',0),(30,'중등부',5,5,'fixed',0),(31,'고등부',6,5,'fixed',0),(32,'사랑부',7,5,'fixed',0),(33,'청년1부',8,5,'fixed',0),(34,'청년2부',9,5,'fixed',0),(35,'청년3부',10,5,'fixed',0),(36,'선교위원회',1,6,'list',0),(37,'국내선교',2,6,'list',0),(38,'아시아',3,6,'list',0),(39,'아프리카',4,6,'list',0),(40,'기타',5,6,'list',0),(41,'단기선교',6,6,'list',0),(42,'양육시스템',1,7,'fixed',0),(43,'새가족부 자료실',2,7,'list',0),(44,'확신반 자료실',3,7,'list',0),(45,'문서자료실',1,8,'list',0),(46,'기타자료실',2,8,'list',0),(47,'주보자료실',3,8,'list',0);
/*!40000 ALTER TABLE `data_submenu` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-28 12:07:49
