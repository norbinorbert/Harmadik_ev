import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Channel;

public class Producer {
    public static void main(String[] args) throws Exception {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("rabbitmq");
        factory.setUsername("guest");
        factory.setPassword("guest");

        try (var connection = factory.newConnection(); var channel = connection.createChannel()) {
            channel.exchangeDeclare("fanout_exchange", "fanout");

            String message = "New Landmark Added";
            for(int i=0; i<5; i++){
                Thread.sleep(5000);
                channel.basicPublish("fanout_exchange", "", null, message.getBytes("UTF-8"));
                System.out.println(" [Java Producer] Sent '" + message + "'");
            }
        }
    }
}
