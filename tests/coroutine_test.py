from pykka.actor import ThreadingActor
from pykka.registry import ActorRegistry
import time
import unittest
import threading

class CoroutineActor(ThreadingActor):
    def __init__(self):
        ThreadingActor.__init__(self)
        self.infinite_loop_count = 0
        self.other_called = False
    def loop_infinitely(self, i):
        self.infinite_loop_count = i
        time.sleep(0.001)
        if i < 100:
            self.as_message.loop_infinitely(i+1)
    def other_method(self):
        self.other_called = True
class CoroutineActorTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        ActorRegistry.stop_all()
    def test_runs_parallel(self):
        self.actor = CoroutineActor.start().proxy()
        first = self.actor.infinite_loop_count.get()
        self.actor.loop_infinitely(0).get()
        second = self.actor.infinite_loop_count.get()
        self.actor.other_method().get()
        called = self.actor.other_called.get()
        third = self.actor.infinite_loop_count.get()
        self.assertTrue(called)
        self.assertLess(first, second)
        self.assertLess(second, third)
        ActorRegistry.stop_all()
if __name__ == '__main__':
    import logging
    logging.basicConfig()
    logging.getLogger('pykka').setLevel(logging.DEBUG)
    unittest.main()
