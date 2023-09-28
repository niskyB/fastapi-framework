## Environment

Python version: 3.10

You can set the application environment in `.env` file

### Environment variables

| Name                 | Description                      |
| -------------------- | -------------------------------- |
| BACKEND_CORS_ORIGINS | CORS allow origin                |
| DB_SERVER            | DB host server                   |
| DB_USER              | DB user                          |
| DB_PASSWORD          | DB password                      |
| DB_PORT              | DB port                          |
| DB_DB                | DB DB name                       |
| TENANT_ID            | Azure AD B2C tenant id           |
| CLIENT_ID            | Azure AD B2C client id           |
| CLIENT_SECRET        | Azure AD B2C client secret       |
| FSSK_TENANT_ID       | Federated Azure AD tenant id     |
| FSSK_CLIENT_ID       | Federated Azure AD client id     |
| FSSK_CLIENT_SECRET   | Federated Azure AD client secret |

## Running the application

### Window

Run `run.cmd` file to start the application

### Linux

Run `run.sh` file to start the application

## Documentation

Open API Documentations are provided by [Redoc](http://localhost:8000/redoc) and [Swagger UI](http://localhost:8000/docs)

# Code formatting

Black is used as the formatter for the repository. It can be invoked from inside the virtual environment.
To check for formatting:

```
black --check .
```

To format all code files:

```
black .
```

# Autogenerate a database revision

Since the backend container has been installed with alembic, you can use the following command:

`alembic revision --autogenerate -m "$message"`

This will autogenerate a new revision for the database migration, and you can get the migration file with the message as the name from the Docker container. You can then put it in `./alembic/versions/` to update the database migration.
