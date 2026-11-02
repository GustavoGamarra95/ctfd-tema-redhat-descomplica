FROM ctfd/ctfd:3.8.9

USER root
# Hugging Face Spaces roda o contêiner com UID 1000
RUN usermod -u 1000 ctfd \
    && chown -R 1000 /opt/CTFd /var/log/CTFd /var/uploads
COPY --chmod=755 hf-entrypoint.sh /opt/hf-entrypoint.sh

USER 1000
ENV REVERSE_PROXY=true \
    WORKERS=1 \
    SKIP_DB_PING=true
EXPOSE 8000
ENTRYPOINT ["/opt/hf-entrypoint.sh"]
