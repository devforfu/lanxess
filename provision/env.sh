#!/usr/bin/env bash

echo "Saving environment variables"

echo "export APP_DB_USER=${APP_DB_USER}" >> /home/vagrant/.bashrc
echo "export APP_DB_PASS=${APP_DB_PASS}" >> /home/vagrant/.bashrc
echo "export APP_DB_NAME=${APP_DB_NAME}" >> /home/vagrant/.bashrc
echo "export APP_DB_URL_DEV=${APP_DB_URL_DEV}" >> /home/vagrant/.bashrc
echo "export APP_DB_URL_TEST=${APP_DB_URL_TEST}" >> /home/vagrant/.bashrc
echo "export APP_DB_URL_PROD=${APP_DB_URL_PROD}" >> /home/vagrant/.bashrc
echo "export APP_SECRET=${APP_SECRET}" >> /home/vagrant/.bashrc
