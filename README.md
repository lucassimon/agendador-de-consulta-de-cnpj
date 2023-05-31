$ psql -h localhost -U postgres
postgres=# create user agendadorcnpj with encrypted password 'teste123';
postgres=# create database agendadorcnpj;
postgres=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO agendadorcnpj;
