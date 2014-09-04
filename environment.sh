export DATABASE_URL='postgresql://localhost/introductions'
export SETTINGS='config.DevelopmentConfig'

set +o errexit
createuser -s introductions
createdb -U introductions -O introductions introductions -T template0
