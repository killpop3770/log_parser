from __future__ import annotations
 
import re
from datetime import datetime
 
 
class Event:
 
    def __init__(self, dt: datetime, rt: str):
        self.dt, self.rt = dt, rt
    
    @classmethod
    def from_string(self, string: str, pattern: str) -> Event:
        match = re.fullmatch(pattern, string)
        self.dt = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
        self.rt = match.group(2)
        return Event(self.dt, self.rt)
 
    def __repr__(self)->str:
        return self.__str__()
 
    def __str__(self) -> str:
        return f"Event(datetime={self.dt}, result={self.rt})"
 
 
class LogParser:
 
 
    def __init__(self, fileName: str):
        self.fileName = fileName
        self.events = []
        self.end_mas = []
        self.count = 0
 
    def read(self, pattern: str):
        with open(self.fileName, "rt") as file:
            lines = file.read().split("\n")
        self.events = [Event.from_string(line, pattern) for line in lines if line]
 
 
    @property
    def group_in_minutes(self) -> tuple:
        group_events = [[self.events[0]], ]
        for event in self.events[1:]:
            if (event.dt - group_events[-1][0].dt).seconds < 60:
                group_events[-1].append(event)
            else:
                group_events.append([event])

        for i in range(len(group_events)):
            for j in range(len(group_events[i])):
                if group_events[i][j].rt == "NOK":
                    self.count+=1
            self.end_mas.append(str(group_events[i][j].dt)+ " "+ str(self.count))
            self.count = 0

        return group_events
 
 
lg = LogParser("test.log")
lg.read(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (\w{2,3})")
lg.events
lg.group_in_minutes
print(lg.end_mas)