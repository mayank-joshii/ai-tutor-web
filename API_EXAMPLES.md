# API Examples - AI Tutor System

Use these examples to test the AI Tutor API with tools like Postman, curl, or Insomnia.

## Base URL
```
http://localhost:8000
```

---

## 1. Authentication

### Register New User
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "secure_password123"
  }'
```

**Response:**
```json
{
    "message": "User created successfully.",
    "username": "student1"
}
```

### Login User
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "secure_password123"
  }'
```

**Response:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

> Save the `access` token for subsequent requests

---

## 2. Get Class Levels

### Request
```bash
curl -X GET http://localhost:8000/api/ai-tutor/classes/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Response
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "class_name": "Class 9",
            "description": "NCERT Class 9 - Secondary Education"
        },
        {
            "id": 2,
            "class_name": "Class 10",
            "description": "NCERT Class 10 - Secondary Education"
        },
        {
            "id": 3,
            "class_name": "Class 11",
            "description": "NCERT Class 11 - Senior Secondary"
        },
        {
            "id": 4,
            "class_name": "Class 12",
            "description": "NCERT Class 12 - Senior Secondary"
        },
        {
            "id": 5,
            "class_name": "JEE Main",
            "description": "Engineering Entrance Examination - Main"
        },
        {
            "id": 6,
            "class_name": "NEET",
            "description": "Medical Entrance Examination"
        }
    ]
}
```

---

## 3. Get Subjects by Class

### Request
```bash
curl -X GET "http://localhost:8000/api/ai-tutor/subjects/?class_id=2" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Response
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Mathematics",
            "description": "Algebra, Geometry, Trigonometry, Statistics"
        },
        {
            "id": 2,
            "name": "Science",
            "description": "Physics, Chemistry, Biology"
        },
        {
            "id": 3,
            "name": "English",
            "description": "Literature, Grammar, Writing Skills"
        },
        {
            "id": 4,
            "name": "Hindi",
            "description": "साहित्य और व्याकरण"
        },
        {
            "id": 5,
            "name": "Social Studies",
            "description": "History, Geography, Political Science, Economics"
        }
    ]
}
```

---

## 4. Get Topics by Subject

### Request
```bash
curl -X GET "http://localhost:8000/api/ai-tutor/topics/?subject_id=1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Response
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Real Numbers",
            "description": "Classification of numbers, operations, properties",
            "difficulty_level": "beginner"
        },
        {
            "id": 2,
            "name": "Polynomials",
            "description": "Algebraic expressions, polynomial equations, division",
            "difficulty_level": "beginner"
        },
        {
            "id": 3,
            "name": "Pair of Linear Equations",
            "description": "Systems of equations, graphical and algebraic solutions",
            "difficulty_level": "beginner"
        },
        {
            "id": 4,
            "name": "Quadratic Equations",
            "description": "Solving by factoring, completing square, quadratic formula",
            "difficulty_level": "intermediate"
        }
    ]
}
```

---

## 5. Ask AI Tutor a Question

### Request (Minimal)
```bash
curl -X POST http://localhost:8000/api/ai-tutor/ask/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is a polynomial?"
  }'
```

### Request (With Full Context)
```bash
curl -X POST http://localhost:8000/api/ai-tutor/ask/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I solve the quadratic equation x² - 5x + 6 = 0?",
    "class_id": 2,
    "subject_id": 1,
    "topic_id": 4
  }'
```

### Response
```json
{
    "success": true,
    "question_id": 1,
    "response_id": 1,
    "answer": "A polynomial is an algebraic expression consisting of variables and coefficients combined using addition, subtraction, and multiplication. For example, 3x² + 2x + 1 is a polynomial.\n\nKey characteristics:\n- Variables are raised to non-negative integer powers\n- Coefficients are constants\n- Can have one or more terms\n\nTypes of polynomials:\n- Monomial: Single term (e.g., 5x)\n- Binomial: Two terms (e.g., 3x + 2)\n- Trinomial: Three terms (e.g., x² + 3x + 2)\n\nDegree of polynomial is the highest power of the variable.",
    "follow_up_suggestions": [
        "Degree of a polynomial and how to find it",
        "Zeros and roots of polynomials",
        "Polynomial division and remainder theorem"
    ],
    "language": "en"
}
```

---

## 6. Set Language Preference

### Request
```bash
curl -X POST http://localhost:8000/api/ai-tutor/set-language/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "hi"
  }'
```

### Response
```json
{
    "success": true,
    "message": "Language preference set to Hindi",
    "language": "hi"
}
```

### Available Languages
```json
{
    "en": "English",
    "hi": "Hindi (हिंदी)",
    "es": "Spanish (Español)",
    "fr": "French (Français)",
    "de": "German (Deutsch)",
    "pt": "Portuguese (Português)"
}
```

---

## 7. Ask Question in Hindi

### Request
```bash
curl -X POST http://localhost:8000/api/ai-tutor/ask/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "बहुपद क्या है?",
    "class_id": 2,
    "subject_id": 1,
    "topic_id": 2
  }'
```

### Response (Will be in Hindi)
```json
{
    "success": true,
    "question_id": 2,
    "response_id": 2,
    "answer": "बहुपद एक बीजीय व्यंजक है जो चर और गुणांकों से मिलकर बना होता है।\n\nउदाहरण: 3x² + 2x + 1\n\nमुख्य विशेषताएं:\n- चर को गैर-नकारात्मक पूर्णांक घातों तक बढ़ाया जाता है\n- गुणांक स्थिरांक होते हैं\n- एक या अधिक पद हो सकते हैं\n\nबहुपद के प्रकार:\n- एकपदी: एक पद (जैसे 5x)\n- द्विपद: दो पद (जैसे 3x + 2)\n- त्रिपद: तीन पद (जैसे x² + 3x + 2)",
    "follow_up_suggestions": [
        "बहुपद की डिग्री",
        "बहुपद के शून्य",
        "बहुपद विभाजन"
    ],
    "language": "hi"
}
```

---

## 8. Get Question History

### Request
```bash
curl -X GET http://localhost:8000/api/ai-tutor/history/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Response
```json
{
    "success": true,
    "data": [
        {
            "id": 2,
            "question": "बहुपद क्या है?",
            "class_level": "Class 10",
            "subject": "Mathematics",
            "topic": "Polynomials",
            "created_at": "2025-11-14T10:45:23.123456Z",
            "answer": "बहुपद एक बीजीय व्यंजक है..."
        },
        {
            "id": 1,
            "question": "What is a polynomial?",
            "class_level": "Class 10",
            "subject": "Mathematics",
            "topic": "Polynomials",
            "created_at": "2025-11-14T10:30:15.654321Z",
            "answer": "A polynomial is an algebraic expression..."
        }
    ]
}
```

---

## Testing Checklist

- [ ] Register a new user
- [ ] Login and get access token
- [ ] Get all class levels
- [ ] Get subjects for a class
- [ ] Get topics for a subject
- [ ] Ask a question with context
- [ ] Ask a question in Hindi
- [ ] Ask a question in Spanish
- [ ] Set language preference
- [ ] Get question history
- [ ] Verify follow-up suggestions
- [ ] Test with invalid tokens
- [ ] Test with missing parameters

---

## Error Responses

### 400 Bad Request
```json
{
    "error": "Question text is required"
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 500 Internal Server Error
```json
{
    "error": "Gemini API error: Invalid API key"
}
```

---

## Postman Collection

Create a new Postman collection with these environment variables:

```json
{
    "base_url": "http://localhost:8000",
    "access_token": "{{Your access token here}}"
}
```

Then import the requests above using `{{base_url}}` and `{{access_token}}` placeholders.

---

## Rate Limiting (Future Implementation)

Consider adding rate limiting:

```python
# Not implemented yet
# Example: 100 requests per hour per user
```

---

## Webhook Support (Future)

Consider webhook callbacks for:
- New question asked
- AI response generated
- Question marked as helpful

---

**Last Updated**: November 2025
