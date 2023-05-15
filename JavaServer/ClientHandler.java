import org.json.JSONException;
import org.json.JSONObject;

import java.io.DataInputStream;
import java.io.IOException;
import java.net.Socket;
import java.nio.ByteBuffer;

class ClientHandler implements Runnable {
    private final Socket clientSocket;
    private DBConnection DBHandle;

    public ClientHandler(Socket socket)
    {
        this.clientSocket = socket;
    }

    public void run()
    {
        try {
            while (!this.clientSocket.isClosed()) {
                DataInputStream dis = new DataInputStream(clientSocket.getInputStream());
                byte[] lengthPrefix = new byte[4];
                dis.readFully(lengthPrefix);
                // convert the length prefix to an integer
                int length = ByteBuffer.wrap(lengthPrefix).getInt();
                // read the message from the client
                byte[] messageBytes = new byte[length];
                dis.readFully(messageBytes);
                String message = new String(messageBytes);

                System.out.println(message);
                JSONObject messageJson = new JSONObject(convertStandardJSONString(message));
                parse_and_query(messageJson);
            }
            if (this.DBHandle!=null)
                DBHandle.closeConnection();
        } catch (IOException ioe) {
            System.out.println(ioe.getMessage());
            throw new RuntimeException(ioe);
        }

    }
    public static String convertStandardJSONString(String data_json) {
        data_json = data_json.replaceAll("\\\\r\\\\n", "");
        data_json = data_json.replace("\"{", "{");
        data_json = data_json.replace("}\",", "},");
        data_json = data_json.replace("}\"", "}");
        data_json = data_json.replace("\'", "\"");
        data_json = data_json.substring(data_json.indexOf("{"), data_json.lastIndexOf("}") + 1);
        return data_json;
    }
    
    private void parse_and_query(JSONObject message) throws JSONException, IOException {
    	
    	System.out.println("Attempting to create DB handle...");
        DBHandle = DBConnectionFactory.createConnection(message.getString("client_type"), message.getString("database"));
        System.out.println("DB handle created :)");
        
        switch (message.getString("operation")){
            case ("create"):
                DBHandle.create(message.getString("collection"), (JSONObject)message.get("filter"));
            	send_message((new JSONObject().put("result", "create successful")).toString());
                break;
            case("read"):
                JSONObject ret_json = DBHandle.read(message.getString("collection"), message.get("filter"));
            	send_message(ret_json.toString());
                break;
            case("update"):
                DBHandle.update(message.getString("collection"),
                        message.getJSONObject("filter").getJSONObject("filter"),
                        message.getJSONObject("filter").getJSONObject("fields"));
            	send_message((new JSONObject().put("result", "update successful")).toString());
                break;
            case("delete"):
                DBHandle.delete(message.getString("collection"), String.valueOf(message.get("filter")));
            	send_message((new JSONObject().put("result", "delete successful")).toString());
                break;
            case("migrate"):
                DBConnection dest_handle = DBConnectionFactory.createConnection(message.getString("destination"),message.getString("database"));
                DBConnection source_handle = DBConnectionFactory.createConnection(message.getString("source"),message.getString("database"));
                dest_handle.create(message.getString("collection"), source_handle.read(message.getString("collection"), ""));
        }
    }
    
    private void send_message(String message) throws IOException {
    	System.out.println("Sending: "+message+"\n");
    	this.clientSocket.getOutputStream().write(message.getBytes("UTF-8"));
    }
}
