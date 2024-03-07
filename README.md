# Own Backup Home Assignment

## Description

In order to measure and characterize the performance and resources consumption of my laptop I've selected the following metrics:
* CPU, Memory and Disk usage percentage - can be used to monitor resources utilization. A threshold can be set (for example to 80%) that will trigger an alert.
* Disk I/O count and speed - can be used to monitor the load on the disk. If the I/O is slow, it will slow down the whole system. The threshold can be set based on a baseline that can be defined from over time data. 
* Network speed - If network usage is slow, it can slow down the whole system. Here as well the threshold should be defined from the overtime baseline.
* System load - I took the counter of average system load of the past minute (OOTB counter. Can be changed to past 5 or 15 minutes). Because it depends on the number of cores, I've divided it by the number of cores. This number suppose to be lower than 1 (I've represented it in percents for convenience). A threshold can be set to 80% or 90%.
* Battery Left - Used to trigger when the laptop should be plugged in.

## Installation
```bash
pip3 install -r requirements.txt
```

## Usage
* Change the password (OPENSEARCH_INITIAL_ADMIN_PASSWORD) in docker-compose.yml and in own_home_assignment.py
* Run:
```bash 
docker-compose up
````
* Run:
```bash
python3 own_home_assignment.py
```
* Go to http://localhost:5601/ and use user name admin with the above password to login
