FROM ghcr.io/otischung/pros_ai_image:1.3.5

RUN rm -rf /workspaces/src/*
COPY ./src /workspaces/src

WORKDIR /workspaces

RUN pip install --no-cache-dir -r /workspaces/src/requirements.txt
CMD ["bash", "-l"]