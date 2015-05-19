# coding: utf-8

"""ユーザーを追加し、ロール、バージョンを作成するツール"""

import arcpy
import sys


def main():

    data_adm_user = "shinpei" #データ所有者 ユーザー
    viewers = ["taro", "fuyuna", "iharu", "jotaro", "amuro", "hayato"] #閲覧専用ユーザー
    editors = ["jiro", "saburo", "hiromichi"] #編集可能ユーザー

    dbms = "SQL_SERVER"
    db_instance = "localhost"
    database = "demo"

    data_list = [ur"c:\data\gcf2015sde\demo2\shp\東京.shp",
                 ur"c:\data\gcf2015sde\demo2\shp\神奈川.shp",
                 ur"c:\data\gcf2015sde\demo2\shp\埼玉.shp"]


    #管理者での接続ファイルの作成
    print(u"データベース管理者でのデータベースへの接続を作成しています。")
    admin_conn = arcpy.CreateDatabaseConnection_management(r'c:\data\gcf2015sde\demo2', 
                                                           r"gcf2015_demo2_dbadmin.sde", dbms, db_instance, 
                                                           "OPERATING_SYSTEM_AUTH", "", "", "", database)


    #ロールの追加
    print(u"閲覧用ロールと編集用ロールを作成しています。")
    arcpy.CreateRole_management(admin_conn, 'viewers')
    arcpy.CreateRole_management(admin_conn, 'editors')

    #ユーザーの追加
    print(u"データ所有者ユーザーの追加しています。")
    arcpy.CreateDatabaseUser_management(admin_conn, 'DATABASE_USER', data_adm_user, "P@ssw0rd")

    print(u"各ロールに属するユーザーの追加しています。")
    for user in viewers:
        arcpy.CreateDatabaseUser_management(admin_conn, 'DATABASE_USER', user, "P@ssw0rd", 'viewers')

    for user in editors:
        arcpy.CreateDatabaseUser_management(admin_conn, 'DATABASE_USER', user, "P@ssw0rd", 'editors')

    #データ所有者ユーザーでの接続ファイルを作成
    print(u"データ所有者での接続ファイルを作成しています。")
    owner_conn = arcpy.CreateDatabaseConnection_management(r'c:\data\gcf2015sde\demo2', 
                                                           r"gcf2015_demo2_da.sde", dbms, db_instance, 
                                                           "DATABASE_AUTH", data_adm_user, 
                                                           "P@ssw0rd", "SAVE_USERNAME", database)

    #データの投入
    print(u"データをコピーしています。")
    arcpy.FeatureClassToGeodatabase_conversion(data_list, owner_conn)


    #ワークスペースをデータ所有者の接続ファイルに設定
    print(u"ワークスペースをデータ所有者での接続ファイルに設定します。")
    arcpy.env.workspace = owner_conn[0]

    #データリストの取得
    print(u"データリストを取得しています。")
    data_list = arcpy.ListFeatureClasses("*.{0}.*".format(data_adm_user))
    print(data_list)

    #バージョン対応登録
    print(u"バージョン対応登録を行います。")
    for dataset in data_list:
        arcpy.RegisterAsVersioned_management(dataset)

    #権限の設定
    print(u"各ロールに権限を付与しています。")
    arcpy.ChangePrivileges_management(data_list, 'viewers', 'GRANT')
    arcpy.ChangePrivileges_management(data_list, 'editors', 'GRANT', 'GRANT')

    #バージョンの作成
    print(u"編集者ユーザーバージョンを作成します。")
    for user in editors:
        user_conn = arcpy.CreateDatabaseConnection_management(r'c:\data\gcf2015sde\demo2', 
                                                              r"gcf2015_demo2_{0}.sde".format(user), 
                                                            dbms, db_instance, "DATABASE_AUTH", user, 
                                                            "P@ssw0rd", "SAVE_USERNAME", database)
        arcpy.CreateVersion_management(user_conn, 'sde.DEFAULT', user + '_version', 'PRIVATE')



if __name__ == '__main__':
    main()
