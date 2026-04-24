# COMPX234 Assignment 1: Printer Queue Synchronization

This repository contains the COMPX234 Assignment 1 solution for the producer-consumer printer queue problem.

## Repository note

This repository was recreated under the `zingpepiceapi` GitHub account after the previous GitHub account became unavailable. The assignment files were restored and checked before submission.

## Problem overview

The simulation contains:

- 50 machines that produce print requests.
- 5 printers that consume and print requests.
- A shared print queue with capacity 5.

The main challenge is preventing new machine requests from overwriting existing queued requests when the queue is already full.

## Synchronization approach

The implementation in `Assignment1Task.py` uses Python `threading` and semaphores:

- `empty_slots`: a counting semaphore initialized to 5. It prevents machines from inserting when the queue is full.
- `full_slots`: a counting semaphore initialized to 0. It prevents printers from printing when the queue is empty.
- `queue_mutex`: a binary semaphore initialized to 1. It ensures only one machine or printer accesses the queue at a time.

This follows the bounded-buffer producer-consumer pattern.

## How to run

Run the simulation from this directory:

```bash
python Main.py
```

The simulation runs for 30 seconds using the values defined in `Assignment1Task.py`.

## Expected behavior

During execution, machines send print requests and printers print requests from the queue. The queue size should not exceed 5, and the overwrite warning from `printList.py` should not appear during the synchronized implementation.

## Main files

- `Assignment1Task.py`: machine/printer thread logic and synchronization.
- `Main.py`: starts the simulation.
- `printDoc.py`: print request data object.
- `printList.py`: linked-list print queue provided by the starter code.
- `A1.md`: assignment specification.
