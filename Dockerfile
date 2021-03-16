# Base docker image
FROM python:3

# Send python output straight to terminal
ENV PYTHONUNBUFFERED=1

# Install Microsoft ODBC SQL driver
# https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15#debian17
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Install ODBC headers, required by Django
RUN apt-get install -y unixodbc-dev
RUN apt-get clean -y

WORKDIR /code

# Install Python requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy remaining source code
COPY ./cc_midterm ./

# Run server, listening for any IP at port 8000
CMD python manage.py runserver 0:8000
