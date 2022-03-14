FROM openjdk:8-jdk
MAINTAINER Gunter Mingato

ARG VERSION
ARG URL_REPOSITORY
ENV URL "${URL_REPOSITORY}/service/rest/v1/search/assets/download?version=${VERSION}&repository=maven-releases&name=notification&group=com.redcompany&maven.extension=jar"

RUN echo "URL = ${URL}"

RUN curl -L -u admin:admin -X GET "${URL}" -o app.jar

ENTRYPOINT ["java","-jar","app.jar"]
EXPOSE 8080