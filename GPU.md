# GPU

# NVIDIA System Management Interface

The NVIDIA System Management Interface (nvidia-smi) is a command line utility that uses the Nvidia Management Library (NVML) to aid in the management and monitoring of Nvidia GPU devices.

```Bash
>watch -n 0.5 nvidia-smi
Sun Feb 26 22:42:48 2017       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 375.39                 Driver Version: 375.39                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX 1070    Off  | 0000:01:00.0     Off |                  N/A |
| N/A   46C    P0    35W /  N/A |    377MiB /  8114MiB |      7%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID  Type  Process name                               Usage      |
|=============================================================================|
|    0      1356    G   /usr/lib/xorg/Xorg                             221MiB |
|    0      2308    G   /usr/bin/compiz                                126MiB |
|    0     14404    G   ...sionActionRedesign/Enabled/GoogleBrandedC    27MiB |
+-----------------------------------------------------------------------------+
```

[tmux-control](https://github.com/wdbm/tmux-control) can be used to display `htop` and `nvidia-smi` in the same terminal using `tmux`.

```Bash
tmux-control.py --nvidia
```

[gpustat](https://github.com/wookayin/gpustat) is a simple command-line script (wrapper for `nvidia-smi` for querying and monitoring GPU status.

# CUDA Samples

```Bash
sudo su
cd /usr/local/cuda-8.0/samples
make
```

```Bash
>/usr/local/cuda-8.0/samples/1_Utilities/deviceQuery/deviceQuery

Starting...

 CUDA Device Query (Runtime API) version (CUDART static linking)

Detected 1 CUDA Capable device(s)

Device 0: "GeForce GTX 1070"
  CUDA Driver Version / Runtime Version          8.0 / 8.0
  CUDA Capability Major/Minor version number:    6.1
  Total amount of global memory:                 8114 MBytes (8508145664 bytes)
  (16) Multiprocessors, (128) CUDA Cores/MP:     2048 CUDA Cores
  GPU Max Clock rate:                            1695 MHz (1.70 GHz)
  Memory Clock rate:                             4004 Mhz
  Memory Bus Width:                              256-bit
  L2 Cache Size:                                 2097152 bytes
  Maximum Texture Dimension Size (x,y,z)         1D=(131072), 2D=(131072, 65536), 3D=(16384, 16384, 16384)
  Maximum Layered 1D Texture Size, (num) layers  1D=(32768), 2048 layers
  Maximum Layered 2D Texture Size, (num) layers  2D=(32768, 32768), 2048 layers
  Total amount of constant memory:               65536 bytes
  Total amount of shared memory per block:       49152 bytes
  Total number of registers available per block: 65536
  Warp size:                                     32
  Maximum number of threads per multiprocessor:  2048
  Maximum number of threads per block:           1024
  Max dimension size of a thread block (x,y,z): (1024, 1024, 64)
  Max dimension size of a grid size    (x,y,z): (2147483647, 65535, 65535)
  Maximum memory pitch:                          2147483647 bytes
  Texture alignment:                             512 bytes
  Concurrent copy and kernel execution:          Yes with 2 copy engine(s)
  Run time limit on kernels:                     Yes
  Integrated GPU sharing Host Memory:            No
  Support host page-locked memory mapping:       Yes
  Alignment requirement for Surfaces:            Yes
  Device has ECC support:                        Disabled
  Device supports Unified Addressing (UVA):      Yes
  Device PCI Domain ID / Bus ID / location ID:   0 / 1 / 0
  Compute Mode:
     < Default (multiple host threads can use ::cudaSetDevice() with device simultaneously) >

deviceQuery, CUDA Driver = CUDART, CUDA Driver Version = 8.0, CUDA Runtime Version = 8.0, NumDevs = 1, Device0 = GeForce GTX 1070
Result = PASS
```

```Bash
/usr/local/cuda-8.0/samples/1_Utilities/bandwidthTest/bandwidthTest

[CUDA Bandwidth Test] - Starting...
Running on...

 Device 0: GeForce GTX 1070
 Quick Mode

 Host to Device Bandwidth, 1 Device(s)
 PINNED Memory Transfers
   Transfer Size (Bytes)	Bandwidth(MB/s)
   33554432			12264.1

 Device to Host Bandwidth, 1 Device(s)
 PINNED Memory Transfers
   Transfer Size (Bytes)	Bandwidth(MB/s)
   33554432			12386.7

 Device to Device Bandwidth, 1 Device(s)
 PINNED Memory Transfers
   Transfer Size (Bytes)	Bandwidth(MB/s)
   33554432			192516.0

Result = PASS

NOTE: The CUDA Samples are not meant for performance measurements. Results may vary when GPU Boost is enabled.
```
