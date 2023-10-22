FROM mysql:8.0

EXPOSE 3306

COPY ./db/database_app.sql /docker-entrypoint-initdb.d/
# CMD ["mysqld"]
