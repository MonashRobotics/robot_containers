
## Running

```
./build.py [robot]-[rosdistro]
./run.py [robot]-[rosdistro]
```

e.g.
```
./build.py jackal-foxy
./run.py jackal-foxy
```

See [build.py](build.py) for supported robot and rosdistro combinations.

### Notes on GUI/GPU support

https://github.com/osrf/rocker/tree/main/src/rocker/templates

https://github.com/dusty-nv/jetson-containers

### How to create a .repos file for use by vcstool

```
git clone https://repo-a.git
git clone https://repo-b.git
vcs export > sourcecode.repos
```