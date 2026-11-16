"""A max-heap: the biggest value is always at the top.

Adapted from the MaxHeap in the course zyBook (section "Python: Heaps"),
the same structure used in Homework 9. Added peek() for the draft board.

The heap is a complete binary tree stored in a list:
  children of index i are at 2*i + 1 and 2*i + 2
  parent of index i is at (i - 1) // 2
"""


class MaxHeap:
    def __init__(self):
        self.heap_array = []

    # Support for len(heap)
    def __len__(self):
        return len(self.heap_array)

    # Look at the biggest value without removing it: O(1)
    def peek(self):
        return self.heap_array[0]

    # Add a value: O(log N)
    def insert(self, value):
        # Put it at the end, then move it up until its parent is bigger.
        self.heap_array.append(value)
        self.percolate_up(len(self.heap_array) - 1)

    # Remove and return the biggest value: O(log N)
    def remove(self):
        max_value = self.heap_array[0]

        # Move the last value to the top, then move it down into place.
        last_value = self.heap_array.pop()
        if len(self.heap_array) > 0:
            self.heap_array[0] = last_value
            self.percolate_down(0)
        return max_value

    def percolate_up(self, node_index):
        while node_index > 0:
            parent_index = (node_index - 1) // 2

            # Parent is already at least as big: the heap is correct.
            if self.heap_array[node_index] <= self.heap_array[parent_index]:
                return

            self.swap(node_index, parent_index)
            node_index = parent_index

    def percolate_down(self, node_index):
        while True:
            left = 2 * node_index + 1
            right = 2 * node_index + 2
            biggest = node_index

            # Find the biggest of the node and its (up to two) children.
            if (left < len(self.heap_array) and
                    self.heap_array[left] > self.heap_array[biggest]):
                biggest = left
            if (right < len(self.heap_array) and
                    self.heap_array[right] > self.heap_array[biggest]):
                biggest = right

            # The node is bigger than both children: the heap is correct.
            if biggest == node_index:
                return

            self.swap(node_index, biggest)
            node_index = biggest

    def swap(self, i, j):
        self.heap_array[i], self.heap_array[j] = (self.heap_array[j],
                                                  self.heap_array[i])
