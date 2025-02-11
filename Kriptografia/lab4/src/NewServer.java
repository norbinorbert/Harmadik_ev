import com.sun.net.httpserver.HttpsConfigurator;
import com.sun.net.httpserver.HttpsServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import javax.net.ssl.*;
import java.io.*;
import java.net.InetSocketAddress;
import java.security.KeyStore;
import java.util.stream.Collectors;

public class NewServer {
    public static void main(String[] args) throws Exception {
        int port = 443;
        String keystoreFile = "server_keystore.jks";
        char[] keystorePassword = "admin1".toCharArray();
        String truststoreFile = "server_truststore.jks";
        char[] truststorePassword = "admin1".toCharArray();

        HttpsServer server = HttpsServer.create(new InetSocketAddress(port), 0);

        SSLContext sslContext = SSLContext.getInstance("TLS");

        KeyStore serverKeyStore = KeyStore.getInstance("JKS");
        try (FileInputStream fis = new FileInputStream(keystoreFile)) {
            serverKeyStore.load(fis, keystorePassword);
        }

        KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
        kmf.init(serverKeyStore, keystorePassword);

        KeyStore trustStore = KeyStore.getInstance("JKS");
        try (FileInputStream fis = new FileInputStream(truststoreFile)) {
            trustStore.load(fis, truststorePassword);
        }

        TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
        tmf.init(trustStore);

        sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);
        server.setHttpsConfigurator(new HttpsConfigurator(sslContext));

        server.createContext("/", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                BufferedReader reader = new BufferedReader(new FileReader("bnr_homepage.html"));
                byte[] response = reader.lines().collect(Collectors.joining("")).getBytes();
                exchange.sendResponseHeaders(200, response.length);
                OutputStream os = exchange.getResponseBody();
                os.write(response);
                os.close();
            }
        });

        server.setExecutor(null);
        server.start();
        System.out.println("Server running on https://localhost:" + port);
    }
}
