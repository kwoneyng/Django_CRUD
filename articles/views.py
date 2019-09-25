from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment


# articles 의 메인 페이지, article list 를 보여 줌
def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)


# Variable Routing 으로 사용자가 보기를 원하는 페이지 pk 를 받아서
# Detail 페이지를 보여준다.
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)


# 데이터를 전달 받아서 article 생성
def create(request):
    # 만약 POST 요청일 경우 사용자 데이터 받아서 article 생성
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        article = Article(title=title, content=content, image=image)
        article.save()
        return redirect('articles:detail', article.pk)
    # 만약 GET 요청으로 들어오면 html 페이지 rendering
    else:
        return render(request, 'articles/create.html')


# 사용자로부터 받은 article_pk 값에 해당하는 article 을 삭제한다.
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        article.delete()
        return redirect('articles:index')
    else:
        return redirect('articles:detail', article_pk)


# /articles/5/update/
def update(request, article_pk):
    # POST /articles/5/update/ : 실제 Update 로직이 수행
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if image:
            article.image = image
        article.title = title
        article.content = content
        article.save()
        return redirect('articles:detail', article.pk)

    # GET /articles/5/update/ : Update 를 하기위한 Form 을 제공하는 페이지
    else:
        context = {'article': article}
        return render(request, 'articles/update.html', context)


def comments_create(request, article_pk):
    # article_pk 에 해당하는 article 에 새로운 comment 생성
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = Comment()
        comment.content = content
        comment.article = article
        # comment.article_id = article_pk
        comment.save()
        # 생성한 다음 article detail page 로 redirect
    return redirect('articles:detail', article_pk)


def comments_delete(request, article_pk, comment_pk):
    # comment_pk에 해당하는 댓글 삭제
    # POST 요청으로 들어올 때만

    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        # 댓글 삭제 후 detail 페이지로 이동
    return redirect('articles:detail', article_pk)