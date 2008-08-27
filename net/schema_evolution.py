
# all of your evolution scripts, mapping the from_version and to_version to a list if sql commands
mysql_evolutions = [
    [('fv1:-1737118284','fv1:-37353995'), # generated 2008-08-27 12:20:13.528273
        "CREATE TABLE `net_userdata` (\n    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,\n    `type` varchar(15) NOT NULL,\n    `title` varchar(511) NOT NULL\n)\n;",
        "CREATE TABLE `net_user` (\n    `user_ptr_id` integer NOT NULL PRIMARY KEY,\n    `avatar` varchar(100) NULL,\n    `country_id` integer NULL,\n    `city_id` integer NULL,\n    `birthdate` date NULL,\n    `gender` varchar(10) NULL,\n    `about` longtext NOT NULL,\n    `contacts` longtext NOT NULL,\n    `interest` longtext NOT NULL,\n    `writer` longtext NOT NULL,\n    `site` longtext NOT NULL,\n    `private` longtext NOT NULL\n)\n;",
        "CREATE TABLE `net_place` (\n    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,\n    `user_id` integer NOT NULL,\n    `type_id` integer NOT NULL,\n    `name` varchar(255) NOT NULL,\n    `city_id` integer NULL,\n    `address` longtext NULL,\n    `map_link` varchar(200) NULL,\n    `from_date` date NULL,\n    `to_date` date NULL\n)\n;",
        "ALTER TABLE `net_placetype` MODIFY COLUMN `id` integer AUTO_INCREMENT;",
        "CREATE TABLE `net_user_user_data` (\n    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,\n    `user_id` integer NOT NULL REFERENCES `net_user` (`user_ptr_id`),\n    `userdata_id` integer NOT NULL REFERENCES `net_userdata` (`id`),\n    UNIQUE (`user_id`, `userdata_id`)\n)\n;",
    ],
] # don't delete this comment! ## mysql_evolutions_end ##
