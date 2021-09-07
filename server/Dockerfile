FROM python:3

WORKDIR /server

RUN apt update
# Install multiarch libs
RUN apt install -y wget
RUN apt update && wget http://archive.ubuntu.com/ubuntu/pool/main/g/glibc/multiarch-support_2.27-3ubuntu1.4_amd64.deb 
RUN apt update && apt-get install ./multiarch-support_2.27-3ubuntu1.4_amd64.deb
# Install Microsoft ODBC Driver for remote database connection
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
#Ubuntu 20.04
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN exit
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
# optional: for bcp and sqlcmd
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools
# Install odbc dependencies
RUN apt-get update \
  && apt-get -y install gcc \
  && apt-get -y install g++ \
  && apt-get -y install unixodbc unixodbc-dev \
  && apt-get clean

COPY . .

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install python server dependencies:
COPY requirements.txt .

RUN pip install -e .
RUN pip install -r requirements.txt

# Run the application:
COPY junco_server.py .
ENV FLASK_APP=junco_server
ENV FLASK_ENV=production
CMD ["python", "junco_server.py"]
