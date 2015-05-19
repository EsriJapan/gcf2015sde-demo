# -*- coding: utf-8 -*-
import arcpy
arcpy.CreateEnterpriseGeodatabase_management("SQL_Server", r'localhost', 'demo',
                                             "OPERATING_SYSTEM_AUTH", '', '', "SDE_SCHEMA", 
                                             'sde', 'P@ssw0rd', '', r'c:\data\gcf2015sde\demo1\authorization.ecp')


