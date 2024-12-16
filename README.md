# IoT

We should prolly write some desc of our project up here, but i'm out of creativity.

## Raspberry Pi

### Running checkout script

```bash
cd raspberry
python -m checkout.checkout_main
```

### Running terminal script

```bash
cd raspberry
python -m terminal.terminal_main
```

### Running terminal tests

```bash
pytest raspberry/terminal/tests 
```

## Backend

### Setting environmental variables

Set your SQLite database path in the `.env` file. The default should be fine in most cases. For other database engines, some changes may be
required in `backend/database.py`.

```bash
cp backend/.env.example backend/.env
nano backend/.env
```

### Running the server

```bash
cd backend
uvicorn main:app --reload
```

### API documentation

Access Swagger documentation at http://127.0.0.1:8000/docs.

## Frontend

### WiP