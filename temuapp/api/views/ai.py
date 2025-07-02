from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from temuapp.models import TouristSpot, SpotImage
# from ..serializers.aiserializ import ChatSessionSerializer
import requests
import json
import re
from rapidfuzz import fuzz  # Tambahkan ini
import random

@api_view(['POST'])
@permission_classes([AllowAny])
def chat_ai(request):
    user_prompt = request.data.get('prompt', '').lower()

    wisata_keywords = ['wisata', 'tempat', 'tiket', 'alamat', 'fasilitas', 'spot', 'pariwisata', 'harga', 'rekomendasi']
    if any(k in user_prompt for k in wisata_keywords):
        spots = TouristSpot.objects.all()
        found_spots = []

        # Cek jika ada permintaan rentang harga
        harga_range = re.findall(r'(\d{4,})', user_prompt)
        if "harga" in user_prompt and len(harga_range) >= 2:
            harga_min = int(harga_range[0])
            harga_max = int(harga_range[1])
            spots = spots.filter(price_min__gte=harga_min, price_max__lte=harga_max)

        for spot in spots:
            # NLP string matching dengan rapidfuzz
            max_score = max([
                fuzz.partial_ratio(user_prompt, str(spot.name).lower()),
                fuzz.partial_ratio(user_prompt, str(spot.kota).lower()),
                fuzz.partial_ratio(user_prompt, str(spot.kecamatan).lower()),
                fuzz.partial_ratio(user_prompt, str(spot.desa).lower()),
                fuzz.partial_ratio(user_prompt, str(spot.category).lower()),
                fuzz.partial_ratio(user_prompt, str(spot.fasilitas).lower()),
                fuzz.partial_ratio(user_prompt, str(spot.description).lower()),
            ])
            # Ambil spot jika kemiripan di atas threshold (misal 60)
            if max_score > 60 or (
                "harga" in user_prompt and (
                    "termurah" in user_prompt and float(spot.price_min) == min([float(s.price_min) for s in spots])
                    or str(int(spot.price_min)) in user_prompt
                    or str(int(spot.price_max)) in user_prompt
                )
            ):
                found_spots.append(
                    f"{spot.name} adalah {spot.description}. Lokasinya di {spot.address}. "
                    f"Harga tiket masuk: {spot.price_min} - {spot.price_max}. "
                    f"Fasilitas yang tersedia: {spot.fasilitas}."
                )
        # Jika tidak ada spot yang cocok, cek apakah user minta rekomendasi
        if not found_spots and "rekomendasi" in user_prompt:
            all_spots = list(spots)
            if all_spots:
                rekomendasi = random.sample(all_spots, min(3, len(all_spots)))
                found_spots = [+
                    f"{spot.name} adalah {spot.description}. Lokasinya di {spot.address}. "
                    f"Harga tiket masuk: {spot.price_min} - {spot.price_max}. "
                    f"Fasilitas yang tersedia: {spot.fasilitas}."
                    for spot in rekomendasi
                ]
                return Response({"response": "Berikut rekomendasi tempat wisata untuk Anda:\n\n" + "\n\n".join(found_spots)})
        if found_spots:
            return Response({"response": "\n\n".join(found_spots)})
        return Response({"response": "Maaf, saya tidak menemukan destinasi yang dimaksud di database kami."})

    # Ambil data pariwisata dari database untuk context
    spots = TouristSpot.objects.all() # batasi agar prompt tidak terlalu panjang
    spots_info = ""
    for spot in spots:
        spots_info += f"Nama: {spot.name}, Deskripsi: {spot.description}, Alamat: {spot.address}, Harga: {spot.price_min}-{spot.price_max}, Fasilitas: {spot.fasilitas}\n"

    # Prompt untuk Gemini dengan context database
    prompt = (
        "Berikut adalah data tempat wisata di database kami:\n"
        f"{spots_info}\n"
        "Jawablah pertanyaan user hanya berdasarkan data di atas. "
        "Buatlah jawaban yang natural, ramah, dan mudah dipahami seperti asisten manusia. "
        "Jika pertanyaan user tidak berkaitan dengan data di atas, balaslah dengan sopan.\n"
        f"Pertanyaan user: {user_prompt}"
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

        # # Dapatkan/make session (misal, dari user id dan session id di request)
        # session, _ = ChatSession.objects.get_or_create(user=request.user)  # atau pakai session_id dari request

        # # Simpan prompt user
        # ChatMessage.objects.create(session=session, sender='user', message=user_prompt)
        # # Simpan response AI
        # ChatMessage.objects.create(session=session, sender='ai', message=ai_reply)

        return Response({"response": ai_reply})
    except Exception as e:
        print("Error:", e)
        return Response({"response": "Maaf, terjadi kesalahan pada AI."})

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_chat_history(request, session_id):
#     try:
#         session = ChatSession.objects.get(id=session_id, user=request.user)
#     except ChatSession.DoesNotExist:
#         return Response({"message": "Session not found"}, status=404)
#     serializer = ChatSessionSerializer(session)
#     return Response(serializer.data)