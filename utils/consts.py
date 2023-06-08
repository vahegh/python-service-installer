service_base_dir = "/opt"
systemd_base_dir = "/etc/systemd/system"

create_user_mysql = f"CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_pass}';"
create_db_mysql = f"CREATE DATABASE {db_name};"
grant_privileges_mysql =f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost';"
flush_privileges_mysql = "FLUSH PRIVILEGES;"


create_user = f"CREATE USER {db_user} WITH PASSWORD '{db_pass}';"
create_db = f"CREATE DATABASE {db_name} OWNER {db_user};"
grant_privileges = f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};"
flush_privileges = f"GRANT USAGE, CREATE ON SCHEMA PUBLIC TO {db_user}"


delete_db_mysql = f"DROP DATABASE IF EXISTS {db_name};"
revoke_privileges_mysql = None
delete_user_mysql = f"DROP USER IF EXISTS '{db_user}'@'localhost';"

delete_db = f"DROP DATABASE IF EXISTS {db_name};"
revoke_privileges = f"REVOKE USAGE, CREATE ON SCHEMA PUBLIC FROM {db_user}"
delete_user = f"DROP USER IF EXISTS {db_user};"