CREATE SCHEMA IF NOT EXISTS `agenda_web` DEFAULT CHARACTER SET utf8mb4 ;
USE `agenda_web` ;

-- -----------------------------------------------------
-- Table `agenda_web`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agenda_web`.`usuario` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NULL DEFAULT NULL,
  `email` VARCHAR(100) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `agenda_web`.`contacto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agenda_web`.`contacto` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NULL DEFAULT NULL,
  `telefono` VARCHAR(20) NULL DEFAULT NULL,
  `email` VARCHAR(100) NULL DEFAULT NULL,
  `usuario_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `usuario_id` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `contacto_ibfk_1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `agenda_web`.`usuario` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4;
