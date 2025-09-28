param()
Write-Host "Starting RainRef dev stack..."
docker compose -f infra/docker-compose.yml up --build
