from django.shortcuts import render, redirect
import json
from django.http import JsonResponse, HttpResponseForbidden
from newspaper import Article
import requests
from .models import *
from django.core.paginator import Paginator
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize
from collections import Counter

tokenizer = AutoTokenizer.from_pretrained("bias_model")
model = AutoModelForSequenceClassification.from_pretrained("bias_model")
model.eval()

def predict_bias(text):
    sentences = sent_tokenize(text)
    predictions = []

    for sentence in sentences:
        input = tokenizer.encode_plus(
            sentence,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding="max_length"
        )

        with torch.no_grad():
            output = model(**input)
            prediction = torch.argmax(output.logits, dim=1).item()
            predictions.append(prediction)

    final_prediction = Counter(predictions).most_common(1)[0][0] #most_common returns a list of tuples (label, frequency) in descending order
    labels = {
        0: "Neutral",
        1: "Nationalistic Bias",
        2: "Sensationalism/Emotional Language",
        3: "Religious/Cultural Bias"
    }
    return labels[final_prediction]



#####################VIEWS#####################
def index(request):
    return render(request, "biasdetector/index.html")

def detect_view(request):
    return render(request, "biasdetector/detect.html", {
        'detect': True
    })

def about_us(request):
    return render(request, "biasdetector/about.html")

def howitworks(request):
    return render(request, "biasdetector/howitworks.html")

def feedback(request):
    article_url = request.session.get('url')
    bias = request.session.get('bias')

    if not article_url or not bias:
        return HttpResponseForbidden("Feedback unavailable. Analyze an article first.")

    if request.method == "POST":
        agree = request.POST.get("agree") == "agree"
        comments = request.POST.get("comments", "")

        Feedback.objects.create(
            article_url=article_url,
            bias_label=bias,
            agree=agree,
            comments=comments
        )

        del request.session['feedback_url']
        del request.session['feedback_bias']

        return redirect("index")

    return render(request, "feedback.html", {
        "article_url": article_url,
        "bias": bias
    })

def view_feedback(request):
    # if not request.user.is_superuser:
    #     return HttpResponseForbidden("You are not allowed to view this page.")

    feedback_list = Feedback.objects.all().order_by('-id')
    paginator = Paginator(feedback_list, 5)  # 5 feedback entries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "racetracker/view_feedback.html", {
        "page_obj": page_obj
    })

#############API VIEWS#############
def analyze_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required.'}, status=405)

    try:
        data = json.loads(request.body)
        url = data.get('article_url')
    except:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)       

    if not url:
        return JsonResponse({'error': 'No URL provided.'}, status=400)

    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code >= 400:
            return JsonResponse({'error': 'URL is unreachable or returned an error status.'}, status=400)

        article = Article(url)
        article.download()
        article.parse()

        if not article.text.strip():
            return JsonResponse({'error': 'No article content found at the provided URL.'}, status=400)
        
        predicted_bias = predict_bias(article.text)

        request.session['url'] = url
        request.session['bias'] = predicted_bias

        return JsonResponse({
            'title': article.title,
            'text': article.text,
            'url': url,
            'bias': predicted_bias
        })
    except requests.exceptions.RequestException:
        return JsonResponse({'error': 'The URL appears to be invalid or unreachable.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Failed to analyze article: {str(e)}'}, status=500)