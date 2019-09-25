# Django ORM

## Create

### 기초설정

- Shell

  ```bash
  $ python manage.py shell
  ```

- import model

  ```python
  from articles.models import Article
  ```

### 데이터를 저장하는 3가지 방법

1. 첫번째 방식

   - ORM 을 쓰는 이유는? => DB 를 조작하는 것을 객체지향 프로그래밍 (클래스) 처럼 하기 위해서

     ```python
     article = Article()
     article # <Article: Article object (None)>
     article.title = 'First Article'
     article.content = 'Hello, article?'
     article.save()
     article # <Article: Article object (1)>
     ```

2. 두번째 방식

   - 함수에서 keyword 인자 넘기기 방식과 동일

     ```python
     >>> article = Article(title='Second', content='hihi')
     >>> article.save()
     >>> article
     <Article: Article object (2)>
     ```

3. 세번째 방식

   - `create()` 를 사용하면 쿼리셋 객체를 생성하고 저장하는 로직이 한번의 스텝

     ```python
     >>> Article.objects.create(title='third', content='Django! Good')
     <Article: Article object (3)>
     ```

4. 검증

   `full_clean()` 함수를 통해 저장하기 전 데이터 검증을 할 수 있다.

   ```python
   >>> article = Article()
   >>> article.title = 'Python is good'
   >>> article.full_clean()
   ```

---

## Read

- 객체 표현 변경

  ```python
  # artlcles/models.py
  class Article(models.Model):
      ...
      def __str__(self):
          return f'{self.id}번 글 - {self.title} : {self.content}'
  ```

- 모든객체

  ```python
  >>> Article.objects.all()
  <QuerySet [<Article: Article object (1)>, <Article: Article object (2)>, <Article: Article object (3)>, <Article: Article object (4)>]>
  ```

- DB에 저장된 글 중에서 title이 Second 인 글만 가지고 오기

  ```python
  >>> Article.objects.filter(title='Second')
  ```

- DB 에 저장된 글 중에서 title 이 Second 인 글 중에서 첫번째만 가지고 오기

  ```python
  >>> querySet = Article.objects.filter(title='Second')
  >>> querySet
  <QuerySet [<Article: ID : 2 - Second : hihi>, <Article: ID : 5 - Second : content>]>
  >>> querySet.first()
  <Article: ID : 2 - Second : hihi>
  ---
  >>> Article.objects.filter(title='Second').first()
  <Article: ID : 2 - Second : hihi>
  ```

- DB 에 저장된 글 중에서 pk 가 1인 글만 가지고 오기

  **PK 만 `get()` 으로 가지고 올 수 있다.**

  ```python
  >>> Article.objects.get(pk=1)
  <Article: ID : 1 - First article : Hello, article?>
  ```

- 오름차순

  ```python
  >>> articles = Article.objects.order_by('pk')
  >>> articles
  <QuerySet [<Article: ID : 1 - First article : Hello, article?>, <Article: ID : 2 - Second : hihi>, <Article: ID : 3 - third : Django! Good>, <Article: ID : 4 - title : >, <Article: ID : 5 - Second : content>]>
  ```

- 내림차순

  ```python
  >>> articles = Article.objects.order_by('-pk')
  >>> articles
  <QuerySet [<Article: ID : 5 - Second : content>, <Article: ID : 4 - title : >, <Article: ID : 3 - third : Django! Good>, <Article: ID : 2 - Second : hihi>, <Article: ID : 1 - First article : Hello, article?>]>
  ```

- 인덱스 접근이 가능하다!

  ```python
  >>> article = articles[2]
  >>> article
  <Article: ID : 3 - third : Django! Good>
  ---
  >>> articles = Article.objects.all()[1:3]
  >>> articles
  <QuerySet [<Article: ID : 2 - Second : hihi>, <Article: ID : 3 - third : Django! Good>]>
  ```

- LIKE - 문자열을 포함하고 있는 값을 가지고 옴

  장고 ORM 은 이름(title)과 필터(contains)를 더블 언더스코어로 구분합니다.

  ```python
  >>> articles = Article.objects.filter(title__contains='Sec')
  >>> articles
  <QuerySet [<Article: ID : 2 - Second : hihi>, <Article: ID : 5 - Second : content>]>
  ```

- startswith

  ```python
  >>> articles = Article.objects.filter(title__startswith='first')
  >>> articles
  <QuerySet [<Article: ID : 1 - First article : Hello, article?>]>
  ```

- endswith

  ```python
  >>> articles = Article.objects.filter(content__endswith='good')
  >>> articles
  <QuerySet [<Article: ID : 3 - third : Django! Good>]>
  ```

## Delete

article 인스턴스 호출 후 `.delete()` 함수를 실행한다.

```python
>>> article = Article.objects.get(pk=2)
>>> article.delete()
(1, {'articles.Article': 1})
```

## Update

article 인스턴스 호출 후 값 변경하여 `.save()` 함수 실행

```python
>>> article = Article.objects.get(pk=4)
>>> article.content
''
>>> article.content = 'new contents'
>>> article.save()
```

