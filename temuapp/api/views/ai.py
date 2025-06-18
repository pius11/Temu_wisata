from rest_framework.decorators import api_view
from rest_framework.response import Response
from temuapp.models import TouristSpot, SpotImage
import requests
import json
import re

@api_view(['POST'])
def chat_ai(request):
    user_prompt = request.data.get('prompt', '').lower()

    wisata_keywords = ['wisata', 'tempat', 'tiket', 'alamat', 'fasilitas', 'spot', 'pariwisata', 'harga']
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
            if (
                spot.name.lower() in user_prompt
                or spot.kota.lower() in user_prompt
                or spot.kecamatan.lower() in user_prompt
                or spot.desa.lower() in user_prompt
                or spot.category.lower() in user_prompt
                or spot.fasilitas.lower() in user_prompt
                or spot.description.lower() in user_prompt
                or ("harga" in user_prompt and (
                    "termurah" in user_prompt and float(spot.price_min) == min([float(s.price_min) for s in spots])
                    or str(int(spot.price_min)) in user_prompt
                    or str(int(spot.price_max)) in user_prompt
                ))
            ):
                images = [img.file_name.url for img in spot.images.all()]
                found_spots.append(
                    f"Info {spot.name}: {spot.description}\nAlamat: {spot.address}\nHarga: {spot.price_min} - {spot.price_max}\nFasilitas: {spot.fasilitas}\nGambar: {images}"
                )
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
        "Jawablah pertanyaan user hanya berdasarkan data di atas jika menyangkut pariwisata. "
        "Jika pertanyaan user hanya basa-basi, balaslah seperti asisten ramah.\n"
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
        return Response({"response": ai_reply})
    except Exception as e:
        print("Error:", e)
        return Response({"response": "Maaf, terjadi kesalahan pada AI."})