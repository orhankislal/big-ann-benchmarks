FROM neurips23_postgres

# install pgvector
RUN git clone https://github.com/pgvector/pgvector.git --branch v0.7.0
WORKDIR /home/app/pgvector
RUN make clean && make -sj$(nproc) && make install
WORKDIR /home/app/

# XXX: should use docker secrets for or such but install.py doesn't support them yet
ARG MSRUSTUP_PAT

# install msrustup
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt install -y ca-certificates curl jq lldb unzip
COPY ./neurips23/streaming/postgres-pg-diskann/install_msrustup.sh install_msrustup.sh
RUN chmod +x install_msrustup.sh
RUN export MSRUSTUP_PAT=$MSRUSTUP_PAT && ./install_msrustup.sh

# install cargo via msrustup and ms-stable toolchain
RUN echo | ./msrustup

# install cargo-pgrx
RUN . /root/.cargo/env && cargo +ms-stable install --locked cargo-pgrx@0.11.4

# initialize pgrx for pg16
RUN . /root/.cargo/env && cargo +ms-stable pgrx init --pg16=/usr/bin/pg_config

ARG ADO_USERNAME

# XXX: should use docker secrets or such but install.py doesn't support them yet
ARG PG_DISKANN_REPO_PASSWORD
ARG DISKANN_REPO_PASSWORD

# set git credentials for the repos that we're interested in
RUN git config --global credential.helper store
RUN echo https://$ADO_USERNAME:$PG_DISKANN_REPO_PASSWORD@dev.azure.com > ~/.git-credentials
RUN echo https://$ADO_USERNAME:$DISKANN_REPO_PASSWORD@msdata.visualstudio.com >> ~/.git-credentials
RUN chmod 600 ~/.git-credentials

#download, build and install pgvectorscale
RUN cd /tmp
RUN git clone https://github.com/timescale/pgvectorscale
WORKDIR /home/app/pgvectorscale
RUN git fetch && git checkout 0.4.0
RUN cd pgvectorscale
RUN cargo pgrx install --release
WORKDIR /home/app/

# start the database and create pgvector and pg_diskann extensions
USER postgres
RUN /usr/lib/postgresql/16/bin/pg_ctl -D /var/lib/postgresql/test_database -l /var/lib/postgresql/test_database_logfile -o "-F -p 5432" start && \
    /usr/lib/postgresql/16/bin/psql -p 5432 -U postgres -d postgres -c "CREATE EXTENSION vector" && \
    /usr/lib/postgresql/16/bin/psql -p 5432 -U postgres -d postgres -c "CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE;";
USER root
