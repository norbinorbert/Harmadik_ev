FROM php:8.2-apache
RUN apt-get update && apt-get install -y git
RUN a2enmod rewrite
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
WORKDIR /var/www/html
COPY . ./
RUN composer install
CMD ["apache2-foreground"]