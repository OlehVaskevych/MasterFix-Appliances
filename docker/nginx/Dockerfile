# Nginx Dockerfile for production
FROM nginx:1.25-alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media

# Expose ports
EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
