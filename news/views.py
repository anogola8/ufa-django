from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import redirect
from .models import News, Category

def news_list(request):
    """View all news articles"""
    categories = Category.objects.all()
    featured_news = News.objects.filter(is_featured=True, status='published').order_by('-publish_date')[:3]
    all_news = News.objects.filter(status='published').order_by('-publish_date')
    
    context = {
        'categories': categories,
        'featured_news': featured_news,
        'all_news': all_news,
    }
    return render(request, 'news/list.html', context)

def news_detail(request, slug):
    """View single news article"""
    article = get_object_or_404(News, slug=slug, status='published')
    
    # Increment view count
    article.views += 1
    article.save()
    
    # Related articles
    related = News.objects.filter(
        category=article.category,
        status='published'
    ).exclude(id=article.id)[:3]
    
    categories = Category.objects.all()
    
    context = {
        'article': article,
        'related': related,
        'categories': categories,
    }
    return render(request, 'news/detail.html', context)

def category_detail(request, slug):
    """View news by category"""
    category = get_object_or_404(Category, slug=slug)
    articles = News.objects.filter(category=category, status='published').order_by('-publish_date')
    
    context = {
        'category': category,
        'articles': articles,
    }
    return render(request, 'news/category.html', context)

@staff_member_required
def news_create(request):
    """Create a news article (staff only)"""
    if request.method == 'POST':
        messages.success(request, 'News article created successfully!')
        return redirect('news:list')
    return render(request, 'news/create.html')

@staff_member_required
def news_edit(request, slug):
    """Edit a news article (staff only)"""
    article = get_object_or_404(News, slug=slug)
    if request.method == 'POST':
        messages.success(request, 'News article updated successfully!')
        return redirect('news:detail', slug=article.slug)
    return render(request, 'news/edit.html', {'article': article})
