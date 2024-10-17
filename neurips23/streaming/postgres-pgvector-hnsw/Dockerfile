FROM neurips23_postgres

# install pgvector
RUN git clone https://github.com/pgvector/pgvector.git --branch v0.7.4
WORKDIR /home/app/pgvector
RUN make clean && make -sj$(nproc) && make install
WORKDIR /home/app/

# start the database and create pgvector
USER postgres
RUN /usr/lib/postgresql/16/bin/pg_ctl -D /var/lib/postgresql/test_database -l /var/lib/postgresql/test_database_logfile -o "-F -p 5432" start && \
    /usr/lib/postgresql/16/bin/psql -p 5432 -U postgres -d postgres -c "ALTER SYSTEM SET shared_buffers TO '32GB'" && \
    /usr/lib/postgresql/16/bin/psql -p 5432 -U postgres -d postgres -c "ALTER SYSTEM SET work_mem  TO '2GB'" && \
    /usr/lib/postgresql/16/bin/pg_ctl -D /var/lib/postgresql/test_database -l /var/lib/postgresql/test_database_logfile -o "-F -p 5432" stop
RUN /usr/lib/postgresql/16/bin/pg_ctl -D /var/lib/postgresql/test_database -l /var/lib/postgresql/test_database_logfile -o "-F -p 5432" start && \
    /usr/lib/postgresql/16/bin/psql -p 5432 -U postgres -d postgres -c "CREATE EXTENSION vector";
USER root
