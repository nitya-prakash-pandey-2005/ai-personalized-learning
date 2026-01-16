class ResourceRecommender:

    def recommend(self, topic):
        resources = {
            "Mathematics": [
                ("Khan Academy – Math", "https://www.khanacademy.org/math"),
                ("3Blue1Brown", "https://www.youtube.com/@3blue1brown")
            ],
            "Science": [
                ("CrashCourse Science", "https://www.youtube.com/@crashcourse"),
                ("Khan Academy – Science", "https://www.khanacademy.org/science")
            ],
            "Programming": [
                ("freeCodeCamp", "https://www.youtube.com/@freecodecamp"),
                ("GeeksForGeeks", "https://www.geeksforgeeks.org")
            ],
            "Languages": [
                ("BBC Learning English", "https://www.bbc.co.uk/learningenglish"),
                ("Grammarly Blog", "https://www.grammarly.com/blog")
            ]
        }
        return resources.get(topic, [])
