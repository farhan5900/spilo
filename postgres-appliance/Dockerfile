FROM spilo:squashed

MAINTAINER Alexander Kukushkin <alexander.kukushkin@zalando.de>

ARG PGSQL_USER=postgres
ARG PGSQL_GROUP=postgres

RUN groupadd -g 99 nobody \
    && usermod -u 99 -g 99 -c 'Nobody for RHEL based system' nobody \
    && echo "nobody:x:65534:65534:Nobody for Debian based system:/nonexistent:/sbin/nologin" >> /etc/passwd \
    && usermod -a -G users nobody

EXPOSE 5432 8008 8080

ENV LC_ALL=en_US.utf-8 \
    PATH=$PATH:/usr/lib/postgresql/${PGVERSION}/bin \
    PGHOME=/mnt/mesos/sandbox

ENV WALE_ENV_DIR=$PGHOME/etc/wal-e.d/env \
    PGROOT=$PGHOME/pgroot \
    LOG_ENV_DIR=$PGHOME/etc/log.d/env

ENV PGDATA=$PGROOT/pgdata \
    PGLOG=$PGROOT/pg_log

WORKDIR $PGHOME

ADD pgq_ticker.ini /etc/
ADD envdir /usr/local/bin/

RUN if [ ${PGSQL_USER} = "nobody" ]; then \
        chown -R ${PGSQL_USER}:${PGSQL_GROUP} /var/run/postgresql /var/log/postgresql /etc/pgq_ticker.ini \
        && chmod -R g+w /var/run/postgresql /var/log/postgresql; \
    fi \
    && sed -i "s|/var/lib/postgresql.*|$PGHOME:/bin/bash|" /etc/passwd \
    && sed -i 's/set compatible/set nocompatible/' /etc/vim/vimrc.tiny \
    && for e in TERM=linux LC_ALL=C.UTF-8 LANG=C.UTF-8 EDITOR=vi; \
        do echo "export $e" >> /etc/bash.bashrc; \
    done \
    && echo "export PAGER='pspg -bX --no-mouse'" >> /etc/bash.bashrc

RUN env -i /usr/sbin/cron

ADD scripts bootstrap /scripts/

ADD scm-source.json launch.sh /

CMD ["/bin/sh", "/launch.sh"]
