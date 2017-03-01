# Caffe 

# introduction

Caffe is a deep learning framework developed by the Berkeley Vision and Learning Center (BVLC) with cleanliness, readability and speed in mind. It has a clean architecture which enables rapid deployment. It is readable and modifiable, encouraging active development. It is a fast CNN implementation. It has command line, Python and MATLAB interfaces for day-to-day usage, interfacing with research code and rapid prototyping. While Caffe is essentially a C++ library, it has a modular interface for development with cmdcaffe, pycaffe and matcaffe.

The Caffe core software packages are as follows:

- Caffe
- CUDA
- cuDNN
- OpenBLAS
- OpenCV
- Boost

Caffe other dependencies are as follows:

- protobuf
- google-glog
- gflags
- snappy
- leveldb
- lmdb
- hdf5

The Caffe build tools are CMake and make.

# command line

The command line interface cmdcaffe is a Caffe tool for model training, scoring and diagnostics. Run it without arguments for help. It is at directory `caffe/build/tools`.

## train

`caffe train` learns models from scratch, resumes learning from saved snapshots and fine-tunes models to new data and tasks. All training requires a solver configuration through the option `-solver solver.prototxt`. Resuming requires the option `snapshot model_item_1000.solverstate` argument to load the solver snapshot.

```Bash
# train LeNet
caffe train -solver examples/mnist/lenet_solver.prototxt
# train on GPU 2
caffe train -solver examples/mnist/lenet_solver .prototxt -gpu 2
```

## test

`caffe test` scores models by running them in the test phase and resport the network output as its score. The network architecture must be defined properly to output an accuracy measure or loss as its output. The per-batch score is reported and then the grand average is reported last.

```Bash
# score the learned LeNet model on the validation set
as defined in the model architecture lenet_train_test.prototxt
caffe test - model examples/mnist/lenet_train_test.prototxt -weights examples/mnist/lenet_iter_10000 -gpu 0 -iterations 100
```

## benchmark

`caffe time` benchmarks model execution layer-by-layer through timing and synchronisation. This is useful to check system performance and measure relative execution times for models.

```Bash
# time LeNet training on CPU for 10 iterations
caffe time -model examples/mnist/lenet_train_test.prototxt -iterations 10
# time LeNet training on GPU for the default 50 iterations
caffe time -model examples/mnist/lenet_train_test.prototxt - gpu 0
```

## diagnose

`caffe device_query` reports GPU details for reference and checking device ordinals for running on a device in multi-GPU machines.

```Bash
# query the first device
caffe device_query -gpu 0
```

# pycaffe

The Python interface `pycaffe` is the caffe module and its scripts are at the directory `caffe/python`. Run `import caffe` to load models, do forward and backward, handle IO, visualise networks and instrument model-solving. All model data, derivatives and parameters are exposed for reading and writing.

`caffe.Net` is the central interface for loading, configuring and running models. `caffe.Classifier` and `caffe.Detector` provide convenience interfaces for common tasks. `caffe.SGDSolver` exposes the solving interface. `caffe.io` handles input and output with preprocessing and protocol buffers. `caffe.draw` visualises network architectures. Caffe blobs are exposed as numpy ndarrays for ease-of-use and efficiency.

# MATLAB

The MATLAB interface `matcaffe` is the Caffe MATLAB MEX file and its helper m-files are at the directory caffe/matlab. There is example code `caffe/matlab/caffe/matcaffe_demo.m`.

# models

The directory structure of models is as follows:

```Bash
.
├── bvlc_alexnet
│   ├── deploy.prototxt
│   ├── readme.md
│   ├── solver.prototxt
│   └── train_val.prototxt
├── bvlc_googlenet
│   ├── bvlc_googlenet.caffemodel
│   ├── deploy.prototxt
│   ├── quick_solver.prototxt
│   ├── readme.md
│   ├── solver.prototxt
│   └── train_val.prototxt
├── bvlc_reference_caffenet
│   ├── deploy.prototxt
│   ├── readme.md
│   ├── solver.prototxt
│   └── train_val.prototxt
├── bvlc_reference_rcnn_ilsvrc13
│   ├── deploy.prototxt
│   └── readme.md
└── finetune_flickr_style
    ├── deploy.prototxt
    ├── readme.md
    ├── solver.prototxt
    └── train_val.prototxt
```

# draw a graph of network architecture

```Bash
"${CAFFE}"/python/draw_net.py "${CAFFE}"/models/bvlc_googlenet/deploy.prototxt bvlc_googlenet_deploy.png
```

# setup 2015

```Bash
sudo apt-get -y install libprotobuf-dev
sudo apt-get -y install libleveldb-dev
sudo apt-get -y install libsnappy-dev
sudo apt-get -y install libopencv-dev
sudo apt-get -y install libhdf5-dev
sudo apt-get -y install libhdf5-serial-dev
sudo apt-get -y install protobuf-compiler
sudo apt-get -y install --no-install-recommends libboost-all-dev
sudo apt-get -y install libatlas-base-dev
sudo apt-get -y install python-dev
sudo apt-get -y install libgflags-dev
sudo apt-get -y install libgoogle-glog-dev
sudo apt-get -y install liblmdb-dev
sudo apt-get -y install python-pydot
```

```Bash
sudo pip install protobuf
sudo pip install scikit-image
```

```Bash
cd
git clone https://github.com/BVLC/caffe.git
cd caffe
cp Makefile.config.example Makefile.config
```

Edit the makefile. Uncomment `CPU_ONLY := 1` for a non-GPU compilation (without CUDA). It may be necessary to include the following lines:

```
INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial/
LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/x86_64-linux-gnu/hdf5/serial
```

```Bash
time make all
time make test
time make runtest
time make pycaffe
```

```Bash
PYTHONPATH="/home/"${USER}"/caffe/python:${PYTHONPATH}"
CAFFE="/home/"${USER}"/caffe"
```

Download Caffe models from the Model Zoo.

- <http://caffe.berkeleyvision.org/model_zoo.html>
- <https://github.com/BVLC/caffe/wiki/Model-Zoo>

```Bash
~/caffe/scripts/download_model_binary.py models/bvlc_googlenet
```
