param()
Write-Host "Applying migrations..."
pushd api
alembic -c alembic.ini upgrade head
popd
