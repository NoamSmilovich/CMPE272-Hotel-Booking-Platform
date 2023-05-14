public class DBConnectionFactory {
    public static DBConnection createConnection(String databaseType, String database) {
        switch (databaseType) {
            case "mongodb":
                return new MongoDBConnection(database);
//            case "arangodb":
//                return new ArangoDBConnection(database);
            case "mysql":
                try {
                    return new MySQLConnection(database);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            default:
                throw new IllegalArgumentException("Unsupported database type: " + databaseType);
        }
    }
}
