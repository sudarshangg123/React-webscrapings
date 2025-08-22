import os
import urllib.parse
import urllib.robotparser as robotparser
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ScrapedItem
from .serializers import ScrapedItemSerializer
import requests
from bs4 import BeautifulSoup

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth_verify(request):
    """Verify frontend Google ID token, create or get user, return JWT tokens."""
    token = request.data.get('id_token')
    if not token:
        return Response({'detail': 'Missing id_token'}, status=400)
    try:
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), GOOGLE_CLIENT_ID)
        email = idinfo.get('email')
        name = idinfo.get('name') or email.split('@')[0]
        user, _ = User.objects.get_or_create(username=email, defaults={'first_name': name, 'email': email})
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {'email': user.email, 'username': user.username}
        })
    except Exception as e:
        return Response({'detail': 'Invalid token', 'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def scrape_url(request):
    """Scrape a provided URL and store simplified items. Respects robots.txt."""
    target = request.data.get('url')
    if not target:
        return Response({'detail': 'Missing url'}, status=400)

    parsed = urllib.parse.urlparse(target)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
        if not rp.can_fetch('*', target):
            return Response({'detail': 'Scraping disallowed by robots.txt'}, status=403)
    except Exception:
        # robots.txt not reachable — proceed but be cautious
        pass

    headers = {'User-Agent': 'ReactScraperAssignment/1.0 (+https://example.com)'}
    resp = requests.get(target, headers=headers, timeout=10)
    if resp.status_code != 200:
        return Response({'detail': 'Failed to fetch target', 'status_code': resp.status_code}, status=400)

    soup = BeautifulSoup(resp.text, 'html.parser')
    # Example: find common headline tags
    candidates = soup.select('h1, h2, h3')[:20]
    created_items = []
    for tag in candidates:
        title = tag.get_text(strip=True)
        if not title:
            continue
        a = tag.find('a')
        link = a['href'] if a and a.has_attr('href') else target
        # normalize relative links
        if link and link.startswith('/'):
            link = f"{parsed.scheme}://{parsed.netloc}{link}"
        item = ScrapedItem.objects.create(title=title, url=link, source=parsed.netloc)
        created_items.append(item)

    serializer = ScrapedItemSerializer(created_items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_items(request):
    qs = ScrapedItem.objects.all().order_by('-scraped_at')[:200]
    serializer = ScrapedItemSerializer(qs, many=True)
    return Response(serializer.data)
