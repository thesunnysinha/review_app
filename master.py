import argparse
import sys
from subprocess import call, check_output


def get_container_name():
    """Get the name of the running container"""
    container_name = (
        check_output(["docker", "compose", "ps", "-q", "backend"]).strip().decode()
    )
    return container_name


def is_container_running(container_name):
    """Check if the container is running"""
    try:
        status = (
            check_output(
                ["docker", "inspect", "--format", "{{.State.Running}}", container_name]
            )
            .strip()
            .decode()
        )
        return status == "true"
    except Exception as e:
        print(f"Error checking container status: {e}")
        return False


def make_migrations(message):
    """Create new database migration inside the running container"""
    container_name = get_container_name()
    if not is_container_running(container_name):
        print(f"Container {container_name} is not running. Aborting.")
        sys.exit(1)
    call(
        [
            "docker",
            "exec",
            "-it",
            container_name,
            "alembic",
            "revision",
            "--autogenerate",
            "-m",
            message,
        ]
    )


def migrate():
    """Apply database migrations inside the running container"""
    container_name = get_container_name()
    if not is_container_running(container_name):
        print(f"Container {container_name} is not running. Aborting.")
        sys.exit(1)
    call(["docker", "exec", "-it", container_name, "alembic", "upgrade", "head"])


def open_shell():
    """Open a shell inside the running container"""
    container_name = get_container_name()
    if not is_container_running(container_name):
        print(f"Container {container_name} is not running. Aborting.")
        sys.exit(1)
    call(["docker", "exec", "-it", container_name, "bash"])


def run_test():
    """Trigger the test.py script inside the container"""
    container_name = get_container_name()
    if not is_container_running(container_name):
        print(f"Container {container_name} is not running. Aborting.")
        sys.exit(1)
    call([
        "docker", "exec", "-it", container_name,
        "python", "test.py"
    ])

def run():
    """Run the application by bringing up the Docker Compose services"""
    print("Starting the application...")
    call(["docker", "compose", "up", "-d"])
    print("Application started successfully.")


def reset():
    """Reset by dropping all volumes"""
    print("Dropping all Docker volumes...")
    call(["docker", "compose", "down", "--volumes", "--remove-orphans"])
    print("All volumes dropped successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage application")
    subparsers = parser.add_subparsers(dest="command")

    # Makemigrations command
    makemigrations_parser = subparsers.add_parser("makemigrations")
    makemigrations_parser.add_argument("-m", "--message", required=True)

    # Migrate command
    subparsers.add_parser("migrate")

    # Shell command
    subparsers.add_parser("shell")

    # Run application command
    subparsers.add_parser("run")

    # Reset command (new command to drop all volumes)
    subparsers.add_parser("reset")

    # Test command to trigger test.py inside the container
    subparsers.add_parser('test')

    args = parser.parse_args()

    if args.command == "makemigrations":
        make_migrations(args.message)
    elif args.command == "migrate":
        migrate()
    elif args.command == "shell":
        open_shell()
    elif args.command == "run":
        run()
    elif args.command == "reset":
        reset()
    elif args.command == 'test':
        run_test()
    else:
        parser.print_help()
        sys.exit(1)
