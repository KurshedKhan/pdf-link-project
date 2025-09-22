
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import fitz
import os

def index(request):
    context = {}
    if request.method == 'POST':
        files = request.FILES.getlist('pdf_files')
        link = request.POST.get('link')
        output_files = []

        for i, f in enumerate(files):
            fs = FileSystemStorage()
            filename = fs.save(f.name, f)
            input_path = fs.path(filename)

            doc = fitz.open(input_path)
            for page in doc:
                rect = page.rect
                page.insert_link({
                    "kind": fitz.LINK_URI,
                    "from": rect,
                    "uri": link
                })

            output_name = f"output_{i+1}_{f.name}"
            output_path = os.path.join("media", output_name)
            doc.save(output_path)
            doc.close()

            output_files.append(output_name)

        context['output_files'] = output_files

    return render(request, 'index.html', context)
