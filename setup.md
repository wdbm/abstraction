# setup 2018-09-18T1512Z

The setup generally assumes Ubuntu 18.04 LTS and an Nvidia 1070 GPU.

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
sudo apt install nvidia-396 nvidia-prime
```

Verify the driver version.

```Bash
$ cat /proc/driver/nvidia/version
NVRM version: NVIDIA UNIX x86_64 Kernel Module  396.37  Tue Jun 12 13:47:27 PDT 2018
GCC version:  gcc version 7.3.0 (Ubuntu 7.3.0-16ubuntu3)
```

## install CUDA 9.0

The Nvidia Compute Unified Device Architecture (CUDA) is a parallel programming architecture.

```Bash
curl -O -L --remote-header-name https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda-repo-ubuntu1704-9-0-local_9.0.176-1_amd64-deb
curl -O -L --remote-header-name https://developer.nvidia.com/compute/cuda/9.0/Prod/patches/1/cuda-repo-ubuntu1704-9-0-local-cublas-performance-update_1.0-1_amd64-deb
curl -O -L --remote-header-name https://developer.nvidia.com/compute/cuda/9.0/Prod/patches/2/cuda-repo-ubuntu1704-9-0-local-cublas-performance-update-2_1.0-1_amd64-deb
curl -O -L --remote-header-name https://developer.nvidia.com/compute/cuda/9.0/Prod/patches/3/cuda-repo-ubuntu1704-9-0-local-cublas-performance-update-3_1.0-1_amd64-deb
curl -O -L --remote-header-name https://developer.nvidia.com/compute/cuda/9.0/Prod/patches/4/cuda-repo-ubuntu1704-9-0-176-local-patch-4_1.0-1_amd64-deb

sudo dpkg -i cuda-repo-ubuntu1704-9-0-local_9.0.176-1_amd64-deb
sudo apt update
sudo apt install cuda-9-0
sudo dpkg -i cuda-repo-ubuntu1704-9-0-local-cublas-performance-update_1.0-1_amd64-deb
sudo dpkg -i cuda-repo-ubuntu1704-9-0-local-cublas-performance-update-2_1.0-1_amd64-deb
sudo dpkg -i cuda-repo-ubuntu1704-9-0-local-cublas-performance-update-3_1.0-1_amd64-deb
sudo dpkg -i cuda-repo-ubuntu1704-9-0-176-local-patch-4_1.0-1_amd64-deb
```

This should install CUDA at directory `/usr/local/cuda-9.0` (and at `/usr/local/cuda`). Include directory `/usr/local/cuda/bin` in the `PATH` environment variable.

```Bash
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
```

Test the installation.

```Bash
$ nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2017 NVIDIA Corporation
Built on Fri_Sep__1_21:08:03_CDT_2017
Cuda compilation tools, release 9.0, V9.0.176
```

```Bash
export LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64/stubs/:$LD_LIBRARY_PATH
sudo chown -R $USER:$USER /usr/local/cuda-9.0/
sudo chmod -R 777 /usr/local/cuda-9.0/
```

## install cuDNN

The NVIDIA CUDA Deep Neural Network library (cuDNN) is a library for machine learning. Register for a developer account. Install cuDNN v7.2.1 Library for Linux for CUDA 9.0.

```Bash
tar -xvf cudnn-9.0-linux-x64-v7.2.1.38.tgz
```

The cuDNN archive contains the following:

```Bash
cuda/include/cudnn.h
cuda/NVIDIA_SLA_cuDNN_Support.txt
cuda/lib64/libcudnn.so
cuda/lib64/libcudnn.so.7
cuda/lib64/libcudnn.so.7.2.1
cuda/lib64/libcudnn_static.a
```

Copy cuDNN to the CUDA Tookkit directory and change the file permissions.

```Bash
sudo cp cuda/include/cudnn.h /usr/local/cuda-9.0/include/
sudo cp cuda/lib64/* /usr/local/cuda-9.0/lib64/
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda-9.0/lib64/libcudnn*
```

# install TensorFlow

Install TensorFlow.

```Bash
sudo pip3 install tf-nightly-gpu
```

# test Tensorflow

```Python
import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
sess.run(hello)

a = tf.constant(10)
b = tf.constant(32)
sess.run(a + b)
sess.close()
```

# other instructions

Now follow some of the old instructions.

---

# setup (old)

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
sudo apt install nvidia-384 nvidia-prime
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

## set up GCC (2018-04-12T0135Z possibly unnecessary)

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

`pip` can install system-wide or locally. Miniconda can simplify the setup of Python, pip and other modules.

To install Miniconda, follow a procedure like the following:

```Bash
wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
bash Miniconda2-latest-Linux-x86_64.sh
```

Following the prompts. The default install directory is `${HOME}/miniconda2` or `${HOME}/miniconda3`.

# install TensorFlow

Install TensorFlow.

```Bash
sudo apt-get -y install python-pip
sudo apt-get -y install python-dev
pip install tensorflow-gpu
#pip install tensorflow # CPU
```

# set up ROOT 2017-04-21

Install CMake.

```Bash
sudo apt-get remove cmake

wget https://cmake.org/files/v3.8/cmake-3.8.0-Linux-x86_64.sh
sudo sh cmake-3.8.0-Linux-x86_64.sh --prefix=/opt/cmake
PATH="/opt/cmake/cmake-3.8.0-Linux-x86_64/bin:"${PATH}""
```

Install ROOT.

```Bash
wget https://raw.githubusercontent.com/wdbm/soil/master/setup.sh
chmod 755 setup.sh
./setup.sh
rm setup.sh
```

# set up tmux-control

```Bash
sudo apt-get -y install cmus   \
                        elinks \
                        htop   \
                        ranger \
                        tmux

pip install tmux_control
```

# set up other dependencies and abstraction (2017-03-21 upcoming)

- Install [tonescale](https://github.com/wdbm/tonescale).

```Bash
sudo apt-get -y install festival    \
                        pylint      \
                        snakefood   \
                        sqlite      \
                        sqliteman   \
                        python-nltk

pip install nltk
sudo python -m nltk.downloader all
sudo easy_install -U gensim
pip install gensim
pip install sklearn
pip install abstraction
git clone https://github.com/wdbm/abstraction.git
```

Create a PRAW credentials file `~/.reddit`. Its contents should have the following form:

```Python
client_id     = "xxxxxxxxxxxxxx"
client_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxx"
user_agent    = "xxxxxxxxxx"
```

The function `abstraction.setup()` should be run.

---

# uninstall

## uninstall TensorFlow

```Bash
sudo pip2 uninstall tensorflow-cpu
sudo pip3 uninstall tensorflow-cpu

sudo pip2 uninstall tensorflow-gpu
sudo pip3 uninstall tensorflow-gpu
```

For TensorFlow 1.0.1 CPU, the procedure is as follows:

```Bash
sudo pip2 uninstall tensorflow
sudo pip3 uninstall tensorflow
```

## uninstall CUPTI

```Bash
sudo apt remove libcupti-dev
```

## uninstall cuDNN and CUDA 8.0

There is no need to explicitly remove cuDNN in isolation, as it is removed along with CUDA 8.0.

```Bash
sudo apt remove cuda
sudo apt autoremove
sudo apt remove --purge cuda
```

The `autoremove` step removes about 2 GB for CUDA 8.0. The CUDA 8.0 directory (`/usr/local/cuda-8.0/`) should be removed now.

```Bash
sudo apt remove cuda-repo-ubuntu1604-8-0-local-ga2
sudo apt clean
sudo apt autoclean
```

The `remove cuda-repo-ubuntu1604-8-0-local-ga2` step removes about 2 GB for CUDA 8.0.
