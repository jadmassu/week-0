DROP TABLE IF EXISTS `SlackInformation`;
CREATE TABLE IF NOT EXISTS `SlackInformation` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `msg_type` VARCHAR(200) NOT NULL,
    `user` VARCHAR(200) NOT NULL,
    `msg_content` VARCHAR(255) NOT NULL,
    `sender_name` VARCHAR(200) NOT NULL,
    `msg_sent_time` VARCHAR(200) NOT NULL,
    `msg_dist_type` VARCHAR(200) NOT NULL,
    `time_thread_start` VARCHAR(200) NOT NULL,
    `reply_count` VARCHAR(200) NOT NULL,
    `reply_users_count` VARCHAR(200) NOT NULL,
    `reply_users` VARCHAR(200) NOT NULL,
    `tm_thread_end` VARCHAR(200) NOT NULL,
    `channel` VARCHAR(200) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb3 COLLATE = utf8mb3_unicode_ci;