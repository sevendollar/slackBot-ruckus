FROM mariadb:latest
LABEL maintainer="roycechen68@gmail.com"

ENV MARIADB_USER root
ENV MARIADB_PASS CvL898O4142
ENV LC_ALL en_US.UTF-8
ENV MARIADB_DATABASE ruckus
ENV MARIADB_USER royce
ENV MARIADB_PASSWORD Royce898O4142

COPY scripts /scripts
RUN chmod +x /scripts/start

EXPOSE 3306

VOLUME ["/var/lib/mysql"]

ENTRYPOINT ["/scripts/start"]
