import javax.net.ssl.*;
import java.io.*;
import java.net.URI;
import java.net.URL;
import java.security.cert.Certificate;
import java.security.cert.X509Certificate;

public class TlsClient {
    public static void main(String[] args) {
        String urlString = "https://bnr.ro/Home.aspx";
        String outputFileName = "bnr_homepage.html";

        try {
            URL url = new URI(urlString).toURL();
            HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();

            connection.setSSLSocketFactory((SSLSocketFactory) SSLSocketFactory.getDefault());
            connection.connect();

            printCertificateDetails(connection);

            saveHtmlContent(connection, outputFileName);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void printCertificateDetails(HttpsURLConnection connection) {
        try {
            Certificate[] certs = connection.getServerCertificates();
            for (Certificate cert : certs) {
                if (cert instanceof X509Certificate x509Cert) {
                    System.out.println("Version: " + x509Cert.getVersion());
                    System.out.println("Serial number: " + x509Cert.getSerialNumber());
                    System.out.println("Issued by: " + x509Cert.getIssuerX500Principal().getName());
                    System.out.println("Not before: " + x509Cert.getNotBefore());
                    System.out.println("Not after: " + x509Cert.getNotAfter());
                    System.out.println("Issued to: " + x509Cert.getSubjectX500Principal().getName());
                    System.out.println("Algorithm: " + x509Cert.getPublicKey().getAlgorithm());
                    System.out.println("Public key: " + x509Cert.getPublicKey());
                }
            }
        } catch (Exception e) {
            System.err.println("Error while getting certificate details: " + e.getMessage());
        }
    }

    private static void saveHtmlContent(HttpsURLConnection connection, String outputFileName) {
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
             BufferedWriter writer = new BufferedWriter(new FileWriter(outputFileName))) {

            String line;
            while ((line = reader.readLine()) != null) {
                writer.write(line);
                writer.newLine();
            }
        } catch (IOException e) {
            System.err.println("Error while saving HTML: " + e.getMessage());
        }
    }
}
