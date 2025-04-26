FROM python:3.13

# OCI metadata
LABEL org.opencontainers.image.title="PlexSubSync"
LABEL org.opencontainers.image.description="Dockerized subtitle synchronization service for Plex with FastAPI wrapper and sc0ty/subsync"
LABEL org.opencontainers.image.url="https://github.com/ChrisHansenTech/PlexSubSync"
LABEL org.opencontainers.image.source="https://github.com/ChrisHansenTech/PlexSubSync"
LABEL org.opencontainers.image.license="MIT"
LABEL org.opencontainers.image.vendor="ChrisHansenTech"

# Expose the application port and config volume
EXPOSE 8000

# Install system dependencies
RUN apt-get update -y && apt-get install -y python3-pybind11 libsphinxbase-dev libpocketsphinx-dev ffmpeg libavdevice-dev

WORKDIR /app/subsync

# Download latest version
RUN git clone https://github.com/sc0ty/subsync.git .

# Copy config file
COPY ./config.py subsync/config.py

# Create /config and set permissions
RUN mkdir config && chmod 777 config

# Install requirements and build
RUN pip install .

WORKDIR /app/plexsubsync

COPY ./src .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]