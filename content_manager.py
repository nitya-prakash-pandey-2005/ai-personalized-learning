import random
import json
import os


class ContentManager:
    """
    Manages learning content, topics, and quiz generation.
    Supports difficulty-aware adaptive quizzes.
    """

    def __init__(self):
        self.content_file = "content_data.json"

        # -------------------------------
        # TOPICS METADATA
        # -------------------------------
        self.topics = {
            "Mathematics": {
                "title": "Mathematics Fundamentals",
                "description": "Learn core mathematical concepts including algebra, geometry, and calculus.",
                "subtopics": ["Fractions", "Algebra", "Geometry", "Calculus"],
            },
            "Science": {
                "title": "Science Essentials",
                "description": "Explore physics, chemistry, biology, and environmental science.",
                "subtopics": ["Physics", "Chemistry", "Biology", "Climate Change"],
            },
            "Programming": {
                "title": "Programming Basics",
                "description": "Master programming fundamentals and problem-solving with code.",
                "subtopics": ["Python Basics", "Data Structures", "Algorithms", "Web Development"],
            },
            "Languages": {
                "title": "Language Learning",
                "description": "Improve your language skills with interactive lessons.",
                "subtopics": ["Vocabulary", "Grammar", "Reading Comprehension", "Writing"],
            },
        }

        # -------------------------------
        # QUESTION BANK
        # -------------------------------
        self.questions = self._initialize_questions()
        self._load_content_from_disk()

    # =====================================================
    # INTERNAL HELPERS
    # =====================================================

    def _initialize_questions(self):
        """Initial hardcoded question bank."""
        return {
            "Mathematics": {
                "Fractions": [
                    {
                        "question": "What is 1/2 + 1/4?",
                        "options": ["1/4", "2/4", "3/4", "1"],
                        "correct_answer": "3/4",
                        "difficulty": "Easy",
                        "explanation": "1/2 = 2/4 → 2/4 + 1/4 = 3/4",
                    },
                    {
                        "question": "What is 2/3 × 3/4?",
                        "options": ["5/7", "6/12", "1/2", "2/3"],
                        "correct_answer": "1/2",
                        "difficulty": "Medium",
                        "explanation": "Multiply numerators and denominators → 6/12 = 1/2",
                    },
                ],
                "Algebra": [
                    {
                        "question": "Solve for x: 2x + 5 = 13",
                        "options": ["x = 3", "x = 4", "x = 5", "x = 6"],
                        "correct_answer": "x = 4",
                        "difficulty": "Easy",
                        "explanation": "2x = 8 → x = 4",
                    }
                ],
            },
            "Science": {
                "Climate Change": [
                    {
                        "question": "What is the primary cause of global warming?",
                        "options": [
                            "Increased solar radiation",
                            "Greenhouse gas emissions",
                            "Ocean currents",
                            "Volcanic activity",
                        ],
                        "correct_answer": "Greenhouse gas emissions",
                        "difficulty": "Easy",
                        "explanation": "Greenhouse gases trap heat in the atmosphere.",
                    },
                    {
                        "question": "Which is NOT renewable?",
                        "options": ["Solar", "Wind", "Coal", "Hydroelectric"],
                        "correct_answer": "Coal",
                        "difficulty": "Easy",
                        "explanation": "Coal is a fossil fuel.",
                    },
                ]
            },
            "Programming": {
                "Python Basics": [
                    {
                        "question": "Output of print(2 + 3 * 4)?",
                        "options": ["20", "14", "24", "Error"],
                        "correct_answer": "14",
                        "difficulty": "Easy",
                        "explanation": "Multiplication first → 2 + 12 = 14",
                    }
                ]
            },
            "Languages": {
                "Reading Comprehension": [
                    {
                        "question": "Main idea of a passage on exercise benefits?",
                        "options": [
                            "Exercise is difficult",
                            "Exercise has health benefits",
                            "Exercise is expensive",
                            "Exercise is time-consuming",
                        ],
                        "correct_answer": "Exercise has health benefits",
                        "difficulty": "Easy",
                        "explanation": "The passage focuses on benefits.",
                    }
                ]
            },
        }

    def _load_content_from_disk(self):
        """Load custom content if file exists."""
        if os.path.exists(self.content_file):
            try:
                with open(self.content_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.questions.update(data.get("questions", {}))
            except Exception:
                pass

    def save_content(self):
        """Persist content to disk."""
        with open(self.content_file, "w", encoding="utf-8") as f:
            json.dump({"questions": self.questions}, f, indent=2)

    # =====================================================
    # PUBLIC API
    # =====================================================

    def get_available_topics(self):
        return list(self.topics.keys())

    def get_topic_content(self, topic, student_id=None):
        if topic not in self.topics:
            return {
                "title": "Topic Not Found",
                "description": "This topic does not exist.",
                "difficulty": "Medium",
            }

        return {
            "title": self.topics[topic]["title"],
            "description": self.topics[topic]["description"],
            "subtopics": self.topics[topic]["subtopics"],
            "difficulty": "Medium",
        }

    # =====================================================
    # 🔥 FIXED METHOD (IMPORTANT)
    # =====================================================

    def generate_quiz(
        self,
        topic,
        student_id=None,
        difficulty="Medium",
        num_questions=5,
    ):
        """
        Generate quiz questions filtered by difficulty.
        This FIXES your crash permanently.
        """

        if topic not in self.questions:
            return []

        # Collect questions by difficulty
        filtered = []
        for _, q_list in self.questions[topic].items():
            filtered.extend(
                [q for q in q_list if q.get("difficulty") == difficulty]
            )

        # Fallback: if not enough difficulty-specific questions
        if len(filtered) < num_questions:
            filtered = []
            for _, q_list in self.questions[topic].items():
                filtered.extend(q_list)

        if not filtered:
            return []

        return random.sample(
            filtered,
            min(num_questions, len(filtered)),
        )

    def get_questions_by_difficulty(self, topic, difficulty):
        if topic not in self.questions:
            return []

        result = []
        for _, q_list in self.questions[topic].items():
            result.extend([q for q in q_list if q.get("difficulty") == difficulty])

        return result
