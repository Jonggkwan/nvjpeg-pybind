#!/usr/bin/env python3

import os
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from threading import Lock
from nvjpeg import NvJpeg

nj = NvJpeg()

image_dir = os.path.join(os.path.dirname(__file__), "test-image")
image_dir_out = os.path.join(os.path.dirname(__file__), "out")

# Ensure the output directory exists
os.makedirs(image_dir_out, exist_ok=True)

success_times = 0
lock = Lock()  # Thread-safe lock for updating success_times


def test_process_global(id):
    global nj, success_times
    for run_time in range(id + 1):
        try:
            with open(os.path.join(image_dir, "%d.jpg" % (id % 10,)), "rb") as fp:
                img = fp.read()

            nj_np = nj.decode(img)

            nj_jpg = nj.encode(nj_np)

            with open(os.path.join(image_dir_out, "nv-mp-test-%d.jpg" % (id,)), "wb") as fp:
                fp.write(nj_jpg)

            with lock:
                success_times += 1
        except Exception as e:
            print(f"Error in test_process_global (id={id}, run_time={run_time}): {e}")


def test_process_in_threads(id):
    global success_times
    nj_local = NvJpeg()
    for run_time in range(id + 1):
        try:
            with open(os.path.join(image_dir, "%d.jpg" % (id % 10,)), "rb") as fp:
                img = fp.read()

            nj_np = nj_local.decode(img)

            nj_jpg = nj_local.encode(nj_np)

            with open(os.path.join(image_dir_out, "nv-mp-test-%d.jpg" % (id,)), "wb") as fp:
                fp.write(nj_jpg)

            with lock:
                success_times += 1
        except Exception as e:
            print(f"Error in test_process_in_threads (id={id}, run_time={run_time}): {e}")
    del nj_local


TEST_TIMES = 50

executor = ThreadPoolExecutor(max_workers=10)
task_ids = range(TEST_TIMES)

print("submit global test")
success_times = 0
all_task = [executor.submit(test_process_global, id) for id in task_ids]
wait(all_task, return_when=ALL_COMPLETED)
if success_times == TEST_TIMES * (TEST_TIMES + 1) // 2:
    print("global test finished")
else:
    print(f"global test with error {TEST_TIMES * (TEST_TIMES + 1) // 2 - success_times}")

print("submit in threads test")
success_times = 0
all_task = [executor.submit(test_process_in_threads, id) for id in task_ids]
wait(all_task, return_when=ALL_COMPLETED)
if success_times == TEST_TIMES * (TEST_TIMES + 1) // 2:
    print("in threads test finished")
else:
    print(f"in threads test with error {TEST_TIMES * (TEST_TIMES + 1) // 2 - success_times}")
