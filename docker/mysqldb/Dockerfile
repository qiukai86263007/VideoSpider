# Use an official MySQL 8.0 image as a base
FROM mysql:8.0

# Install Python 3.10 and other dependencies
#RUN apt-get update && \
#    apt-get install -y software-properties-common && \
#    add-apt-repository ppa:deadsnakes/ppa && \
#    apt-get update && \
#    apt-get install -y python3.10 python3.10-dev python3.10-venv python3-pip && \
#    apt-get clean
ENV MYSQL_ROOT_PASSWORD=Admin1234!
# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
#COPY requirements.txt .

# Install Python dependencies
#RUN python3.10 -m pip install --upgrade pip && \
#    python3.10 -m pip install -r requirements.txt

# Expose the MySQL port
EXPOSE 3306

# Set the default command to run python django server
CMD ["mysqld"]