## To start the application

### Prerequisites

- Docker
- OPEN API KEY

**Note** - Please update .env with your keys.

### Start the application using the Python script

## To start the application, you can use the following command:

```bash
python master.py run
```

*OR*

```bash
docker compose up --build
```

## To test the api's
```bash
python master.py test
```

*OR

## Access swagger 

```bash
http://localhost:8000/docs#/
```

This command will bring up the Docker Compose services in detached mode (-d), starting the application.

## Other commands
- **Make migrations**: If you need to create new database migrations, you can use the following command:
    ```bash
    python master.py makemigrations -m "Migration message"
    ```

- **Apply migrations**: To apply the database migrations:
    ```bash
    python master.py migrate
    ```
    
- **Open a shell inside the container**: If you need to access the container’s shell:
    ```bash
    python master.py shell
    ```

- **Reset the application (drop all volumes)**: To reset the application by removing all volumes (including data), use the following command:
    ```bash
    python master.py reset
    ```

