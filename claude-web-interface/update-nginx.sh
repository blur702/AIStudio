#!/bin/bash

# Script to update nginx configuration for Claude Web Interface

echo "Updating nginx configuration for Claude Web Interface..."

# Backup existing config
sudo cp /etc/nginx/sites-available/kevinalthaus.conf /etc/nginx/sites-available/kevinalthaus.conf.backup.$(date +%Y%m%d_%H%M%S)

# Update the config with sed
sudo sed -i '216,235c\    # Claude Web Interface API\n    location /code/api/ {\n        proxy_pass http://localhost:5001/api/;\n        proxy_http_version 1.1;\n        proxy_set_header Host $host;\n        proxy_set_header X-Real-IP $remote_addr;\n        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n        proxy_set_header X-Forwarded-Proto $scheme;\n        proxy_set_header Cookie $http_cookie;\n        proxy_cookie_path / /;\n        \n        # Long timeouts for Claude operations\n        proxy_connect_timeout 600s;\n        proxy_send_timeout 600s;\n        proxy_read_timeout 600s;\n        \n        # Disable buffering for streaming\n        proxy_buffering off;\n    }\n    \n    # React Frontend for Code\n    location /code {\n        alias /opt/code/claude-web-interface/frontend/dist;\n        try_files $uri $uri/ @code_fallback;\n        \n        # Security headers\n        add_header X-Frame-Options "SAMEORIGIN" always;\n        add_header X-Content-Type-Options "nosniff" always;\n        add_header X-XSS-Protection "1; mode=block" always;\n        \n        # Cache static assets\n        location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {\n            expires 1y;\n            add_header Cache-Control "public, immutable";\n        }\n    }\n    \n    # Fallback for React Router\n    location @code_fallback {\n        rewrite ^/code(.*) /code/index.html last;\n    }' /etc/nginx/sites-available/kevinalthaus.conf

# Test nginx config
echo "Testing nginx configuration..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "Nginx configuration is valid. Reloading nginx..."
    sudo systemctl reload nginx
    echo "Nginx reloaded successfully!"
else
    echo "Nginx configuration test failed. Please check the configuration."
    exit 1
fi