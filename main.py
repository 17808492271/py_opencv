from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models.models import session, Ht, Dk, User

app = FastAPI()
app.mount("/s", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates("static/ht")


# @app.get("/login")
# async def login(request: Request):
#     print(await request.form())


@app.post("/login")
async def login(request: Request):
    form_data = await request.form()  # 使用await来调用协程
    print(form_data.get("uid"))
    try:
        if form_data.get("uid") and form_data.get("password"):

            count = session.query(Ht).filter(Ht.uid == form_data.get("uid"),
                                             Ht.password == form_data.get("password")).count()
            if count > 0:
                return templates.TemplateResponse("ht.html", {"request": request})
            else:
                return "err"
    except:
        session.rollback()
    finally:
        session.close()


@app.get("/daydata")
async def daydata(request: Request):
    try:
        # daydata=session.query(Dk).filter(Dk.day==datetime.now().strftime("%Y-%m-%d")).all()
        daydatax = session.query(User).all()
        j = []
        for i in daydatax:
            c = {}
            c["name"] = i.name
            c["ename"] = i.ename
            for ii in i.dk:
                # print("ii.day", type(ii.day), type(datetime.now().strftime("%Y-%m-%d")))
                if str(ii.day) == str(datetime.now().strftime("%Y-%m-%d")):
                    # print("jr")
                    c["zt"] = ii.zt
                    c["date"] = ii.date
                    c["zt2"] = ii.zt2
                    c["date2"] = ii.date2
            j.append(c)

        return j
    except Exception as e:
        print("e", e)
        session.rollback()
    finally:
        session.close()

@app.get("/mothdata")
async def mothdata(request: Request):
    if int(datetime.now().strftime("%m")) % 2 == 0:
        min = (str(datetime.now().strftime("%Y-%m")) + '-01')
        max = (str(datetime.now().strftime("%Y-%m")) + '-30')
    else:
        min = (str(datetime.now().strftime("%Y-%m")) + '-01')
        max = (str(datetime.now().strftime("%Y-%m")) + '-31')
    try:
        # daydata=session.query(Dk).filter(Dk.day==datetime.now().strftime("%Y-%m-%d")).all()
        daydatax = session.query(User).all()
        j = []
        for i in daydatax:

            for ii in i.dk:
                print("ii.day", type(ii.day), datetime.now().strftime("%Y-%m"))
                if datetime.strptime(min, '%Y-%m-%d').date() <= ii.day <= datetime.strptime(max, '%Y-%m-%d').date():
                    print("jr",ii.__dict__)
                    c = {}
                    c["name"] = i.name
                    c["ename"] = i.ename
                    c["zt"] = ii.zt
                    c["date"] = ii.date
                    c["zt2"] = ii.zt2
                    c["date2"] = ii.date2
                    print("c",c)
                    j.append(c)
        print("j",j)
        return j
    except Exception as e:
        print("e", e)
        session.rollback()
    finally:
        session.close()

@app.get("/yggzdata")
async def yggzdata(request: Request):
    if int(datetime.now().strftime("%m")) % 2 == 0:
        min = (str(datetime.now().strftime("%Y-%m")) + '-01')
        max = (str(datetime.now().strftime("%Y-%m")) + '-30')
    else:
        min = (str(datetime.now().strftime("%Y-%m")) + '-01')
        max = (str(datetime.now().strftime("%Y-%m")) + '-31')
    try:
        # daydata=session.query(Dk).filter(Dk.day==datetime.now().strftime("%Y-%m-%d")).all()
        daydatax = session.query(User).all()
        j = []
        for i in daydatax:
            c = {}

            c["name"] = i.name
            c["ename"] = i.ename
            print("daydatax",daydatax)
            for ii in i.dk:
                cd = 0
                upday = 0

                zaotui = 0
                print("ii",i.name,ii.__dict__)
                upday=upday+1
                print("ii.day", type(ii.day),ii.day, datetime.now().strftime("%Y-%m"))

                print("max-min",max,min)
                if datetime.strptime(min, '%Y-%m-%d').date() <= ii.day <= datetime.strptime(max, '%Y-%m-%d').date():
                    print("jr",ii.day, datetime.strptime(min, '%Y-%m-%d').date())
                    if ii.zt=="上班迟到":
                        cd=cd+1
                    if ii.zt2=="":
                        zaotui=zaotui+1

            c["upday"] =upday
            c["cd"]=cd
            c["zaotui"]=zaotui
            c["sjmoney"]=upday*i.money
            c["koumoney"]=upday*i.money-(cd*50+zaotui*50)
            j.append(c)
        print("j",j)
        return j
    except Exception as e:
        print("e", e)
        session.rollback()
    finally:
        session.close()
