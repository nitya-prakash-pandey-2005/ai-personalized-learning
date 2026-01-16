import numpy as np
from v2.database import get_connection


class LearnerProfiler:
    """
    Profiles learners based on performance, pace, confidence & engagement.
    SQLite-backed (persistent).
    """

    # -------------------------
    # PUBLIC METHODS
    # -------------------------

    def get_profile(self, student_id):
        """Fetch profile or return default"""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT learning_style, difficulty
        FROM preferences
        WHERE user_id = ?
        """, (student_id,))

        row = cur.fetchone()
        conn.close()

        profile = self._create_default_profile()

        if row:
            profile["style"] = row[0] or "Visual"
            profile["preferred_difficulty"] = row[1] or "Medium"

        return profile

    def update_profile(self, student_id):
        """Recompute learner profile from progress table"""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT accuracy, response_time
        FROM progress
        WHERE user_id = ?
        """, (student_id,))

        rows = cur.fetchall()
        conn.close()

        profile = self.get_profile(student_id)

        if not rows:
            return profile

        accuracies = [r[0] for r in rows if r[0] is not None]
        times = [r[1] for r in rows if r[1] is not None]

        profile["total_activities"] = len(accuracies)
        profile["average_accuracy"] = round(np.mean(accuracies), 2)
        profile["average_time"] = round(np.mean(times), 2)

        # -------------------------
        # PACE
        # -------------------------
        if profile["average_time"] < 30:
            profile["pace"] = "Fast"
        elif profile["average_time"] > 90:
            profile["pace"] = "Slow"
        else:
            profile["pace"] = "Moderate"

        # -------------------------
        # ENGAGEMENT
        # -------------------------
        if profile["average_accuracy"] >= 80:
            profile["engagement"] = "High"
        elif profile["average_accuracy"] < 50:
            profile["engagement"] = "Low"
        else:
            profile["engagement"] = "Medium"

        # -------------------------
        # CONFIDENCE
        # -------------------------
        if profile["average_accuracy"] >= 75:
            profile["confidence"] = "High"
        elif profile["average_accuracy"] < 50:
            profile["confidence"] = "Low"
        else:
            profile["confidence"] = "Medium"

        # -------------------------
        # OVERALL SCORE (DIFFERENT FROM ACCURACY)
        # -------------------------
        profile["overall_score"] = self._calculate_overall_score(profile)

        # -------------------------
        # LEVEL & BADGE
        # -------------------------
        profile["level"] = self._get_level(profile["overall_score"])
        profile["badge"] = self._get_badge(profile["overall_score"])

        # -------------------------
        # STRENGTHS & WEAKNESSES
        # -------------------------
        self._update_strengths_weaknesses(profile)

        return profile

    # -------------------------
    # INTERNAL HELPERS
    # -------------------------

    def _create_default_profile(self):
        return {
            "pace": "Moderate",
            "style": "Visual",
            "engagement": "Medium",
            "confidence": "Medium",
            "preferred_difficulty": "Medium",
            "strengths": [],
            "weaknesses": [],
            "total_activities": 0,
            "average_accuracy": 0,
            "average_time": 0,
            "overall_score": 0,
            "level": "Beginner",
            "badge": "🌱 Starter"
        }

    def _calculate_overall_score(self, profile):
        """
        Overall score ≠ accuracy
        Combines accuracy, speed & consistency
        """
        score = (
            profile["average_accuracy"] * 0.6 +
            max(0, 100 - profile["average_time"]) * 0.25 +
            min(profile["total_activities"] * 2, 20)
        )
        return round(min(score, 100), 2)

    def _get_level(self, score):
        if score >= 85:
            return "Advanced"
        elif score >= 60:
            return "Intermediate"
        return "Beginner"

    def _get_badge(self, score):
        if score >= 90:
            return "🏆 Master"
        elif score >= 75:
            return "🔥 Pro Learner"
        elif score >= 60:
            return "🚀 Improving"
        return "🌱 Starter"

    def _update_strengths_weaknesses(self, profile):
        profile["strengths"].clear()
        profile["weaknesses"].clear()

        if profile["average_accuracy"] >= 80:
            profile["strengths"].append("Strong conceptual understanding")
        if profile["pace"] == "Fast":
            profile["strengths"].append("Quick problem-solving speed")
        if profile["engagement"] == "High":
            profile["strengths"].append("Highly engaged learner")

        if profile["average_accuracy"] < 60:
            profile["weaknesses"].append("Needs more conceptual practice")
        if profile["pace"] == "Slow":
            profile["weaknesses"].append("Takes more time per question")
        if not profile["strengths"]:
            profile["strengths"].append("Consistent learner")

    # -------------------------
    # PREFERENCES
    # -------------------------

    def update_preferences(self, student_id, preferences):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        INSERT OR REPLACE INTO preferences
        (user_id, learning_style, difficulty)
        VALUES (?, ?, ?)
        """, (
            student_id,
            preferences.get("style"),
            preferences.get("preferred_difficulty")
        ))

        conn.commit()
        conn.close()

    def get_all_topic_progress(self, student_id):
        """
        Returns progress for all topics for a student
        """
        student_data = self.progress_data.get(student_id, {})

        topic_progress = {}

        for topic, data in student_data.items():
            attempts = data.get("attempts", 0)
            correct = data.get("correct", 0)

            accuracy = (correct / attempts) * 100 if attempts > 0 else 0

            topic_progress[topic] = {
                "attempts": attempts,
                "accuracy": accuracy
            }

        return topic_progress
