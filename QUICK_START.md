# 🚀 Quick Start Guide

<div align="center">

**Get up and running in 5 minutes!**

*Fast setup • Easy to use • Comprehensive features*

</div>

---

## ⚡ Installation (5 Minutes)

### Step 1: Activate Virtual Environment

**Windows:**
```bash
cd "AI Personalized Learning"
venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd "AI Personalized Learning"
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
pip install bcrypt reportlab openai
```

> **📝 Note**: The `requirements.txt` should be updated to include `bcrypt`, `reportlab`, and `openai`

### Step 3: Run the Application

```bash
streamlit run v2/app_v2.py
```

### Step 4: Open in Browser

- The app will automatically open at `http://localhost:8501`
- Or manually visit the URL shown in your terminal

---

## 👋 First Time Usage

### 1️⃣ Create Your Account

1. Click **"Sign Up"** tab
2. Enter your **email** and **password**
3. Click **"Create Account"**
4. You'll see a success message

### 2️⃣ Login

1. Click **"Login"** tab
2. Enter your credentials
3. Click **"Login"**
4. You're in! 🎉

### 3️⃣ Explore Dashboard

- View your **metrics** (will be 0 for new users)
- Check **personalized recommendations**
- See your **recent activity** (empty initially)

### 4️⃣ Start Learning

1. Navigate to **"📚 Start Learning"**
2. Select a topic:
   - 📐 **Mathematics**
   - 🔬 **Science**
   - 💻 **Programming**
   - 🗣️ **Languages**
3. Click **"▶ Start Learning"**
4. Review the topic description
5. Click **"🎯 Start Quiz"**

### 5️⃣ Take Your First Quiz

- Answer **10 questions**
- Get **immediate feedback** (✅ Correct / ❌ Incorrect)
- View your **score** at the end
- Download your **certificate** (optional)

### 6️⃣ Check Your Progress

- Visit **"📊 Progress Analytics"** for charts
- Check **"👤 Learner Profile"** for your learning traits
- Adjust settings in **"⚙️ Settings"**

---

## 🎯 Key Features to Explore

### 🏠 Dashboard
- **Overall Score**: Your comprehensive learning score
- **Accuracy**: Percentage of correct answers
- **Topics Completed**: Number of subjects attempted
- **Learning Pace**: Fast, Moderate, or Slow

### 📚 Start Learning
- **4 Topics Available**: Mathematics, Science, Programming, Languages
- **Adaptive Difficulty**: Automatically adjusts (Easy → Medium → Hard)
- **10 Questions per Quiz**: Randomized from question bank
- **Real-Time Feedback**: Know immediately if you're correct

### 📊 Progress Analytics
- **Performance Charts**: See your improvement over time
- **Topic Analysis**: Compare performance across subjects
- **Activity Heatmaps**: Understand your learning patterns
- **CSV Export**: Download your data

### 👤 Learner Profile
- **Your Level**: Beginner, Intermediate, or Advanced
- **Your Badge**: From 🌱 Starter to 🏆 Master
- **Strengths**: What you're good at
- **Weaknesses**: Areas to improve

### ⚙️ Settings
- **Learning Preferences**: Difficulty, Style, Daily Goals
- **Quiz Options**: Auto-difficulty, Hints, Shuffling
- **Accessibility**: Large text, Reduced animations

---

## 💡 Tips for Best Experience

### ✅ Do's

1. **Complete Multiple Quizzes**: The system learns more about you with more data
2. **Try Different Topics**: Explore all available subjects
3. **Check Analytics Regularly**: Monitor your progress over time
4. **Use Settings**: Customize your learning preferences
5. **Review Mistakes**: Learn from incorrect answers
6. **Set Daily Goals**: Stay motivated with study targets

### ❌ Don'ts

1. Don't skip questions too often (affects accuracy)
2. Don't ignore weak areas (use recommendations)
3. Don't forget to check your profile (see your progress)
4. Don't disable auto-difficulty (for best adaptation)

---

## 🔧 Troubleshooting

### Issue: Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'bcrypt'`

**Solution**:
```bash
pip install bcrypt reportlab
```

### Issue: Port Already in Use

**Problem**: `Port 8501 is already in use`

**Solution**:
- Streamlit will automatically use the next available port
- Or specify a port: `streamlit run v2/app_v2.py --server.port 8502`

### Issue: Database Error

**Problem**: `OperationalError: no such table`

**Solution**:
- Delete `learning_v2.db` file
- Restart the app (it will recreate the database)

---

## 🎓 Example Learning Flow

### Day 1: Getting Started

1. ✅ Sign up and login
2. ✅ Explore dashboard
3. ✅ Take Mathematics quiz (Easy)
4. ✅ Check your score
5. ✅ Review learner profile

### Day 2: Building Momentum

1. ✅ Take Science quiz
2. ✅ View analytics charts
3. ✅ Adjust settings preferences
4. ✅ Set daily goal (30 minutes)

### Day 3: Advancing

1. ✅ Take Programming quiz
2. ✅ System adapts to Medium difficulty
3. ✅ Check recommendations
4. ✅ Download certificate

### Day 4+: Mastery

1. ✅ Practice weak topics
2. ✅ Achieve higher badges
3. ✅ Maintain learning streak
4. ✅ Export analytics data

---

## 📱 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Storage**: 500MB free space
- **Browser**: Chrome, Firefox, Edge, or Safari (latest versions)

---

## 🔗 Quick Links

- **Main App**: `v2/app_v2.py`
- **Run Command**: `streamlit run v2/app_v2.py`
- **Database**: `learning_v2.db` (auto-generated)
- **Documentation**: `README.md`

---

## ❓ Need Help?

1. **Check Documentation**: Read `README.md` for detailed info
2. **Review Code**: All logic is in `v2/app_v2.py`
3. **Check Issues**: Review troubleshooting section above
4. **Database Reset**: Delete `learning_v2.db` and restart

---

## 🎉 You're Ready!

**Start your personalized learning journey now!**

```bash
streamlit run v2/app_v2.py
```

**Happy Learning! 🚀📚**

---

<div align="center">

*Last Updated: Based on app_v2.py implementation*

**Questions? Check README.md for detailed documentation**

</div>
