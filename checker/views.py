# checker/views.py

from django.shortcuts import render
from django.http import JsonResponse
import requests

# 🔑 Your IPQualityScore API Key
IPQS_API_KEY = "ZPU8L1Fl8Eig5fLCoHy1pGwSr9LMZV9a"


def ip_checker_view(request):
    """
    Main view to check user's IP, location, risk, and user agent.
    """

    # 🌐 Get IP address
    ip_address = request.META.get("REMOTE_ADDR", "")
    user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")

    # 💻 Fallback for localhost
    if ip_address == "127.0.0.1":
        ip_address = requests.get("https://api.ipify.org").text

    # 📍 IP Location Info
    ip_info = {}
    try:
        r = requests.get(f"https://ipapi.co/{ip_address}/json/")
        ip_info = r.json() if r.status_code == 200 else {"error": "IP lookup failed"}
    except Exception as e:
        ip_info = {"error": f"IPAPI Error: {str(e)}"}

    # 🛡️ IPQS Risk Score
    ipqs_data = {}
    try:
        r = requests.get(
            f"https://ipqualityscore.com/api/json/ip/{IPQS_API_KEY}/{ip_address}"
        )
        ipqs_data = (
            r.json() if r.status_code == 200 else {"error": "IPQS lookup failed"}
        )
    except Exception as e:
        ipqs_data = {"error": f"IPQS Error: {str(e)}"}

    return render(
        request,
        "checker/ip_checker.html",
        {
            "ip_address": ip_address,
            "user_agent": user_agent,
            "ip_info": ip_info,
            "ipqs_data": ipqs_data,
        },
    )


from django.http import JsonResponse


def capture_packets(request):
    """
    Educational packet capture (simulated).
    Shows what kind of network activity can be observed and what it reveals.
    """

    packets = [
        {
            "packet": "192.168.1.10 → 8.8.8.8 DNS A query",
            "explanation": "Your device asked the DNS server (Google Public DNS) to resolve a domain name — reveals which websites you're trying to access.",
        },
        {
            "packet": "8.8.8.8 → 192.168.1.10 DNS response",
            "explanation": "The DNS server responded with the IP address — shows how third parties can trace your requests back to you.",
        },
        {
            "packet": "192.168.1.10 → 142.250.64.78 TCP SYN",
            "explanation": "Your device is initiating a TCP connection (e.g., to a website or server) — part of how web traffic starts, and can reveal destinations even under VPNs if DNS is not encrypted.",
        },
    ]

    return JsonResponse({"packets": packets})
