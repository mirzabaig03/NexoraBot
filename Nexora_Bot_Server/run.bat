@echo off
REM Windows Batch file to replace Makefile functionality

if "%1"=="server" goto server
if "%1"=="worker" goto worker
if "%1"=="redis" goto redis
if "%1"=="all" goto all
goto help

:server
echo Starting Server...
poetry run uvicorn src.server:app --reload --host 0.0.0.0 --port 8000
goto end

:worker
echo Starting Worker...
poetry run celery -A src.services.celery:celery_app worker --loglevel=info --pool=threads
goto end

:redis
echo Starting Redis...
cd redis
docker-compose -f docker-compose.yaml up
cd ..
goto end

:all
echo Starting ALL services in new windows...
start "Redis" cmd /k "run.bat redis"
timeout /t 5
start "Worker" cmd /k "run.bat worker"
start "Server" cmd /k "run.bat server"
goto end

:help
echo Usage: run.bat [command]
echo.
echo Commands:
echo   server   - Run the FastAPI server
echo   worker   - Run the Celery worker
echo   redis    - Run Redis via docker-compose
echo   all      - Run ALL services in separate windows
echo.
echo Example: .\run.bat server
goto end

:end
