# Collabstr AI Brief Generator

An AI-powered tool that generates campaign briefs for influencer marketing campaigns. Enter your brand details and get a professional brief with content angles and creator selection criteria in seconds.

## Summary

This project generates tailored campaign briefs using OpenAI's GPT models. It takes brand name, target platform, campaign goal, and tone as inputs, then produces a structured brief with actionable content angles and creator criteria. Built with Django backend and a clean frontend matching Collabstr's design.

## Tech Stack

- **Backend:** Django 4.2, Python 3.8+
- **AI:** OpenAI GPT-4o-mini
- **Frontend:** HTML, CSS, JavaScript, jQuery
- **Database:** SQLite (default)
- **Other:** python-dotenv, django-cors-headers

## Quick Start

```bash
git clone https://github.com/bcano-office/collabstr-brief-ai
cd Collabstr-brief-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
python manage.py migrate
python manage.py runserver
```

Open `http://localhost:8000` in your browser.

## Live Demo
[Try this live Demo](https://collabstr-brief-ai-production.up.railway.app)

## Demo Video

[Watch the demo on Loom](https://www.loom.com/share/5e6d3a48ac594a9a8a77fc3997d0e5d0)

## Features

- AI-generated campaign briefs (4-6 sentences)
- 3 content angles per brief
- 3 creator selection criteria
- Input validation and rate limiting
- Token usage and latency tracking
- Clean, Collabstr-branded UI

## Prompt Design Choices

**System Prompt:** Establishes AI as expert campaign strategist with clear output requirements (4-6 sentences, exactly 3 angles, 3 criteria) and JSON format.

**User Prompt:** Provides structured inputs (brand, platform, goal, tone) with explicit JSON schema example to ensure consistent structure.

**Implementation:** Uses OpenAI's `response_format: {"type": "json_object"}` for deterministic JSON output. Temperature set to 0.5 for balanced consistency.

## Guardrails Implemented

- **Token Limits:** Max 500 tokens to control costs and response length
- **Temperature:** Fixed at 0.5 (meets ≤ 0.5 requirement) for deterministic outputs
- **Rate Limiting:** 10 requests/minute per IP (in-memory, use Redis in production)
- **Input Validation:** Brand name (2-100 chars, alphanumeric + spaces/hyphens/apostrophes, profanity filter), Platform/Goal/Tone (allowlist only)
- **Error Handling:** Comprehensive try-catch blocks with user-friendly messages and proper HTTP status codes

## Token and Latency Measurement

**Tokens:** Extracted from OpenAI response object (`response.usage.total_tokens`, `prompt_tokens`, `completion_tokens`) and included in every API response.

**Latency:** Measured using `time.time()` before and after LLM call, capturing network time, inference, and parsing. Both metrics rounded to 3 decimals and returned in JSON response for cost and performance visibility.


## To be improved

**Must Have for Production:**
1. Testing
2. Logging
3. Redis-based rate limiting
4. Proper error handling
5. Database models for tracking

**Should Have:**
6. Caching
7. API authentication
8. Better profanity filter
9. Configuration management
10. Monitoring

**Nice to Have:**
11. Async support
12. API documentation
13. CI/CD
14. Cost tracking
15. Frontend improvements
