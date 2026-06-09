/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 5.7.9 : Database - mockinterview
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`mockinterview` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `mockinterview`;

/*Table structure for table `answer` */

DROP TABLE IF EXISTS `answer`;

CREATE TABLE `answer` (
  `answer_id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) DEFAULT NULL,
  `correct_answer` varchar(50) DEFAULT NULL,
  `user_answer` varchar(50) DEFAULT NULL,
  `score` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`answer_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `answer` */

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` int(11) DEFAULT NULL,
  `complaint` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `reply` varchar(50) DEFAULT NULL,
  KEY `complaint_id` (`complaint_id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`complaint_id`,`sender_id`,`complaint`,`date`,`reply`) values 
(1,1,'gfg','77','hii'),
(2,8,'ddd','2024-12-07','pending'),
(3,8,'ddd','2024-12-07','ok'),
(4,8,'helooi','2024-12-19','pending'),
(5,8,'','2024-12-27','pending'),
(6,8,'','2024-12-27','pending'),
(7,8,'','2024-12-27','pending'),
(8,8,'','2024-12-27','pending'),
(9,8,'ghjk','2024-12-31','pending'),
(10,8,'','2024-12-31','pending'),
(11,8,'','2024-12-31','pending'),
(12,8,'','2024-12-31','pending'),
(13,8,'','2024-12-31','pending'),
(14,8,'','2024-12-31','pending'),
(15,8,'jjjjjjj','2025-01-03','pending'),
(16,8,'bgb','2025-01-03','pending'),
(17,8,'alannn','2025-02-01','jerry');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(60) DEFAULT NULL,
  `password` varchar(15) DEFAULT NULL,
  `usertype` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'admin','admin','admin'),
(2,'savith','12345644','user'),
(3,'Salma','salma123','user'),
(4,'Aadhi','aaadhi@123','user'),
(5,'Aadhi','aadhi123','user'),
(6,'JJ','j@123','user'),
(7,'JJ','ffggthujj','user'),
(8,'vishnuu','2224556788','user'),
(9,'vishnuu','4455566','user'),
(10,'vishnuu','4455566','user'),
(11,'user','1234','user'),
(12,'user','1234','user'),
(13,'user','1234','user');

/*Table structure for table `notification` */

DROP TABLE IF EXISTS `notification`;

CREATE TABLE `notification` (
  `notification_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) DEFAULT NULL,
  `description` varchar(50) DEFAULT NULL,
  `date_time` varchar(50) DEFAULT NULL,
  KEY `notification_id` (`notification_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `notification` */

insert  into `notification`(`notification_id`,`title`,`description`,`date_time`) values 
(1,'bcgc','hnghn','2024-11-01'),
(2,'dfgh','sdf','2024-11-01'),
(3,'','','2024-12-19'),
(4,'hi','hello','2024-12-31');

/*Table structure for table `question` */

DROP TABLE IF EXISTS `question`;

CREATE TABLE `question` (
  `question_id` int(11) NOT NULL AUTO_INCREMENT,
  `question_text` varchar(50) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`question_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `question` */

/*Table structure for table `role` */

DROP TABLE IF EXISTS `role`;

CREATE TABLE `role` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`role_id`),
  KEY `role_id` (`role_id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

/*Data for the table `role` */

insert  into `role`(`role_id`,`role_name`) values 
(12,'appleeeee'),
(15,'hiiii');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `User_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `fname` varchar(50) DEFAULT NULL,
  `lname` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `phone` int(11) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`User_id`),
  KEY `User_id` (`User_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`User_id`,`login_id`,`fname`,`lname`,`place`,`phone`,`email`) values 
(1,2,'savith','narayan','Thiruvathra',1222334214,'setama9116@bsomek.com'),
(2,3,'salma','basheer','thrissur',1234567890,'salma@gmail.com'),
(3,5,'aadhi','tb','paang',678905432,'aadhi@gmail.com'),
(4,7,'jeeson','jj','peringottukara',1233432145,'jj@gmail.com'),
(5,8,'vishnu','prasad','vaka',1234567890,'vaka@gmail.com'),
(6,9,'vishnu','prasad','vaka',123456788,'vaka111@gmail.com'),
(7,10,'vishnu','prasad','vaka',123456788,'vaka111@gmail.com'),
(8,11,'vishnurr','prasad','vaka',23456789,'vaka111@gmail.com'),
(9,13,'vishnu','prasad','yy',456789,'vaka@gmail.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
