FROM python:3.9-slim-buster

WORKDIR /app

# Install Xvfb, wget and curl
RUN apt-get update && apt-get install -yq xvfb wget curl

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && apt install -yq ./google-chrome-stable_current_amd64.deb

# Copy the contents onto the container

COPY requirements.txt .

# Install dependencies
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . .

# Set the entrypoint
ENTRYPOINT ["./entry.sh"]
