from pygame import mixer
import speech_recognition as sr
import pyttsx3 
import pyjokes
import boto3
import pyglet
import winsound
import datetime
import pywhatkit
import datetime
import time
import os
from PIL import Image
import random
import wikipedia
import smtplib, ssl
from mutagen.mp3 import MP3
import requests, json
from bs4 import BeautifulSoup
import geocoder
from geopy.geocoders import Nominatim
import webbrowser
import pymongo
from getmac import get_mac_address as gma
import cv2
import face_recognition
import numpy as np
import smtplib
import datetime


r = sr.Recognizer()
task={}
filename1=[]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
client = pymongo.MongoClient("mongodb+srv://karan:123@cluster0.gfuxd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client["LocationDatabase"]

table = database["Location"]

def location():
    g = geocoder.ip('me')

    Latitude = str(g.latlng[0])
    
    Longitude = str(g.latlng[1])
     
    geolocator = Nominatim(user_agent="geoapiExercises")

    location = geolocator.reverse(Latitude+","+Longitude)
    
    mydict={"_id":''.join(i for i in gma() if not i.isdigit()).replace(":",""),"location":str(location)}
    try:
        x = table.insert_one(mydict)
    except:
        myquery = { "_id": gma() }
        newvalues = {  "$set": { "location": str(location) } }
        table.update_one(myquery, newvalues)

    

def weather(city):
    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    greetings=["Hello","Hey","Hi","Greetings","Namaste"]
    timewait=speak(greetings[random.randint(0,4)])
    time.sleep(timewait)
    timewait=speak("In "+location)
    time.sleep(timewait)
    d = datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M")
    timewait=speak("It is "+str(d.strftime("%I")))
    time.sleep(timewait-0.1)
    timewait=speak(str(d.strftime("%M")),"op")
    time.sleep(timewait)
    if(datetime.datetime.now().hour>12):
        timewait=speak("P M","ui")
        time.sleep(timewait-0.1)
    else:
        timewait=speak("A M")
        time.sleep(timewait)
    timewait=speak("The Temperature is "+weather+"Degree Celcius","oi")
    time.sleep(timewait)
    
def weather_main():
    g = geocoder.ip('me')

    Latitude = str(g.latlng[0])
    
    Longitude = str(g.latlng[1])
     
    geolocator = Nominatim(user_agent="geoapiExercises")

    location = geolocator.reverse(Latitude+","+Longitude)

    address = location.raw['address']

    city_name=address['city']

    api_key = "da1f94efa4d6cefb2ed01470906d553f"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
     
    response = requests.get(complete_url)

    x = response.json()

    city_name = city_name+" weather"

    weather(city_name)

    if x["cod"] != "404":

        y = x["main"]

        current_temperature = y["temp"]

        current_humidity = y["humidity"]

        z = x["weather"]

        weather_description = z[0]["description"]

        timewait=speak("Humidity is " +str(current_humidity) + "percentage","op")
        time.sleep(timewait)
        timewait=speak("It's "+str(weather_description)+" Today","ooP")
        time.sleep(timewait)
        if(("thunderstorm" in str(weather_description)) or ("rain" in str(weather_description)) or ("shower" in str(weather_description))):
            timewait=speak("You Might Need An Umbrella!")
            time.sleep(timewait)
        elif(("clear" in str(weather_description)) or ("sunny" in str(weather_description))):
            timewait=speak("We Have A Clear Sky!")
            time.sleep(timewait)
        elif("cloudy" in str(weather_description)):
            timewait=speak("The Sky Might Be Cloudy!")
            time.sleep(timewait)
            
        timewait=speak("Have a Nice Day")
        time.sleep(timewait+1)
name="User"   
def speak(text,tp="1",voice="Salli"):
    response = polly_client.synthesize_speech(VoiceId=voice,
                                          OutputFormat='mp3',
                                          Text=text)
    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    file = open('speech'+date_string+tp+'.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()
    filename1.append('speech'+date_string+tp+'.mp3')
    if(len(filename1)>10):       
        for i in range(0,5):
            os.remove(filename1[i])
            filename1.pop(i)
    audio = MP3('speech'+date_string+tp+'.mp3')
    
    mixer.init()
    mixer.music.load('speech'+date_string+tp+'.mp3')
    mixer.music.play()
    return audio.info.length

polly_client = boto3.Session(
    aws_access_key_id="AKIASBGML26WXFHTJR5M",
    aws_secret_access_key="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",
    region_name='us-west-2').client('polly')


try:
    for file in os.listdir("./"):
        filename = os.fsdecode(file)
        if filename.endswith(".jpg"):
            imgloaded=face_recognition.load_image_file(filename)
            imgloaded=cv2.cvtColor(imgloaded,cv2.COLOR_BGR2RGB)
            camera = cv2.VideoCapture(0)
            return_value, image = camera.read()
            cv2.imwrite(os.path.join('./' , 'testimage.jpg'), image)
            imgtest=face_recognition.load_image_file('./testimage.jpg')
            imgtest=cv2.cvtColor(imgtest,cv2.COLOR_BGR2RGB)
            faceloc=face_recognition.face_locations(imgloaded)[0]
            encodeloaded=face_recognition.face_encodings(imgloaded)[0]
            cv2.rectangle(imgloaded,(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]),(255,0,255),2)
            faceloctest=face_recognition.face_locations(imgtest)[0]
            encodetest=face_recognition.face_encodings(imgtest)[0]
            cv2.rectangle(imgtest,(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]),(255,0,255),2)
            results=face_recognition.compare_faces([encodeloaded],encodetest)
            if(results[0]):
                name=filename.replace(".jpg","")
                break
except:
    timewait=speak("What's Your Name? ")
    time.sleep(timewait)
    print("Listening")
    with sr.Microphone() as source2:
        r.adjust_for_ambient_noise(source2, duration=0.1)
        audio2 = r.listen(source2)
        name = r.recognize_google(audio2)

    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    cv2.imwrite(os.path.join('./' , name+'.jpg'), image)

onlyonce=0
while(1):
    try:
        d = datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M")
        if(str(d.strftime("%M"))=='14' and onlyonce==0):
            onlyonce+=1
            location()
        if(onlyonce>0):
            if(str(d.strftime("%M"))!='14'):
                onlyonce=0
        with sr.Microphone() as source2:            
            print("Listening")
            
            r.adjust_for_ambient_noise(source2, duration=1)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()

            print(MyText.title())
            
            if("joke" in MyText):
                My_joke = pyjokes.get_joke(language="en", category="all")
                print(My_joke)
                time1 = speak(My_joke,"joke")
                time.sleep(int(time1))
            elif(("hello" in MyText) or ("update" in MyText) or ("hi" in MyText) or ("hey" in MyText)):
                speak(name,"iu")
                time.sleep(1)
                weather_main()
            elif("time" in MyText):
                speak(name,"iu")
                time.sleep(1)
                speak("The Time Is","O")
                time.sleep(0.7)
                speak(str(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M").strftime("%I")))
                time.sleep(0.5)
                speak(str(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M").strftime("%M")),"o")
                time.sleep(0.8)
                if(datetime.datetime.now().hour>12):
                    timewait=speak("P M","ui")
                    time.sleep(timewait-0.1)
                else:
                    timewait=speak("A M")
                    time.sleep(timewait)
            elif("date" in MyText):
                speak(name,"iu")
                time.sleep(1)
                x = datetime.datetime.now()
                speak("It's "+str(x.strftime("%A")))
                time.sleep(0.85)
                speak(str(x.strftime("%d")).replace("0",""),"i")
                time.sleep(0.8)
                speak(x.strftime("%B"),"P")
                time.sleep(0.8)
                speak(str(x.year),"OP")
                time.sleep(0.8)
            
            elif("mail" in MyText):
                port = 587  
                smtp_server = "smtp.gmail.com"
                sender_email = "techtrends288@gmail.com"
                speak("What's The Receiver's Mail I D")
                
                receiver_email = input("Receiver's Mail ID:")
                password = input("Receiver's Your Password: ")
                speak("What's The Subject?")
                time.sleep(2)
                print("Speak Now")
                r.adjust_for_ambient_noise(source2, duration=0.1)
                audio2 = r.listen(source2)
                SUBJECT = r.recognize_google(audio2)
                speak("What Should The Message Say")
                time.sleep(2)
                print("Speak Now")
                r.adjust_for_ambient_noise(source2, duration=0.1)
                audio2 = r.listen(source2)
                message = r.recognize_google(audio2)
                
                context = ssl.create_default_context()
                with smtplib.SMTP(smtp_server, port) as server:
                    server.ehlo()  
                    server.starttls(context=context)
                    server.ehlo()  
                    server.login(sender_email, password)
                    
                    message = 'Subject: {}\n\n{}'.format(SUBJECT, message)
                    server.sendmail(sender_email, receiver_email, message)
                speak("Message On Its Way!")
                print("Message Sent!")
            elif("whatsapp" and "message" in MyText):
                if("to" in MyText):
                    split_sentence = MyText.split(' ')
                    name=split_sentence[-1]
                    speak("What's "+name+"'s Phone Number?    ")
                else:
                    speak("What's Their Phone Number?")
                time.sleep(2)

                print("Speak Now")
                r.adjust_for_ambient_noise(source2, duration=0.1)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                number = MyText.lower().replace(" ", "")
                speak("What's The Message? ")
                time.sleep(2)
                print("Speak Now")
                r.adjust_for_ambient_noise(source2, duration=0.1)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                msg = MyText.lower()
                

                try:
                    pywhatkit.sendwhatmsg("+91"+number,msg,datetime.datetime.now().hour,datetime.datetime.now().minute+1)
                except:
                    pywhatkit.sendwhatmsg("+91"+number,msg,datetime.datetime.now().hour,datetime.datetime.now().minute+2)
                speak("Message On Its Way!")
                print("Message Sent!")
            
            elif("random" and "number" in MyText):
                speak(name,"iu")
                time.sleep(1)
                if("from" and "to" in MyText):
                    split_sentence = MyText.split(' ')
                    fromIndex=split_sentence.index('from')
                    toIndex=split_sentence.index('to')
                    speak("Here's Your Random Number "+str(random.randint(int(split_sentence[int(fromIndex)+1]),int(split_sentence[int(toIndex)+1]))))

                else:
                    speak("Here's Your Random Number "+str(random.randint(0,100)))
                time.sleep(3)
            elif(("note"  in MyText) or( "write"  in MyText) or( "homework"  in MyText)):
                speak("What's The Content? ")
                time.sleep(2)
                print("Speak Now")
                
                r.adjust_for_ambient_noise(source2, duration=0.1)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                msg = MyText.lower()
                
                pywhatkit.text_to_handwriting(msg)
                
                img_path = "pywhatkit.png"
                image1 = Image.open(r'pywhatkit.png')
                im1 = image1.convert('RGB')

                im1.save(r'HandWritten.pdf')
                speak("Your HomeWork Is Generated As Handwritten dot p n g")
                time.sleep(3)
            elif(("do"  in MyText) or( "what"  in MyText) or ("where" in MyText) or ("who" in MyText)):
                
                split_sentence = MyText.split(' ')
                
                if((split_sentence[-2]!="know") or (split_sentence[-2]!="is") or (split_sentence[-2]!="are") or (split_sentence[-2]!="an") or (split_sentence[-2]!="a") or (split_sentence[-2]!="the")):
                    print(wikipedia.summary(split_sentence[-2]+" "+split_sentence[-1],sentences=2))
                    time1=speak(wikipedia.summary(split_sentence[-2]+" "+split_sentence[-1],sentences=2))
                else:
                    print(wikipedia.summary(split_sentence[-1],sentences=2))
                    time1=speak(wikipedia.summary(split_sentence[-1],sentences=2))
                time.sleep(time1)
                
            elif(("create" in MyText) and  ("list" in MyText)):
                speak(name,"iu")
                time.sleep(1)
                split_sentence = MyText.split(' ')
                dict["new key"]=[]
                task[split_sentence[split_sentence.index("list")-1]]=[]
                nameoflist=split_sentence[split_sentence.index("list")-1]
                speak("What Items Do You Want Me To Add?")
                time.sleep(2)
                speak("Please! Add One Item At a time!","p")
                time.sleep(4)
                
                while ("end" not in MyText):
                    print("Say Task")
                    time.sleep(1)
                    r.adjust_for_ambient_noise(source2, duration=0.1)
                    audio2 = r.listen(source2)
                    MyText = r.recognize_google(audio2)
                    if("end" in MyText):
                        speak("List Updated")
                    else:
                        task[nameoflist].append(MyText)
                        speak("Next Item?")
                        time.sleep(2)
                print(task)
            elif(("show" in MyText) and  ("list" in MyText)):
                speak(name,"iu")
                time.sleep(1)
                if(task=={}):
                    speak("You Currently Have No Items In The List")
                else:
                    speak("You Have"+str(len(task))+" Items In List")
                    time.sleep(2)
                    for key in task:
                        speak("In "+key+" You Have","o")
                        time.sleep(2)
                        for keys in task[key]:
                            
                            speak(keys,"oo")
                            time.sleep(1)
            elif("weather" in MyText):
                speak(name,"iu")
                time.sleep(1)
                weather_main()
            elif(("open" in MyText)):
                split_sentence = MyText.split(' ')
                url=""
                for i in split_sentence:
                    if(i=="open"):
                        continue
                    url+=i
                webbrowser.open_new(url)   
            elif("search" in MyText):
                split_sentence = MyText.split(' ')
                url=""
                for i in split_sentence:
                    if(i=="search"):
                        continue
                    url+=i+"+"
                
                webbrowser.open("https://www.google.com/search?q={query}".format(query=url))
            elif(("siri" in MyText) or ("siri" in MyText) or ("siri" in MyText)):
                comment=["She Seems Clever!","Full Respect, Being An Assistant Is Hardwork","I Know Her, She Is Amazing","You Know Her? That's Great!"]
                timewait=speak(comment[random.randint(0,3)])
                time.sleep(timewait)
            elif("id" in MyText):
                speak(name,"iu")
                time.sleep(1)
                timewait=speak("Please Note Down Your ID ")
                time.sleep(timewait)
                time.sleep(0.5)
                timewait=speak(''.join(i for i in gma() if not i.isdigit()).replace(":",""),"io")
                print(''.join(i for i in gma() if not i.isdigit()).replace(":",""))
                time.sleep(timewait)
            elif("location" in MyText):
                MyText=MyText.lower()
                split_sentence = MyText.split(' ')
                idd=''.join([str(elem) for elem in split_sentence[split_sentence.index("of")+1:]]).lower()
                for x in table.find({"_id":idd},{ "_id": 0, "location": 1}):
                    timewait=speak("Last Updated Location Is "+x["location"])
                    time.sleep(timewait)
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("Could You Repeat That?")
