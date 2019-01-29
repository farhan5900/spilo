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
    PGROOT=$PGHOME/pgdata/pgroot \
    LOG_ENV_DIR=$PGHOME/etc/log.d/env

ENV PGDATA=$PGROOT/data \
    PGLOG=$PGROOT/pg_log

WORKDIR $PGHOME

ADD motd /etc/
ADD supervisor /etc/supervisor
ADD pgq_ticker.ini $PGHOME/
ADD envdir /usr/local/bin/

RUN mkdir -p /var/log/supervisor \
        && ln -s supervisor/supervisord.conf /etc/supervisord.conf \
        && sed -i "s|/var/lib/postgresql.*|$PGHOME:/bin/bash|" /etc/passwd \
        && mkdir -p $PGDATA $PGLOG
        && chown -R ${PGSQL_USER}:${PGSQL_GROUP} $PGHOME \
        && chmod -R g+w $PGHOME \
        && sed -i 's/set compatible/set nocompatible/' /etc/vim/vimrc.tiny \
        && for e in TERM=linux LC_ALL=C.UTF-8 LANG=C.UTF-8 EDITOR=vi; \
            do echo "export $e" >> /etc/bash.bashrc; \
        done \
        && echo "export PAGER='pspg -bX --no-mouse'" >> /etc/bash.bashrc \
        && echo "source /etc/motd" >> /root/.bashrc

ADD scripts bootstrap /scripts/

ADD scm-source.json launch.sh /

CMD ["/bin/sh", "/launch.sh"]
