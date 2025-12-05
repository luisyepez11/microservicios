FROM php:8.2-cli

# Install system dependencies and PHP extensions commonly needed by Laravel
RUN apt-get update \
     && apt-get install -y --no-install-recommends \
       git \
       unzip \
       libonig-dev \
       libzip-dev \
       libpng-dev \
       libicu-dev \
       libxml2-dev \
         libpq-dev \
     && docker-php-ext-configure intl \
     && docker-php-ext-install \
         pdo_mysql \
         pdo_pgsql \
         pgsql \
       mbstring \
       zip \
       intl \
       gd \
       xml \
     && rm -rf /var/lib/apt/lists/*

# Install Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/http

# Copy application source
COPY . /var/www/http

# Ensure required directories are writable
RUN mkdir -p storage bootstrap/cache \
    && chown -R www-data:www-data storage bootstrap/cache \
    && chmod -R 775 storage bootstrap/cache

# Install PHP dependencies
RUN composer install --no-interaction --prefer-dist --no-progress \
    && composer dump-autoload --optimize

# Laravel app setup (skip if not present)
RUN if [ -f artisan ]; then \
      php artisan key:generate --force || true; \
      php artisan config:clear || true; \
      php artisan cache:clear || true; \
    fi

# Expose the default dev server port
EXPOSE 8002