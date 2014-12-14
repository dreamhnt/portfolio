동아리 홈페이지
===========
2013년도 말에 학기 생활중 개발한 동아리 홈페이지입니다.

JSON으로 serialize하는걸 구현하는 부분에서 제일 고생했습니다.

페이스북 django그룹에 질문을 통해 해결을 하였는데 view.py와 model.py 모두 serialize를 위해 함수를 정의해주어야 했습니다.

처음으로 웹 프레임워크를 사용한 것이 django 였고, python도 같이 공부하게 되었는데 정말 재미있게 개발을 했으며
자연스럽게 MVC 개념도 알게 되었습니다.

처음이라 고생을 많이 했지만 결과적으로 짧은 코드로 완성된 것에 놀라웠습니다.

```python
--view.py--

class MyJSONEncoder(DjangoJSONEncoder):		# FileFields 를 json에맞게 Encoder
    def default(self, obj):
        if isinstance(obj, FieldFile):
            return obj.url
        return super(MyJSONEncoder, self).default(obj)

def toJSON(objs, status=200):			#model 객체를 JSON serialize
	j = json.dumps(
        [picture.serialize() for picture in objs],
        cls = MyJSONEncoder,
        ensure_ascii = False)
	return HttpResponse(j, status=status, content_type='application/json; charset=utf-8')
```
```python
--model.py--
class Article(models.Model):
	content = models.CharField(max_length=200)
	written_date = models.DateTimeField('date written')
	def __str__(self):
		return self.content
	def serialize(self):
		data = {
			'content':self.content,
			'written_date':self.written_date
		}
		return data
```


![로그인화면](http://dl.dropbox.com/s/i67qjmxjdzzthd2/login.png)

![화면](http://dl.dropbox.com/s/8gylk62s70mj8yq/pic.png)

![음악](http://dl.dropbox.com/s/2gz8qfzepcxj1o2/mu.png)

![타임라인](http://dl.dropbox.com/s/5ha0aqrksqy64qe/one.png)
