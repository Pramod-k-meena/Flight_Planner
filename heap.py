class Heap:
    def __init__(self, comparison_function=None, init_array=None):
        """
        Time complexity: O(n), where n= the size of the input array.
        """
        self.comparison_function = comparison_function if comparison_function else lambda x, y: x < y
        self._heap = init_array if init_array is not None else []
        if self._heap:
            self._build_heap()

    def _build_heap(self):
        """building the heap if array given."""
        for i in range(len(self._heap) // 2 - 1, -1, -1):
            self._heapify_down(i)

    def insert(self, value):
        """Inserts in heap. O(log n)."""
        self._heap.append(value)
        self._heapify_up(len(self._heap) - 1)

    def extract(self):
        # Extracts the top. O(log n).
        if not self._heap:
            return None
        if len(self._heap) == 1:
            return self._heap.pop()
        top_element = self._heap[0]
        self._heap[0] = self._heap.pop()
        self._heapify_down(0)
        return top_element

    def top(self):
        # """returns top element without removing.  O(1)."""
        return self._heap[0] if self._heap else None

    def _heapify_up(self, index):
        """used when element is added in heap."""
        parent = (index - 1) // 2
        if index > 0 and self.comparison_function(self._heap[index], self._heap[parent]):
            self._heap[index], self._heap[parent] = self._heap[parent], self._heap[index]
            self._heapify_up(parent)

    def _heapify_down(self, index):
        """used when element removed"""
        least = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self._heap) and self.comparison_function(self._heap[left], self._heap[least]):
            least = left
        if right < len(self._heap) and self.comparison_function(self._heap[right], self._heap[least]):
            least = right

        if least != index:
            self._heap[index], self._heap[least] = self._heap[least], self._heap[index]
            self._heapify_down(least)

    def __len__(self): 
        return len(self._heap)
