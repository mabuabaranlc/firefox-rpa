Script para ejecutar en local:
```
xvfb-run -a uvicorn main:app --host 0.0.0.0 --port 4321 --reload
```

Script para ejecutar en docker:
```
docker compose up --build --force-recreate
```
