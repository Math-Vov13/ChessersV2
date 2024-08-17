from transitions import Machine, MachineError  # Final State Machine Library

class Chrono:
    pass # est-ce vraiment utile ? (à voir !)

class Timer:
    # States (PROTECTED)
    _RUNNING = "running"
    _PAUSED = "paused"
    _STOPPED = "stopped"

    def __init__(self) -> None:
        # Private properties
        self.__Time = 0
        self.__LastTick = 0

        transitions = [
            {"trigger": "run", "source": self._STOPPED, "dest": self._RUNNING, "after": "_on_run"},
            {"trigger": "resume", "source": self._PAUSED, "dest": self._RUNNING, "after": "_on_run"},
            {"trigger": "pause", "source": self._RUNNING, "dest": self._PAUSED},
            {"trigger": "stop", "source": self._RUNNING, "dest": self._STOPPED, "after": "_on_stop"},
            {"trigger": "stop", "source": self._PAUSED, "dest": self._STOPPED, "after": "_on_stop"},
        ]

        self.machine = Machine(
            model=self,
            states=[self._RUNNING, self._PAUSED, self._STOPPED],
            transitions=transitions,
            initial=self._STOPPED,
        )
    
    def _on_run(self, tick: int = 0):
        self.__LastTick = tick

    def _on_stop(self):
        self.__Time = 0
        self.__LastTick = 0

    def getTime(self):
        return self.__Time

    def updateTimer(self, tick: int):
        if self.state != self._RUNNING: return
        elapsed = (tick - self.__LastTick) / 1000 # elapsed time
        self.__LastTick = tick       # update Tick
        self.__Time += elapsed


if __name__ == "__main__":
    testTimer = Timer() # Create Timer Object

    try: # Test States
        print("Init State :",testTimer.state)

        testTimer.run() # -> running
        print("State :",testTimer.state)

        testTimer.pause() # -> paused
        print("State :",testTimer.state)

        testTimer.resume() # -> running
        print("State :",testTimer.state)

        testTimer.stop() # -> stopped
        print("State :",testTimer.state)

        testTimer.stop() #  ERROR !

    except MachineError as e: # track error
        print(f"Error with FSM : {e}")