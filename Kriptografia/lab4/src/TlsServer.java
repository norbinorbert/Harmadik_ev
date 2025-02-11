import com.sun.net.httpserver.HttpsConfigurator;
import com.sun.net.httpserver.HttpsServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import javax.net.ssl.*;
import java.io.*;
import java.net.InetSocketAddress;
import java.security.KeyStore;
import java.util.stream.Collectors;

public class TlsServer {
    public static void main(String[] args) throws Exception {
        int port = 443;
        String keystoreFile = "bnr_fake.jks";
        char[] password = ("admin1".toCharArray());

        HttpsServer server = HttpsServer.create(new InetSocketAddress(port), 0);

        SSLContext sslContext = SSLContext.getInstance("TLS");
        KeyStore ks = KeyStore.getInstance("JKS");
        FileInputStream fis = new FileInputStream(keystoreFile);
        ks.load(fis, password);

        KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
        kmf.init(ks, password);

        TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
        tmf.init(ks);

        sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);
        server.setHttpsConfigurator(new HttpsConfigurator(sslContext));

        server.createContext("/", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                BufferedReader bufferedReader = new BufferedReader(new FileReader("bnr_homepage.html"));
                byte[] response = bufferedReader.lines().collect(Collectors.joining("")).getBytes();
                exchange.sendResponseHeaders(200, response.length);
                OutputStream os = exchange.getResponseBody();
                os.write(response);
                os.close();
            }
        });

        server.setExecutor(null);
        server.start();
        System.out.println("Fake server running on https://localhost:" + port);
    }
}
