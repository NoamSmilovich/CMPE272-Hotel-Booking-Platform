import com.mongodb.ConnectionString;
import com.mongodb.MongoClientSettings;
import com.mongodb.MongoException;
import com.mongodb.client.*;
import org.bson.Document;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Iterator;

public class MongoDBConnection implements DBConnection {
    private MongoClient mongoClient;
    private MongoDatabase database;

    public MongoDBConnection(String database) throws MongoException {
        String dbName = database;
        String connectionString = "mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority";
        try {
            this.mongoClient = MongoClients.create(
                    MongoClientSettings.builder()
                            .applyConnectionString(new ConnectionString(connectionString))
                            .build());
            this.database = mongoClient.getDatabase(dbName);
        } catch (MongoException e) {
            throw new MongoException("Failed to connect to MongoDB server: " + e.getMessage());
        }
    }

    public void closeConnection() {
        this.mongoClient.close();
    }

    public void create(String collection, JSONObject document) {
            Iterator<String> keys = document.keys();
            while (keys.hasNext()) {
                String key = keys.next();
                Object value = document.get(key);
                if (value instanceof JSONObject) {
                    database.getCollection(collection).insertOne(Document.parse(((JSONObject) value).toString()));
                } else {
                    database.getCollection(collection).insertOne(Document.parse(document.toString()));
                }
            }
    }

    public JSONObject read(String collection, Object recvFilter) throws JSONException {
    	System.out.println("attempting mongo read...");
        MongoCollection<Document> monCollection = database.getCollection(collection);
        FindIterable<Document> result;
        String filterStr;
        if(recvFilter instanceof String)
            filterStr = (String) recvFilter;
        filterStr = (String) recvFilter;
        if(filterStr!="") {
            Document filter = Document.parse(filterStr);
            result = monCollection.find(filter);
        } else {
            result = monCollection.find();
        }
        if (result == null) {
            return null;
        }
        FindIterable<Document> iterDoc = result;
        Iterator<Document> it = iterDoc.iterator();
        ArrayList<JSONObject> doc_list = new ArrayList<>();
        while (it.hasNext()) {
            doc_list.add(new JSONObject((Document) it.next()));
        }
        System.out.println("returning mongo read...");
        return ListToJSONObject(doc_list);
    }

    private JSONObject ListToJSONObject(ArrayList<JSONObject> doc_list){
        JSONObject json = new JSONObject();
        for(int i=0;i<doc_list.size();i++){
            json.put(String.format("%d", i), doc_list.get(i));
        }
        return json;
    }

    public void update(String collection, JSONObject filterJson, JSONObject fieldsJson) {
        MongoCollection<Document> monCollection = database.getCollection(collection);
        Document filter = Document.parse(filterJson.toString());
        Document fields = Document.parse(fieldsJson.toString());
        monCollection.updateOne(filter, new Document("$set", fields));
    }

    public void delete(String collection, String filterStr){
        database.getCollection(collection).deleteOne(Document.parse(filterStr));
    }
}