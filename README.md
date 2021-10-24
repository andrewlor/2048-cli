# [2048](https://en.wikipedia.org/wiki/2048_(video_game)) CLI

## Usage
### Play
```
./2048
```

![](sample.png)

## Install for development
Requires at least python3.4, numpy, readchar
```
pip3 install numpy readchar
python3 2048.py
```

### Simulation
You can also write/run simulations. Take a look in the `/simulation` directory to see how it works. Then run the `run_simulation` script from the repo root.

```
Usage: [ --stat ] algorithm [ times ]
--stat: display statistical summary of scores, otherwise full dataset is printed
algorithm: name of the algorithm you want to run. Must be a .py file in /simulation
times: the number of simulations to run
```

#### Example
```
./run_simulation --stat down 100
Mean: 7.68
./run_simulation --stat random 100
Mean: 861.4
./run_simulation --stat axis 100
Mean: 1351.96
```