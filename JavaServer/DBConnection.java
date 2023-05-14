import org.json.JSONException;
import org.json.JSONObject;

public interface DBConnection {
    public void create(String collection, JSONObject document);
    public JSONObject read(String collection, Object recvFilter) throws JSONException;
    public void update(String collection, JSONObject filterJson, JSONObject fieldsJson);
    public void delete(String collection, String filterStr);
    public void closeConnection();
}
