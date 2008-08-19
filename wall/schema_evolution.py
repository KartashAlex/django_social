
# all of your evolution scripts, mapping the from_version and to_version to a list if sql commands
sqlite3_evolutions = [
    [('fv1:1518106188','fv1:-1406536048'), # generated 2008-08-11 09:03:21.003008
        "CREATE TABLE \"wall_message\" (\n    \"id\" integer NOT NULL PRIMARY KEY,\n    \"from_user_id\" integer NOT NULL REFERENCES \"net_user\" (\"user_ptr_id\"),\n    \"subject\" varchar(255) NOT NULL,\n    \"body\" text NOT NULL,\n    \"private\" bool NOT NULL,\n    \"sent\" datetime NOT NULL,\n    \"parent_id\" integer NULL,\n    \"content_type_id\" integer NOT NULL REFERENCES \"django_content_type\" (\"id\"),\n    \"object_id\" integer NOT NULL\n)\n;",
    ],
] # don't delete this comment! ## sqlite3_evolutions_end ##
