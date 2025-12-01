# AI Tutor System - Quick Reference

## 🎯 Core Features

| Feature | Details |
|---------|---------|
| **AI Model** | Gemini 2.5 Flash |
| **Languages** | English, Hindi, Spanish, French, German, Portuguese |
| **Organization** | Class-wise, Subject-wise, Topic-wise (NCERT aligned) |
| **Exam Prep** | JEE Main, NEET, and board exams support |
| **History** | Tracks all student questions and AI responses |

---

## 🔧 Technical Stack

- **Backend**: Django + Django REST Framework
- **AI**: Google Generative AI (Gemini 2.5 Flash)
- **Database**: SQLite3
- **Authentication**: JWT Tokens
- **Frontend**: Bootstrap 5 + Vanilla JavaScript
- **Security**: CORS headers, Permission classes

---

## 📱 API Quick Reference

### Authentication
```bash
POST /api/login/
POST /api/register/
POST /api/token/refresh/
```

### AI Tutor
```bash
GET    /api/ai-tutor/classes/
GET    /api/ai-tutor/subjects/?class_id=1
GET    /api/ai-tutor/topics/?subject_id=1
POST   /api/ai-tutor/ask/
POST   /api/ai-tutor/set-language/
GET    /api/ai-tutor/history/
```

---

## 🔑 Configuration

### Required Settings
```python
# In aitutor/settings.py
GEMINI_API_KEY = "your-api-key"
GEMINI_MODEL = "gemini-2.5-flash"
```

### Supported Languages
```
'en' → English
'hi' → Hindi (हिंदी)
'es' → Spanish (Español)
'fr' → French (Français)
'de' → German (Deutsch)
'pt' → Portuguese (Português)
```

---

## 📊 Database Models

```
ClassLevel ─── Subject ─── Topic ─── AIQuestion ─── AIResponse
                                          │
                                          └─── studentprofile
                                                     │
                                                     └─── CustomUser
```

---

## 🚀 Getting Started in 5 Steps

1. **Install packages**
   ```bash
   pip install google-generativeai
   ```

2. **Set API key**
   ```python
   # aitutor/settings.py
   GEMINI_API_KEY = "sk-..."
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Populate data** (Optional)
   ```bash
   python manage.py shell < populate_data.py
   ```

5. **Start server**
   ```bash
   python manage.py runserver
   ```

---

## 🎓 Example Questions by Subject

### Mathematics (Class 10)
- "Solve x² - 5x + 6 = 0"
- "What is the Pythagorean theorem?"
- "Explain arithmetic progressions"

### Science (Class 10)
- "What is photosynthesis?"
- "Explain Newton's laws of motion"
- "What is the water cycle?"

### JEE Preparation
- "Explain limits and continuity"
- "What are differential equations?"
- "Explain thermodynamics laws"

### NEET Preparation
- "What is meiosis?"
- "Explain the nervous system"
- "What is enzyme kinetics?"

---

## 🔐 Default Permissions

| Endpoint | Authenticated | Unauthenticated |
|----------|:-------------:|:---------------:|
| `/api/login/` | ✅ | ✅ |
| `/api/register/` | ✅ | ✅ |
| `/api/ai-tutor/ask/` | ✅ | ❌ |
| `/api/ai-tutor/history/` | ✅ | ❌ |
| `/ai-tutor/` | ✅ | ❌ |
| `/admin/` | Admin | ❌ |

---

## 📈 Performance Tips

1. Cache class/subject/topic queries
2. Use pagination for history (20 items default)
3. Monitor Gemini API usage
4. Set up logging for debugging
5. Use CDN for static files in production

---

## 🐛 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| API Key Error | Set `GEMINI_API_KEY` in settings |
| CORS Error | Check `CORS_ALLOWED_ORIGINS` |
| 401 Unauthorized | Verify JWT token is valid |
| Database Error | Run `python manage.py migrate` |
| Empty Options | Populate data using admin or shell |

---

## 📂 File Structure

```
aitutor/
├── settings.py (config)
├── urls.py (main routes)
└── asgi/wsgi.py

tutor/
├── models.py (6 new models)
├── views.py (6 new API views + AITutorService)
├── urls.py (7 new routes)
├── admin.py (8 admin classes)
└── migrations/0006_*.py

templates/
├── login.html (existing)
├── ai_tutor.html (NEW - main UI)
└── register.html (existing)

static/ (NEW - for static files)

AI_TUTOR_SETUP.md (complete setup guide)
IMPLEMENTATION_SUMMARY.md (feature overview)
```

---

## 🎯 Next Steps

1. Get Gemini API key from [aistudio.google.com](https://aistudio.google.com/)
2. Update `GEMINI_API_KEY` in settings
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Populate data via admin or shell
6. Access at `http://localhost:8000/ai-tutor/`

---

## 💡 Pro Tips

- Use specific class/subject/topic selection for better answers
- Questions in multiple languages are supported
- Check history to review previous explanations
- Follow-up suggestions lead to deeper learning
- Admin panel lets you manage all curriculum data

---

## 📞 Support Resources

- **Google AI Docs**: https://ai.google.dev/
- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/
- **Bootstrap Docs**: https://getbootstrap.com/

---

**Version**: 1.0 | **Status**: Ready for Production | **Last Updated**: Nov 2025
