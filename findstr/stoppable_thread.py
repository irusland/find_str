import threading


class StoppableThread(threading.Thread):
    def __init__(self):
        super(StoppableThread, self).__init__()
        self.daemon = True
        self.__monitor = threading.Event()
        self.__monitor.set()
        self.__has_shutdown = False

    def run(self):
        self.startup()
        while self.is_running():
            self.mainloop()
        self.cleanup()
        self.__has_shutdown = True

    def stop(self):
        self.__monitor.clear()

    def is_running(self):
        return self.__monitor.isSet()

    def is_shutdown(self):
        return self.__has_shutdown

    def mainloop(self):
        pass

    def startup(self):
        pass

    def cleanup(self):
        pass
