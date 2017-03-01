# Torch

# setup 2015

```Bash
curl -s https://raw.githubusercontent.com/torch/ezinstall/master/install-deps | bash
git clone https://github.com/torch/distro.git ~/torch --recursive
cd ~/torch; ./install.sh
```

# CPU versus GPU for deep learning

Roelof Pieters set some benchmarks in 2015-07 for deep dreaming video processing using CPU and GPU hardware. The CPU hardware was Amazon EC2 g2.2xlarge Intel Xeon E5-2670 (Sandy Bridge) 8 cores 2.6 GHz/3.3 GHz turbo and the GPU hardware was Amazon EC2 g2.2xlarge 2 x 4 Gb GPU.

|**input image resolution (pixels)**|**CPU processing time for 1 image**|**GPU processing time for 1 image**|**CPU processing time for 2 minute video**|**GPU processing time for 2 minute video**|
|-----------------------------------|-----------------------------------|-----------------------------------|------------------------------------------|------------------------------------------|
|540 x 360                          |45 s                               |1 s                                |1 d 21 h                                  |60 minutes                                |
|1024 x 768                         |144 s                              |3 s                                |6 d                                       |3 h                                       |

So, the GPU hardware was ~45 -- ~48 times faster than the CPU hardware.
