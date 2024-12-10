FROM gradle:8.10.0-jdk21-jammy AS build-env
WORKDIR /
COPY . ./
RUN gradle --no-daemon clean war

FROM tomcat:jre21-temurin-noble
WORKDIR /usr/local/tomcat/webapps
COPY --from=build-env /build/libs/*.war ./server1.war