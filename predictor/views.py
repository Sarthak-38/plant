import os
from django.shortcuts import render
from django.conf import settings
from .ml_model import predict_image

def index(request):
    prediction = None

    if request.method == "POST":
        image = request.FILES.get("image")

        if image:
            file_path = os.path.join(settings.MEDIA_ROOT, image.name)

            with open(file_path, "wb+") as f:
                for chunk in image.chunks():
                    f.write(chunk)

            prediction = predict_image(file_path)

    return render(request, "index.html", {"prediction": prediction})