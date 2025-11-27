import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from .services.llm import LLMService
from .services.validation import validate_all_inputs
from .services.rate_limiter import rate_limiter


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@require_http_methods(["GET"])
def index(request):
    return render(request, 'brief_generator/index.html')


@csrf_exempt
@require_http_methods(["POST"])
def generate_brief(request):
    client_ip = get_client_ip(request)
    if not rate_limiter.is_allowed(client_ip):
        return JsonResponse({
            "success": False,
            "error": "Rate limit exceeded. Please try again later.",
            "retry_after_seconds": 60
        }, status=429)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "error": "Invalid JSON in request body"
        }, status=400)
    
    brand_name = data.get('brand_name', '').strip()
    platform = data.get('platform', '').strip()
    goal = data.get('goal', '').strip()
    tone = data.get('tone', '').strip()
    
    is_valid, error_message = validate_all_inputs(
        brand_name, platform, goal, tone
    )
    
    if not is_valid:
        return JsonResponse({
            "success": False,
            "error": error_message
        }, status=400)
    
    try:
        llm_service = LLMService()
    except ValueError as e:
        return JsonResponse({
            "success": False,
            "error": "OpenAI API key is not configured. Please set OPENAI_API_KEY in your environment variables."
        }, status=500)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": f"Failed to initialize AI service: {str(e)}"
        }, status=500)
    
    result = llm_service.generate_brief(
        brand_name=brand_name,
        platform=platform,
        goal=goal,
        tone=tone
    )
    
    if not result.get("success"):
        error_msg = result.get("error", "Failed to generate brief")
        
        if "api key" in error_msg.lower() or "authentication" in error_msg.lower():
            error_msg = "Invalid OpenAI API key. Please check your OPENAI_API_KEY configuration."
        elif "rate limit" in error_msg.lower():
            error_msg = "OpenAI API rate limit exceeded. Please try again in a moment."
        
        return JsonResponse({
            "success": False,
            "error": error_msg
        }, status=500)
    
    return JsonResponse({
        "success": True,
        "brief": result["brief"],
        "angles": result["angles"],
        "criteria": result["criteria"],
        "metrics": result["metrics"]
    })

