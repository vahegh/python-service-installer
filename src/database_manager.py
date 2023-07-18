from .utils.consts import *

def run_db_commands(db_command, queries, variables):
    for q in queries:
        sub = q.format(**variables)
        command = db_command.__getitem__(sub)
        command()


def configure_database(db_type, db_user, db_pass, db_name):
    variables = vars()
    if db_type in ["mysql", "mariadb", "maria"]:
        run_db_commands(mysql_db_command, mysql_conf_commands, variables)

    elif db_type in ["postgresql", "postgres", "psql"]:
        run_db_commands(postgresql_db_command, postgresql_conf_commands, variables)
    
    else:
        print("Unsupported database.")

    print(f"""Configured database.
    Database: {db_name}
    User: {db_user}
    Password: {db_pass}""")


def remove_database(db_type, db_user, db_name):
    variables = vars()
    if db_type in ["mysql", "mariadb", "maria"]:
        run_db_commands(mysql_db_command, mysql_remove_commands, variables)

    elif db_type in ["postgresql", "postgres", "psql"]:
        run_db_commands(postgresql_db_command, postgresql_remove_commands, variables)
    
    else:
        print("Unsupported database.")

    print(f"""Removed database.
    Database: {db_name}
    User: {db_user}""")


if __name__ == "__main__":
    remove_database("psql", "test123", "test123")