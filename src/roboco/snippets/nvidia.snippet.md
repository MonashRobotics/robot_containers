Add this to the top of your Dockerfile, above the original FROM instruction:
```dockerfile
FROM nvidia/opengl:1.0-glvnd-devel-ubuntu18.04 as glvnd
```

Add this to the middle of your Dockerfile, below the original FROM instruction:
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    libgles2 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=glvnd /usr/share/glvnd/egl_vendor.d/10_nvidia.json /usr/share/glvnd/egl_vendor.d/10_nvidia.json

ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:-all}
```