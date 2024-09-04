import subprocess
import sys

def run_alembic_migrations():
    print('Running Alembic migrations...')
    result = subprocess.run(['alembic', 'upgrade', 'head'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f'Error running migrations: {result.stderr}', file=sys.stderr)
        sys.exit(result.returncode)
    print(result.stdout)

def start_uvicorn():
    print("Starting FastAPI application with Uvicorn...")
    result = subprocess.run(['uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8000'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f'Error starting Uvicorn: {result.stderr}', file=sys.stderr)
        sys.exit(result.returncode)
    print(result.stdout)

if __name__ == "__main__":
    run_alembic_migrations()
    start_uvicorn()
