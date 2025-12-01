# AI Tutor System - Setup & Usage Guide

## Overview
Your AI Tutor System is now integrated with **Gemini 2.5 Flash**, providing:
- ✅ Structured AI-powered education assistant
- ✅ Class-wise, subject-wise, and topic-wise organization
- ✅ NCERT curriculum & government exam preparation support
- ✅ Multi-language responses (English, Hindi, Spanish, French)
- ✅ Question history tracking
- ✅ Follow-up topic suggestions

---

## 1. Initial Setup

### Step 1: Get Your Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key"
4. Copy your API key

### Step 2: Update Settings
Edit `aitutor/settings.py` and replace the placeholder:

```python
GEMINI_API_KEY = "your-gemini-api-key-here"  # Replace with your actual key
GEMINI_MODEL = "gemini-2.5-flash"
```

Or set it as an environment variable in your `.env` file:
```
GEMINI_API_KEY=your-actual-api-key-here
```

### Step 3: Install Required Package
```bash
pip install google-generativeai
```

---

## 2. Database Setup

### Create Initial Data
To populate the database with NCERT classes, subjects, and topics, run:

```bash
python manage.py shell
```

Then paste this code:

```python
from tutor.models import ClassLevel, Subject, Topic

# Create Class Levels
classes_data = [
    ("Class 9", "NCERT Class 9 - Secondary Education"),
    ("Class 10", "NCERT Class 10 - Secondary Education"),
    ("Class 11", "NCERT Class 11 - Senior Secondary"),
    ("Class 12", "NCERT Class 12 - Senior Secondary"),
    ("JEE Main", "Engineering Entrance Examination"),
    ("NEET", "Medical Entrance Examination"),
]

for class_name, description in classes_data:
    ClassLevel.objects.get_or_create(class_name=class_name, defaults={'description': description})

print("Class Levels created!")

# Example: Add subjects for Class 10
class_10 = ClassLevel.objects.get(class_name="Class 10")
subjects = [
    ("Mathematics", "Algebra, Geometry, Trigonometry"),
    ("Science", "Physics, Chemistry, Biology"),
    ("English", "Literature and Grammar"),
    ("Hindi", "हिंदी साहित्य और व्याकरण"),
]

for subject_name, description in subjects:
    Subject.objects.get_or_create(
        class_level=class_10,
        name=subject_name,
        defaults={'description': description}
    )

print("Subjects created!")

# Example: Add topics for Mathematics
math_subject = Subject.objects.get(class_level=class_10, name="Mathematics")
topics = [
    ("Polynomials", "Algebraic expressions and polynomial equations", "beginner"),
    ("Linear Equations", "Systems of linear equations in two variables", "beginner"),
    ("Quadratic Equations", "Solving quadratic equations", "intermediate"),
    ("Arithmetic Progressions", "Sequences and series", "intermediate"),
    ("Triangles", "Properties of triangles and similarity", "intermediate"),
    ("Circles", "Circle geometry and tangents", "intermediate"),
]

for topic_name, description, level in topics:
    Topic.objects.get_or_create(
        subject=math_subject,
        name=topic_name,
        defaults={'description': description, 'difficulty_level': level}
    )

print("Topics created!")
print("Setup complete!")
```

Press `Ctrl+D` (or `Cmd+D` on Mac) to exit the shell.

---

## 3. API Endpoints

### 1. Get All Class Levels
```
GET /api/ai-tutor/classes/
Authorization: Bearer {access_token}
```

**Response:**
```json
{
    "success": true,
    "data": [
        {"id": 1, "class_name": "Class 10", "description": "..."},
        {"id": 2, "class_name": "JEE Main", "description": "..."}
    ]
}
```

### 2. Get Subjects by Class
```
GET /api/ai-tutor/subjects/?class_id=1
Authorization: Bearer {access_token}
```

**Response:**
```json
{
    "success": true,
    "data": [
        {"id": 1, "name": "Mathematics", "description": "..."},
        {"id": 2, "name": "Science", "description": "..."}
    ]
}
```

### 3. Get Topics by Subject
```
GET /api/ai-tutor/topics/?subject_id=1
Authorization: Bearer {access_token}
```

**Response:**
```json
{
    "success": true,
    "data": [
        {"id": 1, "name": "Polynomials", "description": "...", "difficulty_level": "beginner"},
        {"id": 2, "name": "Linear Equations", "description": "...", "difficulty_level": "beginner"}
    ]
}
```

### 4. Ask AI Tutor a Question
```
POST /api/ai-tutor/ask/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "question": "What is a polynomial?",
    "class_id": 1,
    "subject_id": 1,
    "topic_id": 1
}
```

**Response:**
```json
{
    "success": true,
    "question_id": 123,
    "response_id": 456,
    "answer": "A polynomial is an algebraic expression...",
    "follow_up_suggestions": [
        "Degree of a polynomial",
        "Zeros of polynomials",
        "Factorization"
    ],
    "language": "en"
}
```

### 5. Set Language Preference
```
POST /api/ai-tutor/set-language/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "language": "hi"
}
```

**Supported Languages:**
- `en` - English
- `hi` - Hindi
- `es` - Spanish
- `fr` - French
- `de` - German
- `pt` - Portuguese

### 6. Get Question History
```
GET /api/ai-tutor/history/
Authorization: Bearer {access_token}
```

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "id": 123,
            "question": "What is a polynomial?",
            "class_level": "Class 10",
            "subject": "Mathematics",
            "topic": "Polynomials",
            "created_at": "2025-11-14T10:30:00Z",
            "answer": "..."
        }
    ]
}
```

---

## 4. Using the AI Tutor Web Interface

### Access the Interface
1. Start your Django server: `python manage.py runserver`
2. Go to: `http://localhost:8000/ai-tutor/`
3. Login with your credentials

### How to Use
1. **Select Class/Level** - Choose your class (Class 10, JEE, NEET, etc.)
2. **Select Subject** - Pick a subject (Mathematics, Science, English, etc.)
3. **Select Topic** (Optional) - Choose a specific topic for better context
4. **Ask Your Question** - Type your academic question in natural language
5. **Get Answer** - AI Tutor provides detailed explanation in your preferred language
6. **Follow-up Learning** - Click suggested topics to explore related concepts
7. **Change Language** - Adjust language preference anytime

### Features
- 📚 **Contextual Learning** - Answers tailored to class level and topic
- 🌍 **Multi-Language** - Responses in your preferred language
- 💡 **Smart Suggestions** - Related topics for deeper learning
- 📋 **History Tracking** - Review all your previous questions
- 🎯 **NCERT Aligned** - Curriculum-based content

---

## 5. Example Questions

### Class 10 Mathematics
- "How do I solve quadratic equations using the quadratic formula?"
- "Explain the Pythagorean theorem with an example"
- "What are the properties of similar triangles?"

### Class 12 Chemistry
- "What is the difference between ionic and covalent bonding?"
- "Explain Le Chatelier's principle with an example"
- "How do oxidation-reduction reactions work?"

### JEE Preparation
- "What are the key concepts for JEE Mains in calculus?"
- "Explain simple harmonic motion"
- "What are the important formulas for organic chemistry?"

### NEET Preparation
- "Explain the process of photosynthesis"
- "What is genetic engineering?"
- "Describe the circulatory system"

---

## 6. Admin Panel Management

Access Django admin at: `http://localhost:8000/admin/`

### Manage:
- **Class Levels** - Add/edit NCERT classes or exam types
- **Subjects** - Create subjects for each class
- **Topics** - Define topics within subjects with difficulty levels
- **AI Questions** - View all student questions and interactions
- **AI Responses** - Monitor AI responses and quality
- **User Preferences** - Manage student language preferences

---

## 7. Troubleshooting

### Issue: "Gemini API key not configured"
**Solution:** Set your API key in settings.py or .env file

### Issue: "Language not supported"
**Solution:** Use only supported language codes: en, hi, es, fr, de, pt

### Issue: Empty API response
**Solution:** 
- Check your Gemini API quota
- Ensure question text is not empty
- Verify authentication token is valid

### Issue: Missing class/subject/topic options
**Solution:** Run the database population script from Step 3

---

## 8. Best Practices

1. **Use Specific Questions** - More specific questions = better answers
2. **Select Correct Context** - Choose the right class and subject for accurate explanations
3. **Follow Suggestions** - Explore suggested topics to strengthen understanding
4. **Track Progress** - Review history to track your learning journey
5. **Use Preferred Language** - Study in your most comfortable language

---

## 9. Model Structure

### Database Models
```
ClassLevel
├── Subject
│   └── Topic
│       └── AIQuestion
│           └── AIResponse
└── AIQuestion

CustomUser
├── preferred_language
└── studentprofile
    └── AIQuestion
```

---

## 10. Future Enhancements

Consider implementing:
- [ ] Quiz generation from explanations
- [ ] Study progress analytics
- [ ] Concept mind maps
- [ ] PDF export of Q&A
- [ ] Voice input/output support
- [ ] Real-time collaboration features
- [ ] Teacher admin dashboard

---

**Happy Learning! 🎓**
