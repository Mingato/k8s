FROM openjdk:8-jdk
MAINTAINER Gunter Mingato

#${VERSION}

RUN curl -L -u admin:admin -X GET 'http://192.168.100.12:8081/service/rest/v1/search/assets/download?version=${VERSION}&repository=maven-releases&name=auth&group=com.redcompany&maven.extension=jar' -o app.jar


ENTRYPOINT ["java","-jar","app.jar"]
EXPOSE 8080