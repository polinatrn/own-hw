import time
import os
import psutil
from datetime import datetime
from opensearchpy import OpenSearch

host = 'localhost'
port = 9200
auth = ('admin', '<OPENSEARCH_INITIAL_ADMIN_PASSWORD>')

client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_compress=True,  # enables gzip compression for request bodies
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    http_auth=auth,
    ssl_show_warn=False
)

index_name = 'my-dsl-index'
index_body = {
    'settings': {
        'index': {
            'number_of_shards': 4
        }
    }
}


def net_usage_per_second():
    global net_usage
    net_io_start = psutil.net_io_counters()
    time.sleep(1)
    net_io_end = psutil.net_io_counters()
    return {
        'bytes_sent_per_second': net_io_end.bytes_sent - net_io_start.bytes_sent,
        'bytes_received_per_second': net_io_end.bytes_recv - net_io_start.bytes_recv
    }


def read_write_per_second():
    disk_io_start = psutil.disk_io_counters()
    time.sleep(1)
    disk_io_end = psutil.disk_io_counters()

    disk_read_speed = disk_io_end.read_bytes - disk_io_start.read_bytes
    disk_write_speed = disk_io_end.write_bytes - disk_io_start.write_bytes
    return {
        'disk_read_speed': disk_read_speed,
        'disk_write_speed': disk_write_speed
    }


def battery_percent():
    battery = psutil.sensors_battery()
    if battery is not None:
        return battery.percent
    return None


def system_load_percent():
    num_cpu_cores = psutil.cpu_count()
    system_load_min = os.getloadavg()[0]
    # represents the number of active processes - amount of computational work that a computer system performs. it depends on the number of CPU cores the system has.
    return (system_load_min * 100) / num_cpu_cores


def disk_io_count():
    disk_io = psutil.disk_io_counters()
    return {'read_count': disk_io.read_count, 'write_count': disk_io.write_count}


for i in range(10000):
    data = {
        'timestamp': datetime.now(),
        'cpu_usage_percent': psutil.cpu_percent(),
        'memory_usage_percent': psutil.virtual_memory().percent,
        'disk_usage_percent': psutil.disk_usage('/').percent,
        'disk_io_count': disk_io_count(),
        'disk_io_speed': read_write_per_second(),
        'net_usage_per_sec': net_usage_per_second(),
        'system_load_percent': system_load_percent(),
        'battery_percent': battery_percent(),
    }

    client.index(index='system_performance_and_utilization', body=data)

    time.sleep(10)
    print(data)
