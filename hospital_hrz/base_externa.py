#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2

hostname = 'localhost'
username = 'postgres'
password = '123456'
database = 'hospitalHRZ'

'''
hostname = '192.168.5.3'
username = 'postgres'
password = ''
database = 'hospitalHRZ'
'''
def connect():
	return psycopg2.connect( host=hostname, user=username, password=password, dbname=database)