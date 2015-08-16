-- --------------------------------------------------------
-- Host:                         192.168.1.2
-- Server version:               5.5.44-0+deb7u1-log - (Debian)
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             9.3.0.4984
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping database structure for icemelt
DROP DATABASE IF EXISTS `icemelt`;
CREATE DATABASE IF NOT EXISTS `icemelt` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `icemelt`;


-- Dumping structure for table icemelt.chars
DROP TABLE IF EXISTS `chars`;
CREATE TABLE IF NOT EXISTS `chars` (
  `cid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `gid` int(11) unsigned DEFAULT NULL,
  `rid` tinyint(3) unsigned NOT NULL,
  `toon_name` varchar(15) NOT NULL,
  `lvl` tinyint(3) unsigned NOT NULL,
  `realm` varchar(256) NOT NULL,
  `updaded` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `class` varchar(50) DEFAULT NULL,
  `spec` varchar(50) DEFAULT NULL,
  `status` smallint(5) unsigned DEFAULT NULL,
  `fid` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`cid`),
  KEY `FK_chars_regions` (`rid`),
  KEY `FK_chars_guilds` (`gid`),
  CONSTRAINT `FK_chars_guilds` FOREIGN KEY (`gid`) REFERENCES `guilds` (`index`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `FK_chars_regions` FOREIGN KEY (`rid`) REFERENCES `regions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table icemelt.checksum
DROP TABLE IF EXISTS `checksum`;
CREATE TABLE IF NOT EXISTS `checksum` (
  `table` varchar(20) DEFAULT NULL,
  `checksum` mediumint(10) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='database integraty info';

-- Data exporting was unselected.


-- Dumping structure for table icemelt.guilds
DROP TABLE IF EXISTS `guilds`;
CREATE TABLE IF NOT EXISTS `guilds` (
  `index` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `guild` varchar(64) NOT NULL,
  `region_id` tinyint(3) unsigned NOT NULL,
  `realm` varchar(64) NOT NULL,
  `status` int(11) DEFAULT NULL,
  `fid` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '1 = Ally 2 = Horde',
  PRIMARY KEY (`index`),
  UNIQUE KEY `Unique_Per_Realm` (`guild`,`realm`),
  KEY `FK_guilds_regions` (`region_id`),
  CONSTRAINT `FK_guilds_regions` FOREIGN KEY (`region_id`) REFERENCES `regions` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table icemelt.regions
DROP TABLE IF EXISTS `regions`;
CREATE TABLE IF NOT EXISTS `regions` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

