import random
import streamlit as st

class QuestionGenerator:
    def __init__(self):
        self.bank = {

            # =========================
            # 📐 MATH
            # =========================
            "Mathematics": {
                "Easy": [
                    ("What is 2 + 2?", ["3", "4", "5", "6"], "4"),
                    ("What is 5 × 1?", ["3", "5", "6", "7"], "5"),
                    ("What is 10 − 6?", ["2", "3", "4", "5"], "4"),
                    ("What is 8 + 1?", ["7", "8", "9", "10"], "9"),
                    ("What is 6 ÷ 2?", ["2", "3", "4", "6"], "3"),
                ],
                "Medium": [
                    ("What is 12 ÷ 3?", ["2", "3", "4", "6"], "4"),
                    ("What is 15 − 7?", ["6", "7", "8", "9"], "8"),
                    ("What is 9 × 4?", ["32", "36", "40", "42"], "36"),
                    ("What is 25 ÷ 5?", ["3", "4", "5", "6"], "5"),
                    ("What is 7²?", ["14", "49", "21", "28"], "49"),
                ],
                "Hard": [
                    ("Solve: 3² + 4²", ["25", "12", "9", "16"], "25"),
                    ("What is √144?", ["10", "11", "12", "13"], "12"),
                    ("Solve: (8 × 5) − 12", ["28", "32", "40", "52"], "28"),
                    ("What is 2³ × 3?", ["12", "18", "24", "16"], "24"),
                    ("What is 45 ÷ 9?", ["3", "4", "5", "6"], "5"),
                ],
            },

            # =========================
            # 🔬 SCIENCE
            # =========================
            "Science": {
                "Easy": [
                    ("Water boils at?", ["50°C", "100°C", "0°C", "150°C"], "100°C"),
                    ("Which planet is known as Red Planet?", ["Earth", "Mars", "Jupiter", "Venus"], "Mars"),
                    ("Humans breathe in?", ["Oxygen", "Carbon", "Nitrogen", "Hydrogen"], "Oxygen"),
                    ("Sun is a?", ["Planet", "Star", "Galaxy", "Asteroid"], "Star"),
                    ("Plants make food by?", ["Respiration", "Photosynthesis", "Digestion", "Fermentation"], "Photosynthesis"),
                ],
                "Medium": [
                    ("Which gas do plants absorb?", ["Oxygen", "Nitrogen", "CO₂", "Hydrogen"], "CO₂"),
                    ("What organ pumps blood?", ["Brain", "Lungs", "Heart", "Kidney"], "Heart"),
                    ("Which vitamin comes from sunlight?", ["A", "B", "C", "D"], "D"),
                    ("What force pulls objects to Earth?", ["Magnetism", "Gravity", "Friction", "Pressure"], "Gravity"),
                    ("pH of pure water is?", ["5", "6", "7", "8"], "7"),
                ],
                "Hard": [
                    ("Chemical symbol of Sodium?", ["So", "Na", "Sn", "S"], "Na"),
                    ("Unit of electric current?", ["Volt", "Ohm", "Ampere", "Watt"], "Ampere"),
                    ("Which blood cells fight infection?", ["RBC", "WBC", "Platelets", "Plasma"], "WBC"),
                    ("Speed of light is approx?", ["3×10⁸ m/s", "3×10⁶ m/s", "3×10⁴ m/s", "300 m/s"], "3×10⁸ m/s"),
                    ("Main gas in Earth’s atmosphere?", ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "Nitrogen"),
                ],
            },

            # =========================
            # 💻 PROGRAMMING
            # =========================
            "Programming": {
                "Easy": [
                    ("Which keyword defines a function in Python?", ["func", "define", "def", "lambda"], "def"),
                    ("Which symbol is used for comments in Python?", ["//", "#", "/*", "--"], "#"),
                    ("What data type is 10?", ["String", "Float", "Integer", "Boolean"], "Integer"),
                    ("Which function prints output?", ["print()", "show()", "echo()", "output()"], "print()"),
                    ("Which operator adds values?", ["*", "-", "+", "/"], "+"),
                ],
                "Medium": [
                    ("What does len([1,2,3]) return?", ["2", "3", "Error", "None"], "3"),
                    ("Which loop repeats a block?", ["if", "for", "break", "return"], "for"),
                    ("What is index of first element?", ["0", "1", "-1", "None"], "0"),
                    ("Which keyword stops a loop?", ["stop", "exit", "break", "end"], "break"),
                    ("Which structure stores key-value pairs?", ["List", "Tuple", "Set", "Dictionary"], "Dictionary"),
                ],
                "Hard": [
                    ("Output of bool([])?", ["True", "False", "None", "Error"], "False"),
                    ("What is returned by type(5)?", ["int", "Integer", "<class 'int'>", "number"], "<class 'int'>"),
                    ("Which is immutable?", ["List", "Set", "Dictionary", "Tuple"], "Tuple"),
                    ("What does pass do?", ["Stops program", "Skips block", "Throws error", "Ends loop"], "Skips block"),
                    ("Result of 5 // 2?", ["2.5", "2", "3", "Error"], "2"),
                ],
            },

            # =========================
            # 🗣️ LANGUAGES
            # =========================
            "Languages": {
                "Easy": [
                    ("Plural of 'child'?", ["childs", "children", "childes", "child"], "children"),
                    ("Opposite of 'hot'?", ["Cold", "Warm", "Cool", "Heat"], "Cold"),
                    ("Synonym of 'big'?", ["Large", "Small", "Tiny", "Little"], "Large"),
                    ("Correct article: ___ apple", ["a", "an", "the", "no article"], "an"),
                    ("Past tense of 'go'?", ["goed", "went", "gone", "goes"], "went"),
                ],
                "Medium": [
                    ("Synonym of 'quick'?", ["slow", "fast", "lazy", "late"], "fast"),
                    ("Antonym of 'happy'?", ["joyful", "sad", "excited", "glad"], "sad"),
                    ("Which is a noun?", ["run", "beautiful", "book", "quickly"], "book"),
                    ("Correct spelling?", ["recieve", "receive", "receeve", "receve"], "receive"),
                    ("Plural of 'mouse'?", ["mouses", "mouse", "mice", "meese"], "mice"),
                ],
                "Hard": [
                    ("Correct spelling?", ["accomodate", "accommodate", "acommodate", "acomodate"], "accommodate"),
                    ("Which is an adverb?", ["quick", "quickly", "quickness", "quicken"], "quickly"),
                    ("Choose correct sentence", [
                        "He don’t like it",
                        "He doesn’t like it",
                        "He didn’t likes it",
                        "He not like it"
                    ], "He doesn’t like it"),
                    ("Meaning of 'ubiquitous'?", [
                        "Rare",
                        "Everywhere",
                        "Dangerous",
                        "Unknown"
                    ], "Everywhere"),
                    ("Which is a conjunction?", ["and", "very", "quick", "blue"], "and"),
                ],
            },
        }

    def generate_question(self, topic, difficulty):
        # 🔐 SAFETY FALLBACKS
        topic_data = self.bank.get(topic, {})
        pool = topic_data.get(difficulty, [])

        # 🚑 IF EMPTY → FALLBACK TO EASY
        if not pool:
            pool = topic_data.get("Easy", [])

        # 🚑 STILL EMPTY → GLOBAL FALLBACK
        if not pool:
            return {
                "question": "Fallback question: 1 + 1 = ?",
                "options": ["1", "2", "3", "4"],
                "correct_answer": "2",
            }

        q, options, correct = random.choice(pool)
        if st.session_state.get("shuffle_options", True):
            random.shuffle(options)

        return {
            "question": q,
            "options": options,
            "correct_answer": correct,
        }

    def generate_ai_question(self, topic, difficulty):
        """
        Simulated AI-generated question.
        (Mentor-safe placeholder for future LLM integration)
        """

        base_question = self.generate_question(topic, difficulty)

        return {
            "question": f"[AI Generated] {base_question['question']}",
            "options": base_question["options"],
            "correct_answer": base_question["correct_answer"],
            "ai_generated": True
        }
    