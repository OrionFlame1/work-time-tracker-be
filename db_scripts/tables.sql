CREATE TABLE IF NOT EXISTS work_time_tracker.accounts (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `firstname` varchar(255),
  `lastname` varchar(255),
  `email` varchar(255),
  `password` varchar(255) COMMENT 'SHA-256 encryption',
  `type` varchar(255) COMMENT 'employee/admin'
);

CREATE TABLE IF NOT EXISTS work_time_tracker.timecards (
  `id` integer PRIMARY KEY,
  `account_id` integer,
  `check_in` timestamp,
  `check_out` timestamp
);

CREATE TABLE IF NOT EXISTS work_time_tracker.tasks (
  `id` integer PRIMARY KEY,
  `account_id` integer,
  `task_name` varchar(255),
  `task_desc` text,
  `status` varchar(255) COMMENT 'unassigned/work-in-progress/complete',
  `created_at` timestamp,
  `finished_at` timestamp
);

ALTER TABLE work_time_tracker.timecards ADD FOREIGN KEY (`account_id`) REFERENCES work_time_tracker.accounts (`id`);

ALTER TABLE work_time_tracker.tasks ADD FOREIGN KEY (`account_id`) REFERENCES work_time_tracker.accounts (`id`);