CREATE TABLE query (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` TEXT NOT NULL UNIQUE,
  `processed` BOOL NOT NULL
  );

CREATE TABLE `suggestion` (
  `id` integer PRIMARY KEY AUTOINCREMENT,
  `name` TEXT ( 255 ) NOT NULL,
  `suggestion_query` CHAR ( 3 ) NOT NULL,
  UNIQUE(name, suggestion_query),
  FOREIGN KEY(`suggestion_query`) REFERENCES `query`(`name`) ON DELETE CASCADE
  );
