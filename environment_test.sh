export SETTINGS='config.TestConfig'
export DATABASE_URL='postgresql://localhost/introductions_test'

createuser -s introductions_test
createdb -U introductions_test -O introductions_test introductions_test -T template0

