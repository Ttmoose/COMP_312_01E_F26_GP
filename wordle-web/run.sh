#!/bin/bash
set -e

# Detect or configure JAVA_HOME if not already pointing to a valid Java installation
if [ -z "$JAVA_HOME" ] || [ ! -x "$JAVA_HOME/bin/java" ]; then
    if [ -x "/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home/bin/java" ]; then
        export JAVA_HOME="/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home"
    elif [ -x "$(/usr/libexec/java_home 2>/dev/null)" ]; then
        export JAVA_HOME="$(/usr/libexec/java_home)"
    fi
fi

if [ -n "$JAVA_HOME" ]; then
    export PATH="$JAVA_HOME/bin:$PATH"
fi

echo "======================================================"
echo " Starting Wordle Web Application (Spring Boot)       "
echo " Java version: $(java -version 2>&1 | head -n 1)      "
echo " Web UI will be available at: http://localhost:8080   "
echo " Press Ctrl+C to stop the server                      "
echo "======================================================"

cd "$(dirname "$0")"
./mvnw spring-boot:run

