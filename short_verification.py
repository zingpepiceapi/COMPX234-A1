"""Short verification runner for COMPX234 Assignment 1.

This script runs the simulation with reduced timing values so the producer-consumer
behavior can be checked quickly without waiting for the full 30 second run.
"""

from Assignment1Task import Assignment1


def main():
    Assignment1.NUM_MACHINES = 10
    Assignment1.NUM_PRINTERS = 5
    Assignment1.SIMULATION_TIME = 4
    Assignment1.MAX_MACHINE_SLEEP = 1
    Assignment1.MAX_PRINTER_SLEEP = 1

    simulation = Assignment1()
    simulation.startSimulation()


if __name__ == "__main__":
    main()
