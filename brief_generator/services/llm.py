import time
import json
from typing import Dict, Any
from openai import OpenAI
from django.conf import settings


class LLMService:
    def __init__(self):
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
        
        try:
            self.client = OpenAI(api_key=api_key)
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")
        
        self.model = "gpt-4o-mini"
        self.max_tokens = 500
        self.temperature = 0.5
    
    def generate_brief(
        self, 
        brand_name: str, 
        platform: str, 
        goal: str, 
        tone: str
    ) -> Dict[str, Any]:
        start_time = time.time()
        
        system_prompt = """You are an expert campaign strategist at Collabstr, a creator marketing platform. 
Generate concise, actionable campaign briefs for brand collaborations. 

Your output must be:
- Professional and strategic
- Tailored to the specified platform, goal, and tone
- Actionable with clear next steps
- Exactly 4-6 sentences for the brief
- Exactly 3 content angles
- Exactly 3 creator selection criteria

Always return valid JSON matching the required schema."""

        user_prompt = f"""Generate a campaign brief for {brand_name}.

Target Platform: {platform}
Goal: {goal}
Tone: {tone}

Return a JSON object with this exact structure:
{{
  "brief": "A 4-6 sentence campaign brief tailored to the inputs",
  "angles": ["First content angle", "Second content angle", "Third content angle"],
  "criteria": ["First selection criterion", "Second selection criterion", "Third selection criterion"]
}}

Provide exactly 3 angles and exactly 3 criteria."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            content = json.loads(response.choices[0].message.content)
            
            latency = time.time() - start_time
            tokens_used = response.usage.total_tokens
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            
            return {
                "success": True,
                "brief": content.get("brief", ""),
                "angles": content.get("angles", []),
                "criteria": content.get("criteria", []),
                "metrics": {
                    "latency_seconds": round(latency, 3),
                    "tokens_used": tokens_used,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "model": self.model
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metrics": {
                    "latency_seconds": round(time.time() - start_time, 3)
                }
            }

