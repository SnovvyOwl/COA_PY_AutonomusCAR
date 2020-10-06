package com.example.wirelesscontroller.DataBase;

public class SettingDB {

    private SettingDB() {}

    public static final String TBL_SETTING = "SETTING_T";
    public static final String COL_IP = "IP";
    public static final String COL_PORT = "PORT";

    public static final String SQL_CREATE_TBL = "CREATE TABLE IF NOT EXISTS " + TBL_SETTING +  " " +
            "(" +
                COL_IP + " INTEGER NOT NULL" + "," +
                COL_PORT + "INTEGER NOT NULL" + "," +
            ")" ;

    public static final String SQL_DROP_TBL = "DROP TABLE IF EXISTS " + TBL_SETTING;

    public static final String SQL_SELECT = "SELECT * FROM "+ TBL_SETTING;

    public static final String SQL_INSERT = "INSERT OR REPLACE INTO "+ TBL_SETTING +" " +
            "(" + COL_IP + "," + COL_PORT + ") VALUES ";

    public static final String SQL_DELETE = "DELETE FROM " + TBL_SETTING;



}
