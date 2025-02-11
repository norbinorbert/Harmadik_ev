FROM eclipse-temurin:21-alpine
WORKDIR /app
COPY . .
RUN apk add --no-cache curl
RUN curl -o amqp-client-5.15.0.jar https://repo1.maven.org/maven2/com/rabbitmq/amqp-client/5.15.0/amqp-client-5.15.0.jar
RUN curl -o slf4j-api-1.7.36.jar https://repo1.maven.org/maven2/org/slf4j/slf4j-api/1.7.36/slf4j-api-1.7.36.jar \
    && curl -o slf4j-simple-1.7.36.jar https://repo1.maven.org/maven2/org/slf4j/slf4j-simple/1.7.36/slf4j-simple-1.7.36.jar
RUN javac -cp "amqp-client-5.15.0.jar:slf4j-api-1.7.36.jar:slf4j-simple-1.7.36.jar:." Producer.java
CMD ["java", "-cp", "amqp-client-5.15.0.jar:slf4j-api-1.7.36.jar:slf4j-simple-1.7.36.jar:.", "Producer"]
