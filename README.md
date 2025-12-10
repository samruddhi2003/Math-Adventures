# Math Adventures — Adaptive Learning App

Math Adventures is a fun, kid-friendly math learning app built using Streamlit.  
It helps children (ages 5–10) practice basic arithmetic while the system **automatically adjusts difficulty** based on their performance.

## 🎯 What This App Does
- Generates math questions (addition, subtraction, multiplication, division)
- Tracks correctness, response time, and streaks
- Adapts difficulty (Easy → Medium → Hard and vice-versa)
- Rewards learners with:
  - Coins 🪙
  - Streak bonuses 🔥
  - Dancing cartoon animations 🎉
- Shows a summary of performance at the end

## 🧠 Adaptive Logic
The app adjusts difficulty depending on:
- How many recent answers were correct  
- How fast the learner responds  
- Their streak level  

This keeps learners in the **optimal challenge zone**—not too easy, not too hard.

---

## 📘 Rule-Based Difficulty Logic
Math Adventures uses a simple and effective **rule-based adaptive engine** to determine the difficulty of the next question.

### **Decision Rules**
IF correctness ≥ 70%: 
Increase difficulty  
ELIF correctness between 40–70%:  
Keep difficulty the same  
ELSE:  
Decrease difficulty  

### **Additional Rules**
- If streak ≥ 3 → encourage harder difficulty  
- If response time is slow → reduce difficulty  
- If mistakes repeatedly occur in a topic → temporarily lower difficulty  

These rules ensure difficulty increases when the learner is performing well, and decreases when they are struggling—creating a smooth, personalized learning experience.

---

## 🚀 How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
