/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for work_time_tracker
CREATE DATABASE IF NOT EXISTS `work_time_tracker` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `work_time_tracker`;

-- Dumping structure for table work_time_tracker.accounts
CREATE TABLE IF NOT EXISTS `accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL COMMENT 'SHA-256 encryption',
  `type` varchar(255) DEFAULT NULL COMMENT 'employee/admin',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table work_time_tracker.accounts: ~2 rows (approximately)
INSERT INTO `accounts` (`id`, `firstname`, `lastname`, `email`, `password`, `type`) VALUES
	(1, 'Toma', 'Adrian', 'aditoma123@gmail.com', '1234', 'admin'),
	(2, 'Employee', 'Number One', 'employeenumber1@company.com', 'employee1', 'employee');

-- Dumping structure for table work_time_tracker.tasks
CREATE TABLE IF NOT EXISTS `tasks` (
  `id` int(11) NOT NULL,
  `account_id` int(11) DEFAULT NULL,
  `task_name` varchar(255) DEFAULT NULL,
  `task_desc` text DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL COMMENT 'unassigned/work-in-progress/complete',
  `created_at` timestamp NULL DEFAULT NULL,
  `finished_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table work_time_tracker.tasks: ~0 rows (approximately)

-- Dumping structure for table work_time_tracker.timecards
CREATE TABLE IF NOT EXISTS `timecards` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) DEFAULT NULL,
  `check_in` timestamp NULL DEFAULT NULL,
  `check_out` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `timecards_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table work_time_tracker.timecards: ~2 rows (approximately)
INSERT INTO `timecards` (`id`, `account_id`, `check_in`, `check_out`) VALUES
	(6, 1, '2023-12-10 08:33:29', '2023-12-10 08:33:29'),
	(7, 1, '2023-12-10 08:33:29', '2023-12-10 08:33:29');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
