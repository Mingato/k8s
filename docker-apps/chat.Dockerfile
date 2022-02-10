FROM openjdk:8-jdk
MAINTAINER Gunter Mingato

RUN curl -L -u admin:admin -X GET 'http://192.168.100.12:8081/service/rest/v1/search/assets/download?sort=version&repository=maven-releases&name=chat&group=com.redcompany&maven.extension=jar' -o app.jar

ENTRYPOINT ["java","-jar","app.jar"]
EXPOSE 8080