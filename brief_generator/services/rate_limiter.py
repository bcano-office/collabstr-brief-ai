from datetime import datetime, timedelta
from django.conf import settings
from collections import defaultdict


class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.max_requests = getattr(settings, 'RATE_LIMIT_REQUESTS_PER_MINUTE', 10)
        self.window_seconds = 60
    
    def is_allowed(self, identifier: str) -> bool:
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.window_seconds)
        
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > cutoff
        ]
        
        if len(self.requests[identifier]) >= self.max_requests:
            return False
        
        self.requests[identifier].append(now)
        return True
    
    def get_remaining(self, identifier: str) -> int:
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.window_seconds)
        
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > cutoff
        ]
        
        return max(0, self.max_requests - len(self.requests[identifier]))


rate_limiter = RateLimiter()

