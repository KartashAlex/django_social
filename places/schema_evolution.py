
# all of your evolution scripts, mapping the from_version and to_version to a list if sql commands
sqlite3_evolutions = [
    [('fv1:1279624373','fv1:633343014'), # generated 2008-07-24 15:36:29.680425
        "-- FYI: sqlite does not support changing columns",
        "-- FYI: so we create a new \"places_country\" and delete the old ",
        "-- FYI: this could take a while if you have a lot of data",
        "ALTER TABLE \"places_country\" RENAME TO \"places_country_1337_TMP\";",
        "CREATE TABLE \"places_country\" (\n    \"id\" integer NOT NULL PRIMARY KEY,\n    \"name\" varchar(255) NOT NULL\n)\n;",
        "INSERT INTO \"places_country\" SELECT \"id\",\"name\" FROM \"places_country_1337_TMP\";",
        "DROP TABLE \"places_country_1337_TMP\";",
        "-- FYI: sqlite does not support changing columns",
        "-- FYI: so we create a new \"places_city\" and delete the old ",
        "-- FYI: this could take a while if you have a lot of data",
        "ALTER TABLE \"places_city\" RENAME TO \"places_city_1337_TMP\";",
        "CREATE TABLE \"places_city\" (\n    \"id\" integer NOT NULL PRIMARY KEY,\n    \"country_id\" integer NOT NULL REFERENCES \"places_country\" (\"id\"),\n    \"name\" varchar(255) NOT NULL\n)\n;",
        "INSERT INTO \"places_city\" SELECT \"id\",\"country_id\",\"name\" FROM \"places_city_1337_TMP\";",
        "DROP TABLE \"places_city_1337_TMP\";",
        "-- FYI: sqlite does not support changing columns",
        "-- FYI: sqlite does not support adding primary keys or unique or not null fields",
        "-- FYI: so we create a new \"places_place\" and delete the old ",
        "-- FYI: this could take a while if you have a lot of data",
        "ALTER TABLE \"places_place\" RENAME TO \"places_place_1337_TMP\";",
        "CREATE TABLE \"places_place\" (\n    \"id\" integer NOT NULL PRIMARY KEY,\n    \"name\" varchar(255) NOT NULL,\n    \"city_id\" integer NOT NULL REFERENCES \"places_city\" (\"id\"),\n    \"address\" text NOT NULL,\n    \"map_link\" varchar(200) NOT NULL\n)\n;",
        "INSERT INTO \"places_place\" SELECT \"id\",'',\"city_id\",\"address\",\"map_link\" FROM \"places_place_1337_TMP\";",
        "DROP TABLE \"places_place_1337_TMP\";",
    ],
] # don't delete this comment! ## sqlite3_evolutions_end ##
