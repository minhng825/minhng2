import random
import time

from multiprocessing import Process, Queue, current_process, freeze_support
from PIL import Image, ImageDraw


def analyze_picture(im):
    t1 = time.clock()
    image = Image.open(im)
    time.sleep(0.5*random.random())
    counter = 0
    for x in range(616,6446):
        for y in range(756,3712):
            r,g,b = image.getpixel((x,y))

            if r != 1 and g != 1 and b != 1:
                counter += 1

    t2 = time.clock()
    dt = t2 - t1
    print('\t It takes ', dt, ' seconds.\n ')
    return counter


def worker(input, output):
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)


def calculate(func, args):
    result = func(args)
    return '%s says that %s%s has %s corrupted pixels\n' % \
        (current_process().name, func.__name__, args, result)
def test():


    NUMBER_OF_PROCESSES = 4

    TASKS = [(analyze_picture, im[i]) for i in range(10)]

    print(TASKS)

    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    # Submit tasks
    for task in TASKS:
        task_queue.put(task)

    # Start worker processes
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()
        print(i)

    # Get and print results
    print('Unordered results:')
    for i in range(len(TASKS)):
        print('\t', done_queue.get())

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')
        print('process ', i, ' is stopped')


if __name__ == '__main__':
    im =[('MA_HA1_drawing_'+str(i)+'.png') for i in range(10)]
    freeze_support()
    test()
