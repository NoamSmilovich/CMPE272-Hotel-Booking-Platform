import com.opencsv.CSVWriter;

import java.io.FileWriter;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ListeningServer {
    private ExecutorService threadPool;
    private ServerSocket server;

    public ListeningServer() throws IOException {
        server = new ServerSocket(8080);
        server.setReuseAddress(true);

        // Create a thread pool with 10 threads
        threadPool = Executors.newFixedThreadPool(10);
        	
        System.out.println("Server running, listening for connection requests...");
        while (true) {
            Socket client = server.accept();
            System.out.println("New client connected: " + client.getInetAddress().getHostAddress());
            ClientHandler clientSock = new ClientHandler(client);

            // Submit the client handler to the thread pool
            threadPool.submit(clientSock);
        }
    }

    public static void main(String[] args) {
//        test_db_connection(DBConnectionFactory.createConnection("mongodb", "hotels_db"));
//        test_db_connection(DBConnectionFactory.createConnection("mysql", "hotels_db"));
//        simulation();
        try {
            new ListeningServer();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void simulation() {
        // create data to write to CSV file
        String[] headers = {"#Reads", "MongoDB Time (ms)", "MySQL Time (ms)"};
        // create CSV writer and file writer objects
        CSVWriter csvWriter = null;
        FileWriter fileWriter = null;
        try {
            // create file writer object with file name
            fileWriter = new FileWriter("results.csv");
            // create CSV writer object with file writer and options
            csvWriter = new CSVWriter(fileWriter,
                    CSVWriter.DEFAULT_SEPARATOR,    // delimiter character
                    CSVWriter.NO_QUOTE_CHARACTER,  // quote character
                    CSVWriter.DEFAULT_ESCAPE_CHARACTER,  // escape character
                    CSVWriter.DEFAULT_LINE_END);  // line ending character
            // write header row to CSV file
            csvWriter.writeNext(headers);
            // write data rows to CSV file
            int mongodb_res, mysql_res;

            for (int i = 1; i < 100; i++) {
                mongodb_res = test_db_connection(i*10, DBConnectionFactory.createConnection("mongodb", "hotels_db"));
                mysql_res = test_db_connection(i*10, DBConnectionFactory.createConnection("mysql", "hotels_db"));
                String[] row = { String.valueOf(i), String.valueOf(mongodb_res), String.valueOf(mysql_res) };
                csvWriter.writeNext(row);
                System.out.println(i);
            }

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            // close the CSV writer and file writer objects
            try {
                if (csvWriter != null) {
                    csvWriter.close();
                }
                if (fileWriter != null) {
                    fileWriter.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public static int test_db_connection(int iterations, DBConnection DBHandle){
        long startTime = System.nanoTime();
        for(int i=0;i<iterations;i++)
            DBHandle.read("hotels", "");
        long endTime = System.nanoTime();
        long elapsedTime = endTime - startTime;
        return (int)(elapsedTime/1000000);
    }
}