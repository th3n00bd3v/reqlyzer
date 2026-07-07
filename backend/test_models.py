from services.har_parser import HARParser
from services.request_analyzer import RequestAnalyzer
from services.security_analyzer import SecurityAnalyzer
from services.risk_scoring import RiskScorer

parser = HARParser("uploads/youtube.har")
requests = parser.parse()

request = requests[0]

request = RequestAnalyzer().analyze(request)
request = SecurityAnalyzer().analyze(request)
request = RiskScorer().analyze(request)

print(request.summary())

print("\n===== REQUEST ANALYSIS =====")
print(request.analysis)

print("\n===== SECURITY ANALYSIS =====")
print(request.security)

print("\n===== RISK ANALYSIS =====")
print(request.risk)