from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from temuapp.models import TouristSpot, SpotImage
from ..serializers.touristSpotsSerializ import TouristSpotSerializer
from ..serializers.spotImageSerializ import SpotImageSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rapidfuzz import fuzz
import requests
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_tourist_spot(request):
    data = request.data.copy()
    data['user_id'] = request.user.id

    # --- Cek kemiripan nama dan deskripsi dengan DB (fuzzy) ---
    input_name = data.get('name', '').strip()
    input_desc = data.get('description', '').strip()
    similar_name = None
    similar_desc = None
    threshold = 80  # bisa diatur sesuai kebutuhan

    # Ambil semua nama dan deskripsi dari DB
    spots = TouristSpot.objects.all()
    for spot in spots:
        # Fuzzy cek nama
        name_score = fuzz.token_sort_ratio(input_name.lower(), spot.name.lower())
        if name_score >= threshold:
            similar_name = spot.name
            break

    for spot in spots:
        # Fuzzy cek deskripsi
        desc_score = fuzz.token_sort_ratio(input_desc.lower(), spot.description.lower())
        if desc_score >= threshold:
            similar_desc = spot.name  # atau spot.description jika ingin tampilkan deskripsi
            break

    # Jika tidak ada yang mirip secara fuzzy, cek dengan Gemini (untuk nama & deskripsi)
    if not similar_name or not similar_desc:
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyBS0adeXniYkaaLnzCCZtxEilVAgv8FfPM"
        headers = {"Content-Type": "application/json"}

        # Cek nama
        if not similar_name:
            for spot in spots:
                prompt = (
                    f"Is the tourist spot name '{input_name}' the same or very similar to '{spot.name}'? "
                    "Consider translation, synonyms, and word order. Answer only 'yes' or 'no'."
                )
                data_gemini = {
                    "contents": [
                        {
                            "parts": [
                                {"text": prompt}
                            ]
                        }
                    ]
                }
                try:
                    resp = requests.post(api_url, headers=headers, data=json.dumps(data_gemini), timeout=10)
                    result = resp.json()
                    ai_reply = result['candidates'][0]['content']['parts'][0]['text']
                    if 'yes' in ai_reply.lower():
                        similar_name = spot.name
                        break
                except Exception as e:
                    pass  # bisa log error jika perlu

        # Cek deskripsi
        if not similar_desc:
            for spot in spots:
                prompt = (
                    f"Is the tourist spot description '{input_desc}' the same or very similar to '{spot.description}'? "
                    "Consider translation, synonyms, and word order. Answer only 'yes' or 'no'."
                )
                data_gemini = {
                    "contents": [
                        {
                            "parts": [
                                {"text": prompt}
                            ]
                        }
                    ]
                }
                try:
                    resp = requests.post(api_url, headers=headers, data=json.dumps(data_gemini), timeout=10)
                    result = resp.json()
                    ai_reply = result['candidates'][0]['content']['parts'][0]['text']
                    if 'yes' in ai_reply.lower():
                        similar_desc = spot.name  # atau spot.description
                        break
                except Exception as e:
                    pass

    # Jika ada kemiripan, kirim warning ke frontend
    if similar_name or similar_desc:
        return Response({
            "code": 4002,
            "message": "Similar tourist spot detected",
            "similar_name": similar_name,
            "similar_desc": similar_desc
        }, status=status.HTTP_200_OK)

    # --- Proses simpan jika tidak ada duplikat ---
    spot_serializer = TouristSpotSerializer(data=data)
    if spot_serializer.is_valid():
        spot = spot_serializer.save()
        images = request.FILES.getlist('images')
        image_objs = []
        for idx, img in enumerate(images):
            image_obj = SpotImage.objects.create(
                spot_id=spot,
                file_name=img,  # file_name sekarang adalah ImageField
                is_primary=(idx == 0)  # gambar pertama jadi primary
            )
            image_objs.append(image_obj)
        images_data = SpotImageSerializer(image_objs, many=True).data
        response_data = spot_serializer.data
        response_data['images'] = images_data
        return Response({"code": 2001, "message": "Tourist spot & images created", "data": response_data}, status=status.HTTP_201_CREATED)
    return Response({"code": 4001, "message": "Error in serializer", "errors": spot_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)