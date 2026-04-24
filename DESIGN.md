# Synchronization Design

## Producer-consumer mapping

The assignment is implemented as a bounded-buffer producer-consumer problem:

- Machines are producers because they create print requests.
- Printers are consumers because they remove and print queued requests.
- The print queue is the shared bounded buffer.

The assignment queue capacity is 5, matching the number of printers.

## Synchronization primitives

`Assignment1Task.py` uses three semaphores.

### `empty_slots`

`empty_slots` is initialized to `NUM_PRINTERS`, which is 5. A machine must acquire this semaphore before inserting into the queue. If the queue already has 5 requests, no empty slots remain and the machine must wait/retry instead of inserting.

This prevents the overwrite behavior inside `printList.queueInsert` from being reached during normal synchronized execution.

### `full_slots`

`full_slots` is initialized to 0. A printer must acquire this semaphore before printing. This ensures a printer only attempts to print when at least one request exists in the queue.

After a machine inserts a request, it releases `full_slots` to signal that work is available.

### `queue_mutex`

`queue_mutex` is initialized to 1 and protects the queue critical section.

Both operations below are protected:

- Machine insertion through `queueInsert`.
- Printer removal through `queuePrint`.

This ensures that no two machines/printers access the linked-list queue at the same time.

## Machine sequence

1. Sleep for a random time.
2. Acquire an empty queue slot.
3. Acquire queue mutual exclusion.
4. Create a `printDoc` request.
5. Insert the request into the queue.
6. Release queue mutual exclusion.
7. Signal one full slot for printers.

## Printer sequence

1. Sleep for a random time.
2. Acquire a full queue slot.
3. Acquire queue mutual exclusion.
4. Print and remove the request at the queue head.
5. Release queue mutual exclusion.
6. Signal one empty slot for machines.

## Requirement coverage

- Queue overwrite prevention: provided by `empty_slots`.
- Exclusive queue access: provided by `queue_mutex`.
- Empty queue protection for printers: provided by `full_slots`.
- Machine/printer sleeping behavior: implemented in `machineSleep` and `printerSleep`.
