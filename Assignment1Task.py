import threading
import time
import random

from printDoc import printDoc
from printList import printList


class Assignment1:
    # Simulation Initialisation parameters
    NUM_MACHINES = 50        # Number of machines that issue print requests
    NUM_PRINTERS = 5         # Number of printers in the system
    SIMULATION_TIME = 30     # Total simulation time in seconds
    MAX_PRINTER_SLEEP = 3    # Maximum sleep time for printers
    MAX_MACHINE_SLEEP = 5    # Maximum sleep time for machines

    # Initialise simulation variables
    def __init__(self):
        self.sim_active = True
        self.print_list = printList()  # Create an empty list of print requests
        self.mThreads = []             # list for machine threads
        self.pThreads = []             # list for printer threads

        self.empty_slots = threading.Semaphore(self.NUM_PRINTERS)
        self.full_slots = threading.Semaphore(0)
        self.queue_mutex = threading.Semaphore(1)

    def startSimulation(self):
        # Create Machine and Printer threads
        for machine_id in range(1, self.NUM_MACHINES + 1):
            self.mThreads.append(self.machineThread(machine_id, self))

        for printer_id in range(1, self.NUM_PRINTERS + 1):
            self.pThreads.append(self.printerThread(printer_id, self))

        # Start all the threads
        for thread in self.mThreads:
            thread.start()

        for thread in self.pThreads:
            thread.start()

        # Let the simulation run for some time
        time.sleep(self.SIMULATION_TIME)

        # Finish simulation
        self.sim_active = False

        # Wait until all threads finish by joining them
        for thread in self.mThreads:
            thread.join()

        for thread in self.pThreads:
            thread.join()

        print("Simulation finished.")

    # Printer class
    class printerThread(threading.Thread):
        def __init__(self, printerID, outer):
            threading.Thread.__init__(self)
            self.printerID = printerID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Simulate printer taking some time to print the document
                self.printerSleep()
                # Grab the request at the head of the queue and print it
                self.printDox(self.printerID)

        def printerSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_PRINTER_SLEEP)
            time.sleep(sleepSeconds)

        def printDox(self, printerID):
            if not self.outer.full_slots.acquire(timeout=0.1):
                return

            print(f"Printer ID: {printerID} : now available")
            self.outer.queue_mutex.acquire()
            self.outer.print_list.queuePrint(printerID)
            self.outer.queue_mutex.release()
            self.outer.empty_slots.release()

    # Machine class
    class machineThread(threading.Thread):
        def __init__(self, machineID, outer):
            threading.Thread.__init__(self)
            self.machineID = machineID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Machine sleeps for a random amount of time
                self.machineSleep()
                if not self.outer.sim_active:
                    break
                # Machine wakes up and sends a print request
                if self.isRequestSafe(self.machineID):
                    self.printRequest(self.machineID)
                    self.postRequest(self.machineID)

        def machineSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleepSeconds)

        def isRequestSafe(self, id):
            print(f"Machine {id} Checking availability")
            if not self.outer.empty_slots.acquire(timeout=0.1):
                return False

            self.outer.queue_mutex.acquire()
            print(f"Machine {id} will proceed")
            return True

        def printRequest(self, id):
            print(f"Machine {id} Sent a print request")
            # Build a print document
            doc = printDoc(f"My name is machine {id}", id)
            # Insert it in the print queue
            self.outer.print_list.queueInsert(doc)

        def postRequest(self, id):
            print(f"Machine {id} Releasing binary semaphore")
            self.outer.queue_mutex.release()
            self.outer.full_slots.release()
