import argparse
import sys
from alembic.config import Config
from alembic import command
from subprocess import call

def make_migrations(message):
    """Create new database migration"""
    alembic_cfg = Config("alembic.ini")
    command.revision(
        alembic_cfg, 
        autogenerate=True,
        message=message
    )

def migrate():
    """Apply database migrations"""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

def runserver():
    """Start the development server"""
    call(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage application")
    subparsers = parser.add_subparsers(dest='command')

    # Makemigrations command
    makemigrations_parser = subparsers.add_parser('makemigrations')
    makemigrations_parser.add_argument('-m', '--message', required=True)

    # Migrate command
    subparsers.add_parser('migrate')

    # Runserver command
    subparsers.add_parser('runserver')

    args = parser.parse_args()

    if args.command == 'makemigrations':
        make_migrations(args.message)
    elif args.command == 'migrate':
        migrate()
    elif args.command == 'runserver':
        runserver()
    else:
        parser.print_help()
        sys.exit(1)