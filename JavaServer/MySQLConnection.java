import org.json.JSONException;
import org.json.JSONObject;

import java.sql.*;
import java.util.Iterator;

public class MySQLConnection implements DBConnection{
    final private String url =  "jdbc:mysql://localhost:3306/";
    final private String username = "root";
    final private String password = "12345678";
    private Connection conn;


    public MySQLConnection(String schema) throws SQLException, ClassNotFoundException {
        Class.forName("com.mysql.jdbc.Driver");
        this.conn = DriverManager.getConnection(this.url+schema, this.username, this.password);
    }

    public void executeQuery(String query){
        try {
            Statement stmt = conn.createStatement();
            stmt.executeUpdate(query);
        } catch (SQLException e){
            System.out.println(e.getMessage());
        }
    }

    public void create(String collection, JSONObject document) {
        String sql = "CREATE TABLE " + collection + " (";
        Iterator<String> keys = document.keys();
        while(keys.hasNext()) {
            String key = keys.next();
            String value = document.getString(key);
            sql += key + " " + value + ",";
        }
        sql = sql.substring(0, sql.length() - 1);
        sql += ")";
        executeQuery(sql);
    }

    // "collection" is equivalent to table here
    public JSONObject read(String collection, Object recvFilter) throws JSONException {
        String sql = "";
        if (recvFilter instanceof String) {
            sql = "SELECT * FROM " + collection;
            if (recvFilter != "")
                sql += " WHERE "+recvFilter;
        } else { // recvFilter is a JSONObject
            Iterator<String> keys = ((JSONObject)recvFilter).keys();
            while (keys.hasNext()){
                String key = keys.next();
                sql += key + "=" + ((JSONObject) recvFilter).getString(key);
            }
        }
        try {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(sql);
            return resultSetToJSONObject(rs);
        } catch (SQLException e){
            System.out.println(e.getMessage());
            return (new JSONObject()).put("result", "error");
        }
    }

    public JSONObject resultSetToJSONObject(ResultSet rs) throws SQLException {
        JSONObject jsonObject = new JSONObject();
        ResultSetMetaData rsmd = rs.getMetaData();
        int numColumns = rsmd.getColumnCount();
        JSONObject row;
        int i = 1;
        while (rs.next()) {
            row = new JSONObject();
            for (int j = 1; j <= numColumns; j++) {
                String columnName = rsmd.getColumnName(j);
                String columnValue = rs.getString(j);
                row.put(columnName, columnValue);
            }
            jsonObject.put(String.valueOf(i), row);
            i++;
        }
        return jsonObject;
    }

    public void update(String collection, JSONObject filterJson, JSONObject fieldsJson){

    }

    public void delete(String collection, String filterStr){

    }
    public void closeConnection() {
    }
}
