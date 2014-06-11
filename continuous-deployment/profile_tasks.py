import time

# Based on MIT-licensed ansible-profile https://github.com/jlafon/ansible-profile


class CallbackModule(object):
    """A plugin for timing tasks"""
    def __init__(self):
        self.stats = {}
        self.current = None

    def playbook_on_task_start(self, name, is_conditional):
        """Logs the start of each task"""
        if self.current is not None:
            self.stats[self.current] = time.time() - self.stats[self.current]

        self.current = name
        self.stats[self.current] = time.time()

    def playbook_on_stats(self, stats):
        """Prints the timings"""

        if self.current is not None:
            self.stats[self.current] = time.time() - self.stats[self.current]

        results = sorted(self.stats.items(), key=lambda value: value[1], reverse=True,)
        results = results[:50]

        with open("../../time_log_" + str(int(time.time())) + ".log", "w") as logfile:
            for name, elapsed in results:
                logfile.write("{0:.02f} s, {1}\n".format(elapsed, name))
