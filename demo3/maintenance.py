# coding: utf-8

import arcpy
import sys

def main():

    admin_connection = r"c:\data\gcf2015sde\demo3\gcf2015_demo3_admin.sde"
    data_admin_connection = r"c:\data\gcf2015sde\demo3\gcf2015_demo3_da.sde"

    #新規接続の拒否
    print(u"新規接続を拒否します。")
    arcpy.AcceptConnections(admin_connection, False)

    #すべてのユーザーを切断します
    print(u"既存の接続を切断します。")
    arcpy.DisconnectUser(admin_connection, "ALL")

    #バージョン情報の取得
    print(u"リコンサイル対象のバージョン名を取得します。")
    tmp_list = arcpy.da.ListVersions(admin_connection)
    version_list = [v.name for v in tmp_list if v.parentVersionName == 'sde.DEFAULT']
    print(version_list)

    #リコンサイル / ポスト
    print(u"リコンサイルとポスト処理を行います。")
    arcpy.ReconcileVersions_management(admin_connection, "ALL_VERSIONS", "sde.DEFAULT",
                                           version_list,"LOCK_ACQUIRED", "NO_ABORT",
                                           "BY_OBJECT", "FAVOR_TARGET_VERSION","POST",
                                           "KEEP_VERSION", sys.path[0] + "/reclog.txt")

    #データベースの圧縮
    print(u"データベースを圧縮します。")
    arcpy.Compress_management(admin_connection)


    #システムテーブルのインデックスの再構築
    print(u"システムテーブルのインデックスを再構築します")
    arcpy.RebuildIndexes_management(admin_connection, "SYSTEM")

    #システムテーブルの統計情報の更新
    print(u"システムテーブルの統計情報を更新します。")
    arcpy.AnalyzeDatasets_management(admin_connection, "SYSTEM")

    #新規接続の許可
    print(u"再度新規接続を許可します。")
    arcpy.AcceptConnections(admin_connection, True)

    #データリストの取得
    print(u"フィーチャクラスのリストを取得します")
    arcpy.env.workspace = data_admin_connection
    user_name = arcpy.Describe(arcpy.env.workspace).connectionProperties.user
    data_list = arcpy.ListFeatureClasses(u'*.' + user_name + u'.*')
    
    #フィーチャクラスのインデックスの再構築
    print(u"フィーチャクラスのインデックスを再構築します")
    arcpy.RebuildIndexes_management(data_admin_connection, "NO_SYSTEM", data_list, "ALL")
    
    #フィーチャクラスの統計情報の更新
    print(u"フィーチャクラスの統計情報を更新します。")
    arcpy.AnalyzeDatasets_management(data_admin_connection, "NO_SYSTEM", data_list)
    

if __name__ == "__main__":
    main()
