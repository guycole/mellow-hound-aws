SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `mellow_hound_v1` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `mellow_hound_v1` ;

-- -----------------------------------------------------
-- Table `mellow_hound_v1`.`geo_loc`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mellow_hound_v1`.`geo_loc` ;

CREATE  TABLE IF NOT EXISTS `mellow_hound_v1`.`geo_loc` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `observation_id` BIGINT UNSIGNED NOT NULL ,
  `time_stamp` TIMESTAMP NOT NULL ,
  `provider` VARCHAR(32) NOT NULL ,
  `accuracy` DOUBLE NOT NULL ,
  `altitude` DOUBLE NOT NULL ,
  `latitude` DOUBLE NOT NULL ,
  `longitude` DOUBLE NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mellow_hound_v1`.`installation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mellow_hound_v1`.`installation` ;

CREATE  TABLE IF NOT EXISTS `mellow_hound_v1`.`installation` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `uuid` VARCHAR(48) NOT NULL ,
  `phone_line` VARCHAR(16) NOT NULL ,
  `platform` VARCHAR(32) NOT NULL ,
  `device` VARCHAR(48) NOT NULL ,
  `note` VARCHAR(128) NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) ,
  UNIQUE INDEX `ndx1` (`uuid` ASC) ,
  INDEX `ndx2` (`phone_line` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mellow_hound_v1`.`ble`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mellow_hound_v1`.`ble` ;

CREATE  TABLE IF NOT EXISTS `mellow_hound_v1`.`ble` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `observation_id` BIGINT UNSIGNED NOT NULL ,
  `address` VARCHAR(48) NOT NULL ,
  `name` VARCHAR(48) NOT NULL ,
  `rssi` INT NOT NULL ,
  `raw_scan` VARCHAR(256) NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) ,
  INDEX `ndx1` (`address` ASC, `name` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mellow_hound_v1`.`wcdma`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mellow_hound_v1`.`wcdma` ;

CREATE  TABLE IF NOT EXISTS `mellow_hound_v1`.`wcdma` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `observation_id` BIGINT UNSIGNED NOT NULL ,
  `register_flag` TINYINT(1) NOT NULL ,
  `cid` INT NOT NULL ,
  `lac` INT NOT NULL ,
  `mcc` INT NOT NULL ,
  `mnc` INT NOT NULL ,
  `psc` INT NOT NULL ,
  `uarfcn` INT NOT NULL ,
  `asu_level` INT NOT NULL ,
  `dbm` INT NOT NULL ,
  `level` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mellow_hound_v1`.`wifi`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mellow_hound_v1`.`wifi` ;

CREATE  TABLE IF NOT EXISTS `mellow_hound_v1`.`wifi` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `observation_id` BIGINT UNSIGNED NOT NULL ,
  `frequency` INT NOT NULL ,
  `level` INT NOT NULL ,
  `ssid` VARCHAR(128) NOT NULL ,
  `bssid` VARCHAR(128) NOT NULL ,
  `capability` VARCHAR(128) NOT NULL ,
  `passpoint_name` VARCHAR(64) NOT NULL ,
  `passpoint_venue` VARCHAR(64) NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) ,
  INDEX `ndx1` (`observation_id` ASC) ,
  INDEX `ndx2` (`ssid` ASC, `bssid` ASC) ,
  INDEX `ndx3` (`passpoint_name` ASC, `passpoint_venue` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mellow_hound_v1`.`observation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mellow_hound_v1`.`observation` ;

CREATE  TABLE IF NOT EXISTS `mellow_hound_v1`.`observation` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `installation_id` BIGINT UNSIGNED NOT NULL ,
  `sortie_id` BIGINT UNSIGNED NOT NULL ,
  `network_name` VARCHAR(48) NOT NULL ,
  `network_operator` VARCHAR(48) NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mellow_hound_v1`.`load_log`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mellow_hound_v1`.`load_log` ;

CREATE  TABLE IF NOT EXISTS `mellow_hound_v1`.`load_log` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `task_id` BIGINT UNSIGNED NOT NULL ,
  `observation_id` BIGINT UNSIGNED NOT NULL ,
  `version` INT NOT NULL ,
  `file_name` VARCHAR(64) NOT NULL ,
  `ble_pop` INT NOT NULL ,
  `cell_cdma_pop` INT NOT NULL ,
  `cell_gsm_pop` INT NOT NULL ,
  `cell_lte_pop` INT NOT NULL ,
  `cell_wcdma_pop` INT NOT NULL ,
  `wifi_pop` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mellow_hound_v1`.`census`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mellow_hound_v1`.`census` ;

CREATE  TABLE IF NOT EXISTS `mellow_hound_v1`.`census` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `time_stamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ,
  `population` BIGINT NOT NULL ,
  `table` VARCHAR(64) NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mellow_hound_v1`.`cdma`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mellow_hound_v1`.`cdma` ;

CREATE  TABLE IF NOT EXISTS `mellow_hound_v1`.`cdma` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `observation_id` BIGINT UNSIGNED NOT NULL ,
  `register_flag` TINYINT(1) NOT NULL ,
  `base_station` INT NOT NULL ,
  `latitude` INT NOT NULL ,
  `longitude` INT NOT NULL ,
  `network` INT NOT NULL ,
  `system` INT NOT NULL ,
  `asu_level` INT NOT NULL ,
  `cdma_dbm` INT NOT NULL ,
  `cdma_ecio` INT NOT NULL ,
  `cdma_level` INT NOT NULL ,
  `dbm` INT NOT NULL ,
  `evdo_dbm` INT NOT NULL ,
  `evdo_ecio` INT NOT NULL ,
  `evdo_level` INT NOT NULL ,
  `evdo_snr` INT NOT NULL ,
  `level` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mellow_hound_v1`.`gsm`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mellow_hound_v1`.`gsm` ;

CREATE  TABLE IF NOT EXISTS `mellow_hound_v1`.`gsm` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `observation_id` BIGINT UNSIGNED NOT NULL ,
  `register_flag` TINYINT(1) NOT NULL ,
  `arfcn` INT NOT NULL ,
  `bsic` INT NOT NULL ,
  `cid` INT NOT NULL ,
  `lac` INT NOT NULL ,
  `mcc` INT NOT NULL ,
  `mnc` INT NOT NULL ,
  `psc` INT NOT NULL ,
  `asu_level` INT NOT NULL ,
  `dbm` INT NOT NULL ,
  `level` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mellow_hound_v1`.`lte`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mellow_hound_v1`.`lte` ;

CREATE  TABLE IF NOT EXISTS `mellow_hound_v1`.`lte` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `observation_id` VARCHAR(45) NOT NULL ,
  `register_flag` VARCHAR(45) NOT NULL ,
  `ci` INT NOT NULL ,
  `earfcn` INT NOT NULL ,
  `mcc` INT NOT NULL ,
  `mnc` INT NOT NULL ,
  `pci` INT NOT NULL ,
  `tac` INT NOT NULL ,
  `asu_level` INT NOT NULL ,
  `dbm` INT NOT NULL ,
  `level` INT NOT NULL ,
  `timing_advance` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mellow_hound_v1`.`application_log`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mellow_hound_v1`.`application_log` ;

CREATE  TABLE IF NOT EXISTS `mellow_hound_v1`.`application_log` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `task_id` BIGINT UNSIGNED NOT NULL ,
  `time_stamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ,
  `level` INT NOT NULL ,
  `facility` VARCHAR(32) NOT NULL ,
  `event` VARCHAR(128) NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mellow_hound_v1`.`task_log`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mellow_hound_v1`.`task_log` ;

CREATE  TABLE IF NOT EXISTS `mellow_hound_v1`.`task_log` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `time_stamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ,
  `command` VARCHAR(128) NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;

USE `mellow_hound_v1` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
