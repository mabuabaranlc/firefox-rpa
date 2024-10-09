xvfb-run -a uvicorn main:app --host 0.0.0.0 --port 4321 --reload

docker compose up --build --force-recreate