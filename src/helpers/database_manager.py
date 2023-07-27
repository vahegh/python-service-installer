from ..utils.consts import *
from ..utils.exceptions import DbTypeError

def run_db_commands(db_command, queries, variables):
    for q in queries:
        sub = q.format(**variables)
        command = db_command.__getitem__(sub)
        command()


def configure_db(db_type, db_user, db_pass, db_name):
    variables = vars()
    if db_type in ["mysql", "mariadb", "maria"]:
        run_db_commands(MYSQL_DB_COMMAND, MYSQL_CONF_COMMANDS, variables)

    elif db_type in ["postgresql", "postgres", "psql"]:
        run_db_commands(POSTGRESQL_DB_COMMAND, POSTGRESQL_CONF_COMMANDS, variables)
    
    else:
        raise DbTypeError("Unsupported database.")

    print(f"""Configured database.
    Database: {db_name}
    User: {db_user}
    Password: {db_pass}""")


def remove_db(db_type, db_user, db_name):
    variables = vars()
    if db_type in ["mysql", "mariadb", "maria"]:
        run_db_commands(MYSQL_DB_COMMAND, MYSQL_REMOVE_COMMANDS, variables)

    elif db_type in ["postgresql", "postgres", "psql"]:
        run_db_commands(POSTGRESQL_DB_COMMAND, POSTGRESQL_REMOVE_COMMANDS, variables)

    print(f"""Removed database.
    Database: {db_name}
    User: {db_user}""")


if __name__ == "__main__":
    remove_db("psql", "test123", "test123")