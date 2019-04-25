# 2019-04-25T1414Z benchmark

According to [this](https://stackoverflow.com/a/44327563/7558518), a GTX 1070 can take ~5 ms per step with the following TensorFlow convolutional neural network.

```Bash
$ git clone https://github.com/tensorflow/models.git
Cloning into 'models'...
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 25412 (delta 0), reused 1 (delta 0), pack-reused 25407
Receiving objects: 100% (25412/25412), 507.93 MiB | 19.81 MiB/s, done.
Resolving deltas: 100% (15196/15196), done.
Checking out files: 100% (2879/2879), done.
$ python3 models/tutorials/image/mnist/convolutional.py 
Successfully downloaded train-images-idx3-ubyte.gz 9912422 bytes.
Successfully downloaded train-labels-idx1-ubyte.gz 28881 bytes.
Successfully downloaded t10k-images-idx3-ubyte.gz 1648877 bytes.
Successfully downloaded t10k-labels-idx1-ubyte.gz 4542 bytes.
Extracting data/train-images-idx3-ubyte.gz
Extracting data/train-labels-idx1-ubyte.gz
Extracting data/t10k-images-idx3-ubyte.gz
Extracting data/t10k-labels-idx1-ubyte.gz
2019-04-25 15:12:50.104773: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2019-04-25 15:12:50.192124: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:964] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2019-04-25 15:12:50.192552: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1432] Found device 0 with properties: 
name: GeForce GTX 1070 major: 6 minor: 1 memoryClockRate(GHz): 1.695
pciBusID: 0000:01:00.0
totalMemory: 7.93GiB freeMemory: 7.74GiB
2019-04-25 15:12:50.192584: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1511] Adding visible gpu devices: 0
2019-04-25 15:12:50.378594: I tensorflow/core/common_runtime/gpu/gpu_device.cc:982] Device interconnect StreamExecutor with strength 1 edge matrix:
2019-04-25 15:12:50.378642: I tensorflow/core/common_runtime/gpu/gpu_device.cc:988]      0 
2019-04-25 15:12:50.378648: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1001] 0:   N 
2019-04-25 15:12:50.378846: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1115] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 7466 MB memory) -> physical GPU (device: 0, name: GeForce GTX 1070, pci bus id: 0000:01:00.0, compute capability: 6.1)
Initialized!
Step 0 (epoch 0.00), 10.0 ms
Minibatch loss: 8.334, learning rate: 0.010000
Minibatch error: 85.9%
Validation error: 84.5%
Step 100 (epoch 0.12), 4.2 ms
Minibatch loss: 3.223, learning rate: 0.010000
Minibatch error: 3.1%
Validation error: 7.7%
Step 200 (epoch 0.23), 4.0 ms
Minibatch loss: 3.402, learning rate: 0.010000
Minibatch error: 12.5%
Validation error: 4.3%
Step 300 (epoch 0.35), 3.9 ms
Minibatch loss: 3.158, learning rate: 0.010000
Minibatch error: 4.7%
Validation error: 3.1%
Step 400 (epoch 0.47), 3.9 ms
Minibatch loss: 3.231, learning rate: 0.010000
Minibatch error: 6.2%
Validation error: 2.8%
Step 500 (epoch 0.58), 3.9 ms
Minibatch loss: 3.159, learning rate: 0.010000
Minibatch error: 3.1%
Validation error: 2.7%
Step 600 (epoch 0.70), 3.9 ms
Minibatch loss: 3.121, learning rate: 0.010000
Minibatch error: 3.1%
Validation error: 2.2%
Step 700 (epoch 0.81), 4.0 ms
Minibatch loss: 2.950, learning rate: 0.010000
Minibatch error: 0.0%
Validation error: 2.1%
Step 800 (epoch 0.93), 4.0 ms
Minibatch loss: 3.055, learning rate: 0.010000
Minibatch error: 6.2%
Validation error: 2.1%
Step 900 (epoch 1.05), 4.1 ms
Minibatch loss: 2.923, learning rate: 0.009500
Minibatch error: 1.6%
Validation error: 1.8%
Step 1000 (epoch 1.16), 4.1 ms
Minibatch loss: 2.897, learning rate: 0.009500
Minibatch error: 1.6%
Validation error: 1.8%
Step 1100 (epoch 1.28), 4.2 ms
Minibatch loss: 2.815, learning rate: 0.009500
Minibatch error: 0.0%
Validation error: 1.4%
Step 1200 (epoch 1.40), 4.2 ms
Minibatch loss: 2.909, learning rate: 0.009500
Minibatch error: 3.1%
Validation error: 1.6%
Step 1300 (epoch 1.51), 4.2 ms
Minibatch loss: 2.776, learning rate: 0.009500
Minibatch error: 0.0%
Validation error: 1.6%
Step 1400 (epoch 1.63), 4.2 ms
Minibatch loss: 2.821, learning rate: 0.009500
Minibatch error: 1.6%
Validation error: 1.7%
Step 1500 (epoch 1.75), 4.2 ms
Minibatch loss: 2.902, learning rate: 0.009500
Minibatch error: 4.7%
Validation error: 1.2%
Step 1600 (epoch 1.86), 4.1 ms
Minibatch loss: 2.733, learning rate: 0.009500
Minibatch error: 3.1%
Validation error: 1.5%
Step 1700 (epoch 1.98), 4.2 ms
Minibatch loss: 2.650, learning rate: 0.009500
Minibatch error: 0.0%
Validation error: 1.5%
Step 1800 (epoch 2.09), 4.2 ms
Minibatch loss: 2.648, learning rate: 0.009025
Minibatch error: 1.6%
Validation error: 1.4%
Step 1900 (epoch 2.21), 4.9 ms
Minibatch loss: 2.626, learning rate: 0.009025
Minibatch error: 1.6%
Validation error: 1.3%
Step 2000 (epoch 2.33), 3.8 ms
Minibatch loss: 2.605, learning rate: 0.009025
Minibatch error: 1.6%
Validation error: 1.2%
Step 2100 (epoch 2.44), 3.9 ms
Minibatch loss: 2.566, learning rate: 0.009025
Minibatch error: 0.0%
Validation error: 1.2%
Step 2200 (epoch 2.56), 4.0 ms
Minibatch loss: 2.594, learning rate: 0.009025
Minibatch error: 3.1%
Validation error: 1.2%
Step 2300 (epoch 2.68), 3.9 ms
Minibatch loss: 2.598, learning rate: 0.009025
Minibatch error: 1.6%
Validation error: 1.3%
Step 2400 (epoch 2.79), 3.9 ms
Minibatch loss: 2.503, learning rate: 0.009025
Minibatch error: 0.0%
Validation error: 1.2%
Step 2500 (epoch 2.91), 3.9 ms
Minibatch loss: 2.468, learning rate: 0.009025
Minibatch error: 0.0%
Validation error: 1.3%
Step 2600 (epoch 3.03), 3.9 ms
Minibatch loss: 2.476, learning rate: 0.008574
Minibatch error: 1.6%
Validation error: 1.2%
Step 2700 (epoch 3.14), 3.9 ms
Minibatch loss: 2.468, learning rate: 0.008574
Minibatch error: 3.1%
Validation error: 1.2%
Step 2800 (epoch 3.26), 3.9 ms
Minibatch loss: 2.444, learning rate: 0.008574
Minibatch error: 3.1%
Validation error: 1.2%
Step 2900 (epoch 3.37), 4.0 ms
Minibatch loss: 2.447, learning rate: 0.008574
Minibatch error: 3.1%
Validation error: 1.0%
Step 3000 (epoch 3.49), 4.0 ms
Minibatch loss: 2.404, learning rate: 0.008574
Minibatch error: 1.6%
Validation error: 0.9%
Step 3100 (epoch 3.61), 3.9 ms
Minibatch loss: 2.366, learning rate: 0.008574
Minibatch error: 1.6%
Validation error: 0.9%
Step 3200 (epoch 3.72), 3.8 ms
Minibatch loss: 2.358, learning rate: 0.008574
Minibatch error: 1.6%
Validation error: 1.1%
Step 3300 (epoch 3.84), 4.0 ms
Minibatch loss: 2.335, learning rate: 0.008574
Minibatch error: 1.6%
Validation error: 1.0%
Step 3400 (epoch 3.96), 4.0 ms
Minibatch loss: 2.302, learning rate: 0.008574
Minibatch error: 0.0%
Validation error: 1.1%
Step 3500 (epoch 4.07), 3.9 ms
Minibatch loss: 2.283, learning rate: 0.008145
Minibatch error: 0.0%
Validation error: 1.0%
Step 3600 (epoch 4.19), 3.9 ms
Minibatch loss: 2.251, learning rate: 0.008145
Minibatch error: 0.0%
Validation error: 1.0%
Step 3700 (epoch 4.31), 3.9 ms
Minibatch loss: 2.228, learning rate: 0.008145
Minibatch error: 0.0%
Validation error: 0.9%
Step 3800 (epoch 4.42), 4.0 ms
Minibatch loss: 2.222, learning rate: 0.008145
Minibatch error: 0.0%
Validation error: 1.0%
Step 3900 (epoch 4.54), 4.0 ms
Minibatch loss: 2.262, learning rate: 0.008145
Minibatch error: 4.7%
Validation error: 1.1%
Step 4000 (epoch 4.65), 4.0 ms
Minibatch loss: 2.255, learning rate: 0.008145
Minibatch error: 3.1%
Validation error: 0.9%
Step 4100 (epoch 4.77), 4.2 ms
Minibatch loss: 2.204, learning rate: 0.008145
Minibatch error: 1.6%
Validation error: 0.9%
Step 4200 (epoch 4.89), 4.1 ms
Minibatch loss: 2.153, learning rate: 0.008145
Minibatch error: 0.0%
Validation error: 1.0%
Step 4300 (epoch 5.00), 4.1 ms
Minibatch loss: 2.216, learning rate: 0.007738
Minibatch error: 1.6%
Validation error: 1.1%
Step 4400 (epoch 5.12), 4.1 ms
Minibatch loss: 2.123, learning rate: 0.007738
Minibatch error: 0.0%
Validation error: 1.2%
Step 4500 (epoch 5.24), 4.2 ms
Minibatch loss: 2.184, learning rate: 0.007738
Minibatch error: 6.2%
Validation error: 1.0%
Step 4600 (epoch 5.35), 4.3 ms
Minibatch loss: 2.085, learning rate: 0.007738
Minibatch error: 0.0%
Validation error: 1.0%
Step 4700 (epoch 5.47), 4.0 ms
Minibatch loss: 2.101, learning rate: 0.007738
Minibatch error: 1.6%
Validation error: 0.9%
Step 4800 (epoch 5.59), 3.9 ms
Minibatch loss: 2.076, learning rate: 0.007738
Minibatch error: 1.6%
Validation error: 0.9%
Step 4900 (epoch 5.70), 4.1 ms
Minibatch loss: 2.079, learning rate: 0.007738
Minibatch error: 3.1%
Validation error: 0.9%
Step 5000 (epoch 5.82), 3.9 ms
Minibatch loss: 2.124, learning rate: 0.007738
Minibatch error: 3.1%
Validation error: 0.9%
Step 5100 (epoch 5.93), 3.9 ms
Minibatch loss: 2.003, learning rate: 0.007738
Minibatch error: 0.0%
Validation error: 1.0%
Step 5200 (epoch 6.05), 4.0 ms
Minibatch loss: 2.076, learning rate: 0.007351
Minibatch error: 1.6%
Validation error: 1.0%
Step 5300 (epoch 6.17), 3.9 ms
Minibatch loss: 1.973, learning rate: 0.007351
Minibatch error: 0.0%
Validation error: 1.1%
Step 5400 (epoch 6.28), 3.9 ms
Minibatch loss: 1.961, learning rate: 0.007351
Minibatch error: 0.0%
Validation error: 1.0%
Step 5500 (epoch 6.40), 3.9 ms
Minibatch loss: 1.977, learning rate: 0.007351
Minibatch error: 3.1%
Validation error: 1.1%
Step 5600 (epoch 6.52), 4.0 ms
Minibatch loss: 1.928, learning rate: 0.007351
Minibatch error: 0.0%
Validation error: 0.8%
Step 5700 (epoch 6.63), 4.1 ms
Minibatch loss: 1.914, learning rate: 0.007351
Minibatch error: 0.0%
Validation error: 0.8%
Step 5800 (epoch 6.75), 4.1 ms
Minibatch loss: 1.899, learning rate: 0.007351
Minibatch error: 0.0%
Validation error: 0.9%
Step 5900 (epoch 6.87), 4.2 ms
Minibatch loss: 1.895, learning rate: 0.007351
Minibatch error: 0.0%
Validation error: 1.0%
Step 6000 (epoch 6.98), 4.0 ms
Minibatch loss: 1.896, learning rate: 0.007351
Minibatch error: 1.6%
Validation error: 0.9%
Step 6100 (epoch 7.10), 3.9 ms
Minibatch loss: 1.874, learning rate: 0.006983
Minibatch error: 0.0%
Validation error: 1.0%
Step 6200 (epoch 7.21), 4.0 ms
Minibatch loss: 1.846, learning rate: 0.006983
Minibatch error: 0.0%
Validation error: 0.9%
Step 6300 (epoch 7.33), 4.0 ms
Minibatch loss: 1.838, learning rate: 0.006983
Minibatch error: 0.0%
Validation error: 0.9%
Step 6400 (epoch 7.45), 4.0 ms
Minibatch loss: 1.847, learning rate: 0.006983
Minibatch error: 1.6%
Validation error: 0.9%
Step 6500 (epoch 7.56), 3.9 ms
Minibatch loss: 1.806, learning rate: 0.006983
Minibatch error: 0.0%
Validation error: 0.9%
Step 6600 (epoch 7.68), 3.9 ms
Minibatch loss: 1.855, learning rate: 0.006983
Minibatch error: 1.6%
Validation error: 1.0%
Step 6700 (epoch 7.80), 3.9 ms
Minibatch loss: 1.781, learning rate: 0.006983
Minibatch error: 0.0%
Validation error: 0.9%
Step 6800 (epoch 7.91), 3.9 ms
Minibatch loss: 1.774, learning rate: 0.006983
Minibatch error: 0.0%
Validation error: 1.0%
Step 6900 (epoch 8.03), 3.9 ms
Minibatch loss: 1.770, learning rate: 0.006634
Minibatch error: 1.6%
Validation error: 0.9%
Step 7000 (epoch 8.15), 4.0 ms
Minibatch loss: 1.764, learning rate: 0.006634
Minibatch error: 1.6%
Validation error: 1.0%
Step 7100 (epoch 8.26), 4.0 ms
Minibatch loss: 1.737, learning rate: 0.006634
Minibatch error: 0.0%
Validation error: 0.9%
Step 7200 (epoch 8.38), 4.0 ms
Minibatch loss: 1.732, learning rate: 0.006634
Minibatch error: 0.0%
Validation error: 1.0%
Step 7300 (epoch 8.49), 4.1 ms
Minibatch loss: 1.747, learning rate: 0.006634
Minibatch error: 3.1%
Validation error: 0.8%
Step 7400 (epoch 8.61), 4.0 ms
Minibatch loss: 1.700, learning rate: 0.006634
Minibatch error: 0.0%
Validation error: 0.7%
Step 7500 (epoch 8.73), 4.0 ms
Minibatch loss: 1.724, learning rate: 0.006634
Minibatch error: 1.6%
Validation error: 1.0%
Step 7600 (epoch 8.84), 4.0 ms
Minibatch loss: 1.800, learning rate: 0.006634
Minibatch error: 1.6%
Validation error: 0.8%
Step 7700 (epoch 8.96), 4.0 ms
Minibatch loss: 1.666, learning rate: 0.006634
Minibatch error: 0.0%
Validation error: 1.0%
Step 7800 (epoch 9.08), 4.1 ms
Minibatch loss: 1.658, learning rate: 0.006302
Minibatch error: 0.0%
Validation error: 0.8%
Step 7900 (epoch 9.19), 4.0 ms
Minibatch loss: 1.645, learning rate: 0.006302
Minibatch error: 0.0%
Validation error: 0.8%
Step 8000 (epoch 9.31), 4.0 ms
Minibatch loss: 1.645, learning rate: 0.006302
Minibatch error: 0.0%
Validation error: 0.9%
Step 8100 (epoch 9.43), 4.1 ms
Minibatch loss: 1.632, learning rate: 0.006302
Minibatch error: 0.0%
Validation error: 0.9%
Step 8200 (epoch 9.54), 4.0 ms
Minibatch loss: 1.619, learning rate: 0.006302
Minibatch error: 0.0%
Validation error: 0.8%
Step 8300 (epoch 9.66), 4.1 ms
Minibatch loss: 1.614, learning rate: 0.006302
Minibatch error: 0.0%
Validation error: 0.8%
Step 8400 (epoch 9.77), 4.0 ms
Minibatch loss: 1.596, learning rate: 0.006302
Minibatch error: 0.0%
Validation error: 0.8%
Step 8500 (epoch 9.89), 4.1 ms
Minibatch loss: 1.596, learning rate: 0.006302
Minibatch error: 0.0%
Validation error: 0.9%
Test error: 0.8%
```
