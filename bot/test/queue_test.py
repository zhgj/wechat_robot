from queue import Queue


msg_picture_queue = Queue()

if __name__ == '__main__':
    msg_picture_queue.put('ssss')
    msg_picture_queue.put('ssss222')
    item = msg_picture_queue.get()
    for value in msg_picture_queue.values():
        print(value)