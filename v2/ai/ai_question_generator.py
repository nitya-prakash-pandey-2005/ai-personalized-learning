from openai import OpenAI
import random

client = OpenAI()

class AIQuestionGenerator:

    def generate_question(self, topic, difficulty):
        prompt = f"""
        Generate ONE multiple-choice question on the topic "{topic}".
        Difficulty: {difficulty}

        Format STRICTLY as JSON:
        {{
            "question": "...",
            "options": ["A", "B", "C", "D"],
            "correct_answer": "A"
        }}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert quiz generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )

        content = response.choices[0].message.content

        try:
            data = eval(content)
        except:
            # Fallback safe question
            data = {
                "question": f"Basic question on {topic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A"
            }

        random.shuffle(data["options"])
        return data

    def get_learning_resources(self, topic):
        return [
            f"https://www.youtube.com/results?search_query={topic}+tutorial",
            f"https://www.khanacademy.org/search?page_search_query={topic}",
            f"https://www.geeksforgeeks.org/{topic.replace(' ', '-')}/"
        ]
