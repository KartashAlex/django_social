
# all of your evolution scripts, mapping the from_version and to_version to a list if sql commands
sqlite3_evolutions = [
    [('fv1:1518106188','fv1:-1406536048'), # generated 2008-08-11 09:03:21.003008
        "CREATE TABLE \"wall_message\" (\n    \"id\" integer NOT NULL PRIMARY KEY,\n    \"from_user_id\" integer NOT NULL REFERENCES \"net_user\" (\"user_ptr_id\"),\n    \"subject\" varchar(255) NOT NULL,\n    \"body\" text NOT NULL,\n    \"private\" bool NOT NULL,\n    \"sent\" datetime NOT NULL,\n    \"parent_id\" integer NULL,\n    \"content_type_id\" integer NOT NULL REFERENCES \"django_content_type\" (\"id\"),\n    \"object_id\" integer NOT NULL\n)\n;",
    ],
    [('fv1:-407686107','fv1:-1083771525'), # generated 2008-09-10 13:06:27.675002
        "-- FYI: sqlite does not support changing columns",
        "-- warning: the following may cause data loss",
        "-- FYI: sqlite does not support deleting columns",
        "-- end warning",
        "-- FYI: so we create a new \"wall_message\" and delete the old ",
        "-- FYI: this could take a while if you have a lot of data",
        "ALTER TABLE \"wall_message\" RENAME TO \"wall_message_1337_TMP\";",
        "CREATE TABLE \"wall_message\" (\n    \"id\" integer NOT NULL PRIMARY KEY,\n    \"from_user_id\" integer NOT NULL,\n    \"body\" text NOT NULL,\n    \"private\" bool NOT NULL,\n    \"sent\" datetime NOT NULL,\n    \"parent_id\" integer NULL REFERENCES \"wall_message\" (\"id\"),\n    \"content_type_id\" integer NOT NULL,\n    \"object_id\" integer NOT NULL\n)\n;",
        "INSERT INTO \"wall_message\" SELECT \"id\",\"from_user_id\",\"body\",\"private\",\"sent\",\"parent_id\",\"content_type_id\",\"object_id\" FROM \"wall_message_1337_TMP\";",
        "DROP TABLE \"wall_message_1337_TMP\";",
        "-- FYI: sqlite does not support changing columns",
        "-- FYI: so we create a new \"wall_adcategory\" and delete the old ",
        "-- FYI: this could take a while if you have a lot of data",
        "ALTER TABLE \"wall_adcategory\" RENAME TO \"wall_adcategory_1337_TMP\";",
        "CREATE TABLE \"wall_adcategory\" (\n    \"id\" integer NOT NULL PRIMARY KEY,\n    \"name\" varchar(255) NOT NULL\n)\n;",
        "INSERT INTO \"wall_adcategory\" SELECT \"id\",\"name\" FROM \"wall_adcategory_1337_TMP\";",
        "DROP TABLE \"wall_adcategory_1337_TMP\";",
        "-- FYI: sqlite does not support changing columns",
        "-- FYI: so we create a new \"wall_post\" and delete the old ",
        "-- FYI: this could take a while if you have a lot of data",
        "ALTER TABLE \"wall_post\" RENAME TO \"wall_post_1337_TMP\";",
        "CREATE TABLE \"wall_post\" (\n    \"id\" integer NOT NULL PRIMARY KEY,\n    \"subject\" varchar(255) NULL,\n    \"body\" text NOT NULL,\n    \"is_ad\" bool NOT NULL,\n    \"ad_cat_id\" integer NULL REFERENCES \"wall_adcategory\" (\"id\"),\n    \"author_id\" integer NOT NULL,\n    \"added\" datetime NULL\n)\n;",
        "INSERT INTO \"wall_post\" SELECT \"id\",\"subject\",\"body\",\"is_ad\",\"ad_cat_id\",\"author_id\",\"added\" FROM \"wall_post_1337_TMP\";",
        "DROP TABLE \"wall_post_1337_TMP\";",
    ],
] # don't delete this comment! ## sqlite3_evolutions_end ##
