FROM ubuntu:latest

LABEL maintainer='ryan225360@gmail.com'
LABEL version="1.0"

RUN apt-get update && apt-get -y upgrade

RUN apt-get install -y software-properties-common

RUN apt-add-repository ppa:ondrej/php

RUN apt update

RUN apt install -y curl apache2 mysql-server unzip

RUN export DEBIAN_FRONTEND=noninteractive; apt -y install php7.2

RUN apt -y install php7.2-xml php7.2-mysqli php7.2-curl php7.2-mbstring

RUN cd /tmp; curl -sS https://getcomposer.org/installer -o composer-setup.php

RUN update-alternatives --set php /usr/bin/php7.2

RUN a2enmod php7.2

RUN cd /tmp; php composer-setup.php --install-dir=/usr/local/bin --filename=composer

RUN curl -LO https://github.com/phpmyadmin/phpmyadmin/archive/RELEASE_4_8_1.tar.gz

RUN tar -xf RELEASE_4_8_1.tar.gz

RUN cp -a /phpmyadmin-RELEASE_4_8_1/. /var/www/html/

RUN cd /var/www/

COPY ./files/config.inc.php /var/www/config.inc.php

RUN cd /var/www/html/; php /usr/local/bin/composer update; chown -R www-data:www-data *

RUN cd /var/www/html; service mysql restart && echo "SOURCE ./sql/create_tables.sql; CREATE USER 'pma'@'localhost' IDENTIFIED WITH mysql_native_password BY 'pmapass'; GRANT ALL PRIVILEGES ON phpmyadmin.* to 'pma'@'localhost' IDENTIFIED BY 'pmapass';"

RUN usermod -d /var/lib/mysql/ mysql

COPY ./files/wrapper.sh /tmp/start.sh

RUN chmod +x /tmp/start.sh

CMD cd /tmp; ./start.sh