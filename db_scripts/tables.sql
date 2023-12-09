CREATE TABLE IF NOT EXISTS work_time_tracker.accounts (
  `id` integer NOT NULL AUTO_INCREMENT,
  `firstname` varchar(255),
  `lastname` varchar(255),
  `email` varchar(255),
  `password` varchar(255) COMMENT 'SHA-256 encryption',
  `type` varchar(255) COMMENT 'employee/admin',
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS work_time_tracker.timecards (
  `id` integer NOT NULL AUTO_INCREMENT,
  `account_id` integer,
  `check_in` timestamp,
  `check_out` timestamp,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS work_time_tracker.tasks (
  `id` integer NOT NULL AUTO_INCREMENT,
  `account_id` integer,
  `task_name` varchar(255),
  `task_desc` text,
  `status` varchar(255) COMMENT 'unassigned/work-in-progress/complete',
  `created_at` timestamp,
  `finished_at` timestamp,
  PRIMARY KEY (id)
);

ALTER TABLE work_time_tracker.timecards ADD FOREIGN KEY (`account_id`) REFERENCES work_time_tracker.accounts (`id`);

ALTER TABLE work_time_tracker.tasks ADD FOREIGN KEY (`account_id`) REFERENCES work_time_tracker.accounts (`id`);