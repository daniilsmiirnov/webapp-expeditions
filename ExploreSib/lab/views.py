from django.shortcuts import render
from django.http import HttpResponse

data = [
    {"id":'1',"place":"c. Карачино" ,"region":"Тюменская область","opener": "Ермак Тимофеевич", "year":1582, "expedition":"Первая русская экспедиция в Сибирь (1581-1585)"},
    {"id":'2',"place":"Кашлык" ,"region":"Тюменская область","opener": "Ермак Тимофеевич", "year":1582, "expedition":"Первая русская экспедиция в Сибирь (1581-1585)"},
    {"id":'3',"place":"Назым" ,"region":"ХМАО","opener": "Ермак Тимофеевич", "year":1583, "expedition":"Первая русская экспедиция в Сибирь (1581-1585)"},
    {"id":'4',"place":"Тюмень" ,"region":"Тюменская область","opener": "Василий Сюкин", "year":1586, "expedition":"Первая русская экспедиция в Сибирь"},
    {"id":'5',"place":"Красноярск" ,"region":"Красноярский край","opener": "Андрей Дубенский", "year":1628, "expedition":"Освоение Сибири Казаками"},
    {"id":'6',"place":"Тобольск" ,"region":"Тюменская область","opener": "Данила Чулков", "year":1587, "expedition":"Создание острогов воеводами по приказу Федора Ивановича"},
    {"id":'7',"place":"мыс Дежнева" ,"region":"Чукотский АО","opener": "Семен Дежнев", "year":1648, "expedition":"Чукотская экспедиция"},
    {"id":'8',"place":"о Диомида" ,"region":"Чукотский АО","opener": "Витус Беринг", "year":1728, "expedition":"Первая Камчатская экспедиция"}]

def GetPlace(request):
    
    return render(request, "main.html", {'data':data})
 
def about(request, id):
    city="Nothing, произошла ошибка"
    for n in data:
        if n['id']== str(id):
            city = n
    print("id",id,type(id))
    print("place:",city)
    return render(request, "about.html",{'data':city})
 
def filter(request):
    new_data=[]
    
    text = request.GET.get('text')
    field = request.GET.get('field')
    print(text,field)
    if (field):
        for n in data:
            if str(n[field])==text:
                print('check,',n[field],text)
                new_data.append(n)
        
    if new_data==[]:
        new_data=data
    return render(request, "main.html", {'data':new_data, 'word':text})