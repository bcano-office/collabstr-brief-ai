import re
from typing import Tuple, Optional


PROFANITY_WORDS = {
    'damn', 'hell', 'crap', 'ass', 'bitch', 'shit', 'fuck', 'piss', 'bastard'
}

ALLOWED_PLATFORMS = ['Instagram', 'TikTok', 'UGC']
ALLOWED_GOALS = ['Awareness', 'Conversions', 'Content Assets']
ALLOWED_TONES = ['Professional', 'Friendly', 'Playful']


def validate_brand_name(brand_name: str) -> Tuple[bool, Optional[str]]:
    if not brand_name or not brand_name.strip():
        return False, "Brand name is required"
    
    brand_name = brand_name.strip()
    
    if len(brand_name) < 2:
        return False, "Brand name must be at least 2 characters"
    
    if len(brand_name) > 100:
        return False, "Brand name must be less than 100 characters"
    
    if not re.match(r'^[a-zA-Z0-9\s\-\']+$', brand_name):
        return False, "Brand name contains invalid characters"
    
    brand_lower = brand_name.lower()
    for word in PROFANITY_WORDS:
        if word in brand_lower:
            return False, "Brand name contains inappropriate content"
    
    return True, None


def validate_platform(platform: str) -> Tuple[bool, Optional[str]]:
    if platform not in ALLOWED_PLATFORMS:
        return False, f"Platform must be one of: {', '.join(ALLOWED_PLATFORMS)}"
    return True, None


def validate_goal(goal: str) -> Tuple[bool, Optional[str]]:
    if goal not in ALLOWED_GOALS:
        return False, f"Goal must be one of: {', '.join(ALLOWED_GOALS)}"
    return True, None


def validate_tone(tone: str) -> Tuple[bool, Optional[str]]:
    if tone not in ALLOWED_TONES:
        return False, f"Tone must be one of: {', '.join(ALLOWED_TONES)}"
    return True, None


def validate_all_inputs(
    brand_name: str,
    platform: str,
    goal: str,
    tone: str
) -> Tuple[bool, Optional[str]]:
    valid, error = validate_brand_name(brand_name)
    if not valid:
        return False, error
    
    valid, error = validate_platform(platform)
    if not valid:
        return False, error
    
    valid, error = validate_goal(goal)
    if not valid:
        return False, error
    
    valid, error = validate_tone(tone)
    if not valid:
        return False, error
    
    return True, None

