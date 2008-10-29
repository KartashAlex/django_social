
# all of your evolution scripts, mapping the from_version and to_version to a list if sql commands
sqlite3_evolutions = [
    [('fv1:-1548750438','fv1:-129256085'), # generated 2008-09-10 13:06:24.483881
        "-- FYI: sqlite does not support changing columns",
        "-- FYI: so we create a new \"photo_album\" and delete the old ",
        "-- FYI: this could take a while if you have a lot of data",
        "ALTER TABLE \"photo_album\" RENAME TO \"photo_album_1337_TMP\";",
        "CREATE TABLE \"photo_album\" (\n    \"id\" integer NOT NULL PRIMARY KEY,\n    \"user_id\" integer NOT NULL,\n    \"title\" varchar(255) NOT NULL\n)\n;",
        "INSERT INTO \"photo_album\" SELECT \"id\",\"user_id\",\"title\" FROM \"photo_album_1337_TMP\";",
        "DROP TABLE \"photo_album_1337_TMP\";",
        "-- FYI: sqlite does not support changing columns",
        "ALTER TABLE \"photo_photo\" ADD COLUMN \"added\" datetime NULL",
        "-- FYI: so we create a new \"photo_photo\" and delete the old ",
        "-- FYI: this could take a while if you have a lot of data",
        "ALTER TABLE \"photo_photo\" RENAME TO \"photo_photo_1337_TMP\";",
        "CREATE TABLE \"photo_photo\" (\n    \"id\" integer NOT NULL PRIMARY KEY,\n    \"album_id\" integer NOT NULL REFERENCES \"photo_album\" (\"id\"),\n    \"title\" varchar(255) NOT NULL,\n    \"image\" varchar(100) NOT NULL,\n    \"added\" datetime NULL\n)\n;",
        "INSERT INTO \"photo_photo\" SELECT \"id\",\"album_id\",\"title\",\"image\",'' FROM \"photo_photo_1337_TMP\";",
        "DROP TABLE \"photo_photo_1337_TMP\";",
    ],
] # don't delete this comment! ## sqlite3_evolutions_end ##
