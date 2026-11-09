"""Question bank and answer-checking helpers."""

QUESTIONS = [
    {
        "question": "Which structure does BFS use to explore level by level?",
        "options": ["Stack", "Queue", "Heap"],
        "answer": 1,
        "explanation": "A FIFO queue processes the oldest discovered node first.",
    },
    {
        "question": "What does A* add to the cost already travelled?",
        "options": ["A heuristic estimate", "A random value", "The number of walls"],
        "answer": 0,
        "explanation": "A* prioritizes g(n) + h(n): cost so far plus estimated cost to goal.",
    },
    {
        "question": "In a four-direction grid, what is Manhattan distance?",
        "options": ["Straight-line distance", "Row difference + column difference", "Number of visited cells"],
        "answer": 1,
        "explanation": "Manhattan distance sums the absolute row and column differences.",
    },
    {
        "question": "Which Python type is commonly used for a unique visited set?",
        "options": ["set", "str", "float"],
        "answer": 0,
        "explanation": "A set stores unique nodes and provides fast membership checks.",
    },
    {
        "question": "Does DFS always find the shortest path in an unweighted maze?",
        "options": ["Yes", "No", "Only on even-sized mazes"],
        "answer": 1,
        "explanation": "DFS finds a path, but its depth-first order does not guarantee minimum length.",
    },
    {
        "question": "What is the usual time complexity of checking membership in a Python set?",
        "options": ["O(1) average", "O(n²)", "O(log n) always"],
        "answer": 0,
        "explanation": "Hash-set membership is O(1) on average.",
    },
    {
        "question": "Why must the Hunter recompute its path?",
        "options": ["The maze changes each frame", "The Explorer changes position", "A* requires a new random seed"],
        "answer": 1,
        "explanation": "The target moves, so the Hunter should plan toward the Explorer's latest cell.",
    },
    {
        "question": "Which value should A* use as the priority for a node?",
        "options": ["g(n) + h(n)", "g(n) - h(n)", "h(n) only"],
        "answer": 0,
        "explanation": "The evaluation function combines known cost and estimated remaining cost.",
    },
    {
        "question": "Which data structure is best suited to A*'s lowest-priority-first frontier?",
        "options": ["Priority queue", "FIFO queue", "Linked list only"],
        "answer": 0,
        "explanation": "A priority queue efficiently removes the node with the smallest estimated total cost.",
    },
]


def question_for(level_index: int, question_index: int) -> dict:
    return QUESTIONS[(level_index * 3 + question_index) % len(QUESTIONS)]


def is_correct(question: dict, answer_index: int) -> bool:
    return answer_index == question["answer"]
