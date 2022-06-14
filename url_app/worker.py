from queue import Queue
from threading import Thread
import os
from .views import UrlViewSet


class CreateWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            request = self.queue.get()
            try:
                UrlViewSet.create(self, request)
            finally:
                self.queue.task_done()


def main():
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    download_dir = UrlViewSet.create()
    # Create a queue to communicate with the worker threads
    queue = Queue()
    # Create 2 worker threads
    for x in range(2):
        worker = CreateWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for dd in download_dir:
        queue.put(download_dir)
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()

if __name__ == '__main__':
    main()