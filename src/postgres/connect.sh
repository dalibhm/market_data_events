psql postgres

GRANT ALL PRIVILEGES ON DATABASE contracts TO ibapp;

psql -d contracts -U ibapp

# hba_file
/usr/local/var/postgresql@12/pg_hba.conf