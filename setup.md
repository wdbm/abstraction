# setup

The setup generally assumes Ubuntu and an Nvidia GPU.

# set up reference hardware P507 

- model:
    - Schenker XMG P507 (2017)
    - SKU: XMG-P507-KBL
- GPU
    - NVIDIA GeForce GTX 1070 8GB GDDR5 with G-SYNC
    - SKU: GPU-GTX-1070-P507-GSYNC
- CPU
    - Intel Core i7-7820HK, quad Core, 8 threads, 2.90 -- 3.90 GHz, 8 MB, 45 W
    - SKU: KCI-7820HK-P507
- RAM:
    - 32GB (2 x 16384) SO-DIMM DDR4 RAM 2133 MHz Samsung
    - SKU: KR4-2x16GB-2133-SAMSUNG
- HD
    - 512GB m.2 SSD Samsung SM961-NVMe via PCI-Express x4
    - SKU: APHDD-SM961-NVME-M2-512

## boot keys

- F2: access BIOS
- F11: access USB boot

## install Ubuntu and Nvidia graphics drivers

UEFI Boot is enabled by default. Disable it.

- BIOS > Boot > UEFI Boot

Install Ubuntu. Following installation, Ubuntu boots to a flawed interface of just wallpaper without Unity. Boot to Ubuntu recovery mode and use more simple graphics to access Ubuntu and Unity. Launch a terminal and install and engage Nvidia drivers.

```Bash
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
sudo apt install nvidia-367 nvidia-prime
```

Verify the driver version.

```Bash
>cat /proc/driver/nvidia/version
NVRM version: NVIDIA UNIX x86_64 Kernel Module  375.39  Tue Jan 31 20:47:00 PST 2017
GCC version:  gcc version 6.2.0 20161018 (Ubuntu 6.2.0-7ubuntu11)
```

## install CUDA

The Nvidia Compute Unified Device Architecture (CUDA) is a parallel programming architecture.

```Bash
sudo dpkg -i cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64.deb
sudo apt-get update
sudo apt-get install cuda
```

This should install CUDA at directory `/usr/local/cuda-8.0`. Include directory `/usr/local/cuda-8.0/bin` in the `PATH` environment variable.

```Bash
export PATH=/usr/local/cuda-8.0/bin${PATH:+:${PATH}}
```

Test the installation.

```Bash
>nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2016 NVIDIA Corporation
Built on Tue_Jan_10_13:22:03_CST_2017
Cuda compilation tools, release 8.0, V8.0.61
```

## install cuDNN

The NVIDIA CUDA Deep Neural Network library (cuDNN) is a library for machine learning. Register for a developer account. Install cuDNN v5.1 Library for Linux.

```Bash
tar -xvf cudnn-8.0-linux-x64-v5.1.tgz
```

The cuDNN archive contains the following:

```Bash
cuda/include/cudnn.h
cuda/lib64/libcudnn.so
cuda/lib64/libcudnn.so.5
cuda/lib64/libcudnn.so.5.1.10
cuda/lib64/libcudnn_static.a
```

```Bash
sudo cp cuda/include/cudnn.h /usr/local/cuda-8.0/include/
sudo cp cuda/lib64/* /usr/local/cuda-8.0/lib64/
```

## set up GCC

Install and change to GCC 4.9 for CUDA.

```Bash
sudo apt-get install gcc-4.9 g++-4.9
```

The existing GCC and g++ links are as follows:

```Bash
>ls -al /usr/bin/gcc
lrwxrwxrwx 1 root root 5 Feb 24 15:13 /usr/bin/gcc -> gcc-6
>ls -al /usr/bin/g++
lrwxrwxrwx 1 root root 5 Feb 24 15:13 /usr/bin/g++ -> g++-6
```

Change the symlinks for GCC and g++ to GCC 4.9.

```Bash
ln -fs /usr/bin/gcc-4.9 /usr/bin/gcc
ln -fs /usr/bin/g++-4.9 /usr/bin/g++
```

## set up OpenCL (2017-03-08T1827Z experimental)

OpenCL is included with CUDA. Create a symbolic link to the Nvidia OpenCL headers at `/usr/include`.

```Bash
sudo ln -s /usr/include/nvidia-375/CL /usr/include
```

## install CUPTI

The NVIDIA CUDA Profiling Tools Interface (CUPTI) provides performance analysis tools with detailed information about how applications are using the GPUs of a system.

```Bash
sudo apt-get install libcupti-dev
```

# pip, Miniconda

`pip` can install system-wide or locally. [Miniconda] can simplify the setup of Python, pip and other modules.

To install Miniconda, follow a procedure like the following:

```Bash
wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
bash Miniconda2-latest-Linux-x86_64.sh
```

Following the prompts. The default install directory is `${HOME}/miniconda2` or `${HOME}/miniconda3`.

# install TensorFlow

Install TensorFlow 1.0.0.

```Bash
sudo apt-get -y install python-pip
sudo apt-get -y install python-dev
sudo pip install tensorflow-gpu
```

# set up abstraction 2017-02-28

Install ROOT.

```Bash
wget https://raw.githubusercontent.com/wdbm/soil/master/setup.sh
chmod 755 setup.sh
./setup.sh
rm setup.sh
```

# set up other dependencies and abstraction (2017-03-21 upcoming)

```Bash
sudo apt-get -y install festival    \
                        pylint      \
                        snakefood   \
                        sqlite      \
                        sqliteman   \
                        python-nltk

sudo python -m nltk.downloader all

sudo easy_install -U gensim

sudo pip install abstraction

git clone https://github.com/wdbm/abstraction.git
```

The function `abstraction.setup()` should be run.
