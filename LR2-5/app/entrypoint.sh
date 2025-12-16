#!/bin/bash

while ! nc -z $DB_HOST $DB_PORT; do
