from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from temuapp.models import TouristSpot, FavoriteSpot
import requests
import json
import re
from rapidfuzz import fuzz
import random
from django.db.models import Count
from langdetect import detect

def format_rupiah(value):
    try:
        value = int(float(value))
        return f"Rp{value:,.0f}".replace(",", ".")
    except Exception:
        return f"Rp{value}"

@api_view(['POST'])
@permission_classes([AllowAny])
def chat_ai(request):
    user_prompt = request.data.get('prompt', '').strip()
    # Deteksi bahasa prompt user
    try:
        detected_lang = detect(user_prompt)
    except Exception:
        detected_lang = 'id'  # fallback jika gagal deteksi

    lang = detected_lang  # gunakan hasil deteksi bahasa

    prompt_history = request.data.get('prompt_history', [])
    bot_history = request.data.get('bot_history', [])

    # Gabungkan history ke dalam context untuk Gemini
    history_text = ""
    for u, b in zip(prompt_history, bot_history):
        history_text += f"User: {u}\nTesa: {b}\n"
    if len(prompt_history) > len(bot_history):
        history_text += f"User: {prompt_history[-1]}\n"

    spots = TouristSpot.objects.filter(is_verified=True)
    spots_info = "\n".join([
        f"Nama: {spot.name}, Deskripsi: {spot.description}, Alamat: {spot.address}, "
        f"Harga: {format_rupiah(spot.price_min)}-{format_rupiah(spot.price_max)}, Fasilitas: {spot.fasilitas}"
        for spot in spots
    ])

    # Prompt universal: selalu balas dengan bahasa yang sama seperti pertanyaan user
    prompt = (
        "You are Tesa, a friendly and helpful virtual travel assistant.\n"
        "Here is the list of verified tourist spots in our database (the data is in Indonesian):\n"
        f"{spots_info}\n"
        "Here is the previous conversation between you and the user:\n"
        f"{history_text}\n"
        "Always reply in the same language as the user's latest question. "
        "If the user's question is in Japanese, reply in Japanese. If in Italian, reply in Italian. "
        "If in Indonesian, reply in Indonesian, and so on.\n"
        "If you use information from the database, always translate it to the user's language before replying.\n"
        "Now, answer the user's latest question based on the above data and the conversation history.\n"
        f"User's latest question: {user_prompt}"
    )

    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyBS0adeXniYkaaLnzCCZtxEilVAgv8FfPM"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    try:
        resp = requests.post(api_url, headers=headers, data=json.dumps(data), timeout=10)
        result = resp.json()
        ai_reply = result['candidates'][0]['content']['parts'][0]['text']
        return Response({"response": ai_reply})
    except Exception as e:
        print("Error:", e)
        return Response({"response": "Maaf, terjadi kesalahan pada AI."})