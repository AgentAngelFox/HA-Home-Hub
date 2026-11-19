FROM nginx:alpine
COPY hub.html /usr/share/nginx/html/index.html
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD wget -q -O /dev/null http://127.0.0.1/ || exit 1
