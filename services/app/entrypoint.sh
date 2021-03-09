#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
# http://stackoverflow.com/questions/19622198/what-does-set-e-mean-in-a-bash-script
set -e

# Check if the required PostgreSQL environment variables are set

# Used by docker-entrypoint.sh to start the dev server
# If not configured you'll receive this: CommandError: "0.0.0.0:" is not a valid port number or address:port pair.
[ -z "$PORT" ] && echo "ERROR: Need to set PORT. E.g.: 8000" && exit 1;


# Used by uwsgi.ini file to start the wsgi Django application
[ -z "$WSGI_MODULE" ] && echo "ERROR: Need to set WSGI_MODULE. E.g.: config.wsgi:application" && exit 1;


# Define help message
show_help() {
    echo """
Usage: docker run <imagename> COMMAND

Commands

dev      : Start a normal Django development server
bash     : Start a bash shell
manage   : Start manage.py
setup_db : Setup the initial database. Configure \$POSTGRES_DB_NAME in docker-compose.yml
fetch_data : Ingest data from OpenFisca API (url specified in .env file)
lint     : Run pylint
python   : Run a python command
shell    : Start a Django Python shell
uwsgi    : Run uwsgi server
help     : Show this message
"""
}

write_uwsgi() {
    echo "Generating uwsgi config file..."
    snippet="import os;
import sys;
import jinja2;
sys.stdout.write(jinja2.Template(sys.stdin.read()).render(env=os.environ))"

    cat /deployment/uwsgi.ini | python -c "${snippet}" > /uwsgi.ini
}

# Run
case "$1" in
    dev)
        echo "Running Development Server on 0.0.0.0:${PORT}"
        python manage.py runserver 0.0.0.0:${PORT}
    ;;
    bash)
        /bin/bash "${@:2}"
    ;;
    manage)
        python manage.py "${@:2}"
    ;;
    setup_db)
        # If the `POSTGRES_DB_NAME` environment variable is set in `docker-compose.yml`,
        # then create the PostgreSQL database
        if [[ -v POSTGRES_DB_NAME ]]; then
            psql -h $POSTGRES_PORT_5432_TCP_ADDR -U $POSTGRES_USER -c "DROP DATABASE IF EXISTS $POSTGRES_DB_NAME"
            psql -h $POSTGRES_PORT_5432_TCP_ADDR -U $POSTGRES_USER -c "CREATE DATABASE $POSTGRES_DB_NAME"
            python manage.py migrate
        # Else; create a sqlite3 database at location `./app/db.sqlite3`
        else
            rm -f db.sqlite3
            python manage.py migrate
        fi  
    ;;
    fetch_data)
        python manage.py fetch_all
    ;;
    lint)
        pylint "${@:2}"
    ;;
    python)
        python "${@:2}"
    ;;
    shell)
        python manage.py shell_plus
    ;;
    uwsgi)
        echo "Running App (uWSGI)..."
        write_uwsgi
        uwsgi --ini /uwsgi.ini
    ;;
    *)
        show_help
    ;;
esac
