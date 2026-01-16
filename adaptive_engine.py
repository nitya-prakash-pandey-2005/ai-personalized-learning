from learner_profiler import LearnerProfiler
from v2.progress_tracker_v2 import ProgressTracker
from content_manager import ContentManager

class AdaptiveEngine:
    """
    Core adaptive learning engine that makes personalized recommendations
    and adjusts content based on learner performance and profile.
    """
    
    def __init__(self):
        self.profiler = LearnerProfiler()
        self.tracker = ProgressTracker()
        self.content_manager = ContentManager()
    
    def get_recommendations(self, student_id):
        """Get personalized learning recommendations for a student."""
        profile = self.profiler.get_profile(student_id)
        progress = self.tracker.get_student_progress(student_id)
        
        recommendations = []
        
        # Recommend based on performance
        average_accuracy = progress.get('average_accuracy', 0)
        if average_accuracy < 50:
            recommendations.append({
                'title': 'Practice Basic Concepts',
                'description': 'Your performance suggests you should review fundamental concepts. Start with easier topics to build confidence.',
                'topic': 'Mathematics',
                'priority': 'High'
            })
        elif average_accuracy > 80:
            recommendations.append({
                'title': 'Challenge Yourself',
                'description': 'You\'re doing great! Try more advanced topics to deepen your understanding.',
                'topic': 'Science',
                'priority': 'Medium'
            })
        
        # Recommend based on topics not yet attempted
        attempted_topics = set(progress.get('topic_scores', {}).keys())
        all_topics = set(self.content_manager.get_available_topics())
        unattempted = all_topics - attempted_topics
        
        for topic in list(unattempted)[:2]:
            recommendations.append({
                'title': f'Explore {topic}',
                'description': f'You haven\'t tried {topic} yet. Give it a go!',
                'topic': topic,
                'priority': 'Medium'
            })
        
        # Recommend topics that need improvement
        for topic, scores in progress.get('topic_scores', {}).items():
            if scores['total'] > 0:
                accuracy = (scores['correct'] / scores['total']) * 100
                if 40 <= accuracy < 70:
                    recommendations.append({
                        'title': f'Improve {topic} Skills',
                        'description': f'You\'re making progress in {topic}, but more practice will help you master it.',
                        'topic': topic,
                        'priority': 'High'
                    })
        
        # Default recommendation if none
        if not recommendations:
            recommendations.append({
                'title': 'Start Learning',
                'description': 'Begin your learning journey by selecting a topic that interests you!',
                'topic': 'Mathematics',
                'priority': 'Low'
            })
        
        return recommendations
    
    def get_next_steps(self, student_id, current_topic, accuracy):
        """Get next steps after completing a quiz."""
        profile = self.profiler.get_profile(student_id)
        progress = self.tracker.get_student_progress(student_id)
        
        if accuracy >= 80:
            # High performance - suggest advanced content
            return {
                'message': f'🎉 Excellent work! You scored {accuracy:.1f}% on {current_topic}. You\'re ready for more challenging content!',
                'action': 'challenge',
                'suggested_topics': self._get_advanced_topics(current_topic)
            }
        elif accuracy >= 60:
            # Moderate performance - suggest practice
            return {
                'message': f'👍 Good job! You scored {accuracy:.1f}% on {current_topic}. A bit more practice will help you master this topic.',
                'action': 'practice',
                'suggested_topics': [current_topic]
            }
        else:
            # Low performance - suggest review
            return {
                'message': f'📚 You scored {accuracy:.1f}% on {current_topic}. Don\'t worry! Review the basics and try again. Learning takes time!',
                'action': 'review',
                'suggested_topics': self._get_review_topics(current_topic)
            }
    
    def _get_advanced_topics(self, current_topic):
        """Get advanced topics related to current topic."""
        topic_map = {
            'Mathematics': ['Science', 'Programming'],
            'Science': ['Programming', 'Mathematics'],
            'Programming': ['Mathematics', 'Science'],
            'Languages': ['Programming']
        }
        return topic_map.get(current_topic, ['Mathematics', 'Science'])
    
    def _get_review_topics(self, current_topic):
        """Get review topics (same topic for practice)."""
        return [current_topic]
    
    def get_learning_path(self, student_id):
        """Generate a personalized learning path for the student."""
        profile = self.profiler.get_profile(student_id)
        progress = self.tracker.get_student_progress(student_id)
        
        # Get all topics
        all_topics = self.content_manager.get_available_topics()
        attempted_topics = set(progress.get('topic_scores', {}).keys())
        
        learning_path = []
        
        # Start with unattempted topics
        for topic in all_topics:
            if topic not in attempted_topics:
                learning_path.append({
                    'topic': topic,
                    'description': f'Learn the fundamentals of {topic}',
                    'completed': False,
                    'order': len(learning_path) + 1
                })
        
        # Add topics that need improvement
        for topic, scores in progress.get('topic_scores', {}).items():
            if scores['total'] > 0:
                accuracy = (scores['correct'] / scores['total']) * 100
                if accuracy < 80:
                    learning_path.append({
                        'topic': topic,
                        'description': f'Practice and improve your {topic} skills',
                        'completed': False,
                        'order': len(learning_path) + 1
                    })
                else:
                    learning_path.append({
                        'topic': topic,
                        'description': f'Mastered {topic} - Great job!',
                        'completed': True,
                        'order': len(learning_path) + 1
                    })
        
        return learning_path[:5]  # Return top 5 recommendations
    
    def adapt_difficulty(self, student_id, topic):
        """Determine appropriate difficulty level for a student on a topic."""
        profile = self.profiler.get_profile(student_id)
        progress = self.tracker.get_student_progress(student_id)
        
        # Check topic-specific performance
        topic_scores_dict = progress.get('topic_scores', {})
        if topic in topic_scores_dict:
            topic_scores = topic_scores_dict[topic]
            if topic_scores.get('total', 0) > 0:
                accuracy = (topic_scores['correct'] / topic_scores['total']) * 100
                
                if accuracy >= 85:
                    return 'Hard'
                elif accuracy < 50:
                    return 'Easy'
                else:
                    return 'Medium'
        
        # Use overall profile
        average_accuracy = profile.get('average_accuracy', 0)
        if average_accuracy >= 80:
            return 'Hard'
        elif average_accuracy < 50:
            return 'Easy'
        else:
            return 'Medium'
    
    def should_show_hint(self, student_id, topic, question_attempts):
        """Determine if a hint should be shown based on learner profile."""
        profile = self.profiler.get_profile(student_id)
        
        # Show hints for struggling learners or after multiple attempts
        if profile['confidence'] == 'Low' or question_attempts >= 2:
            return True
        
        return False
    
    def get_personalized_feedback(self, student_id, is_correct, response_time):
        """Generate personalized feedback based on performance."""
        profile = self.profiler.get_profile(student_id)
        
        if is_correct:
            if response_time < 30:
                return "⚡ Excellent! You answered quickly and correctly. You really understand this concept!"
            else:
                return "✅ Great job! You got it right. Keep up the good work!"
        else:
            if profile['confidence'] == 'Low':
                return "💪 Don't give up! Review the concept and try again. Every mistake is a learning opportunity."
            else:
                return "📚 Not quite right, but that's okay! Take your time to understand the concept better."

    def decide_difficulty(self, accuracy):
        if accuracy >= 80:
            return "Hard"
        elif accuracy >= 50:
            return "Medium"
        return "Easy"

    def needs_resources(self, accuracy):
        return accuracy < 60
