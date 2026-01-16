from datetime import datetime
from v2.database import get_connection, now


class ProgressTracker:
    """
    SQLite-based progress tracker (v2).
    Mirrors the API of ProgressTracker (JSON version).
    """

    # -----------------------------
    # STUDENT HANDLING
    # -----------------------------
    def get_or_create_student(self, student_name):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM users WHERE username = ?",
            (student_name,)
        )
        row = cur.fetchone()

        if row:
            user_id = row[0]
        else:
            cur.execute(
                "INSERT INTO users (username, created_at) VALUES (?, ?)",
                (student_name, now())
            )
            conn.commit()
            user_id = cur.lastrowid

        conn.close()
        return user_id

    # -----------------------------
    # PROGRESS SUMMARY (FIXED)
    # -----------------------------
    def get_student_progress(self, student_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT topic, accuracy
            FROM progress
            WHERE user_id = ?
        """, (student_id,))
        rows = cur.fetchall()
        conn.close()

        if not rows:
            return {
                "topics_completed": 0,
                "topics_mastered": 0,
                "total_activities": 0,
                "overall_score": 0,
                "average_accuracy": 0,
                "topic_scores": {}
            }

        total_attempts = len(rows)
        avg_accuracy = sum(r[1] for r in rows) / total_attempts

        topic_scores = {}
        for topic, accuracy in rows:
            if topic not in topic_scores:
                topic_scores[topic] = {
                    "attempts": 0,
                    "correct": 0
                }

            topic_scores[topic]["attempts"] += 1
            if accuracy == 100:
                topic_scores[topic]["correct"] += 1

        topics_completed = len(topic_scores)
        topics_mastered = sum(
            1 for t in topic_scores.values()
            if t["correct"] / t["attempts"] >= 0.8
        )

        return {
            "topics_completed": topics_completed,
            "topics_mastered": topics_mastered,
            "total_activities": total_attempts,
            "overall_score": avg_accuracy,          # used only if needed
            "average_accuracy": avg_accuracy,       # true accuracy
            "topic_scores": topic_scores
        }

    # -----------------------------
    # RECORD QUIZ RESPONSE
    # -----------------------------
    def record_quiz_response(self, student_id, topic, is_correct, response_time):
        conn = get_connection()
        cur = conn.cursor()

        accuracy = 100 if is_correct else 0

        cur.execute("""
            INSERT INTO progress (
                user_id, topic, accuracy, response_time, timestamp
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            student_id,
            topic,
            accuracy,
            response_time,
            now()
        ))

        conn.commit()
        conn.close()

    # -----------------------------
    # LEARNING HISTORY
    # -----------------------------
    def get_learning_history(self, student_id, limit=None):
        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT topic, accuracy, response_time, timestamp
            FROM progress
            WHERE user_id = ?
            ORDER BY timestamp DESC
        """
        if limit:
            query += f" LIMIT {limit}"

        cur.execute(query, (student_id,))
        rows = cur.fetchall()
        conn.close()

        return [
            {
                "topic": r[0],
                "accuracy": r[1],
                "response_time": r[2],
                "date": r[3]
            }
            for r in rows
        ]

    # -----------------------------
    # RECENT ACTIVITY
    # -----------------------------
    def get_recent_activity(self, student_id, limit=5):
        history = self.get_learning_history(student_id, limit)

        activities = []
        for h in history:
            is_correct = h["accuracy"] == 100
            result = "✅ Correct" if is_correct else "❌ Incorrect"

            activities.append({
                "date": h["date"][:16].replace("T", " "),
                "topic": h["topic"],
                "is_correct": is_correct,
                "description": f"{result} on {h['topic']} quiz"
            })

        return activities

    # -----------------------------
    # TOPIC PROGRESS
    # -----------------------------
    def get_topic_progress(self, student_id, topic):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT accuracy, response_time
            FROM progress
            WHERE user_id = ? AND topic = ?
        """, (student_id, topic))

        rows = cur.fetchall()
        conn.close()

        if not rows:
            return {
                "total_questions": 0,
                "correct_answers": 0,
                "accuracy": 0,
                "average_time": 0,
                "attempts": 0
            }

        total = len(rows)
        correct = sum(1 for r in rows if r[0] == 100)
        avg_time = sum(r[1] for r in rows) / total

        return {
            "total_questions": total,
            "correct_answers": correct,
            "accuracy": (correct / total) * 100,
            "average_time": avg_time,
            "attempts": total
        }

    # -----------------------------
    # RESET PROGRESS
    # -----------------------------
    def reset_student_progress(self, student_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM progress WHERE user_id = ?",
            (student_id,)
        )

        conn.commit()
        conn.close()

    # -----------------------------
    # OVERALL SCORE (SEPARATE FROM ACCURACY)
    # -----------------------------
    def compute_overall_score(self, student_id):
        p = self.get_student_progress(student_id)

        accuracy = p["average_accuracy"]     # %
        topics = p["topics_completed"]       # count

        consistency_score = min(topics * 15, 100)

        overall = (
            accuracy * 0.7 +
            consistency_score * 0.3
        )

        return round(overall, 1)

    # -----------------------------
    # ALL TOPIC PROGRESS
    # -----------------------------
    def get_all_topic_progress(self, student_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT topic,
                COUNT(*) as attempts,
                SUM(CASE WHEN accuracy = 100 THEN 1 ELSE 0 END) as correct
            FROM progress
            WHERE user_id = ?
            GROUP BY topic
        """, (student_id,))

        rows = cur.fetchall()
        conn.close()

        topic_progress = {}

        for topic, attempts, correct in rows:
            accuracy = (correct / attempts) * 100 if attempts else 0

            topic_progress[topic] = {
                "attempts": attempts,
                "accuracy": accuracy
            }

        return topic_progress
