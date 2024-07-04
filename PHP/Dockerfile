# Use the official PHP image
FROM php:8.2-cli

# Set the working directory inside the container
WORKDIR /PHP

# Copy the current directory contents into the container at /app
COPY . .

# Specify the command to run when the container starts
CMD ["php", "-S", "0.0.0.0:8080"]
