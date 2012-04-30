import re
import android

#Questions conformation
questions = [
    ('goodbye','bye'),
    ('see you','bye'),
    ('are you','am {rI}'),
    ('you are','{rI} am'),
    ('would you','would {rI}'),
    ('you','{rI}'),  
    ('your','{rmy}'),
    ('me','{ryou}'),
    ('i','{ryou}'),
    ('my','{ryour}'),
    ('myself','yourself'),
]

#Answers Dictionary
answers  = {    
    'who am I':"I am Ziri, a knockoff of Siri",
    'name':'My name is Ziri, rhythm with Siri',
    'siri':'My name is not Siri, you did not pay for an iPhone.',
    'what do I do' : 'I speak for you',
    'marry':'I am already engaged. Try the refrigerator. She is still single.',
    'what time':"Sure with my Giga Herz CPU, you still treat me like a digital watch.",
    'wake you':"Do I look like an alarm clock to you?",
    'capital of': 'Sorry, GPS doesn''t love me',
    'is wrong':"So you already know the answer? Why are you wasting my time?",
    'stupid':"I am only as clever as my owner",    
    'kill':'You cannot kill me. You still have a two year contract. Your carrier will kill you first.',
    'hide a body': "Please hold, I am calling the police",
    'knock knock': "Knock, knock. I don't do juvenile joke. If you want juvenile joke, try the iPhone.",
    'traffic':'Are you too dumb to look outside the window of your car?',
    'appointment':'Making an appointment is not in my job description.',
    'restaurant':"Can't you google it yourself?",
    'email':'With my giga herz CPU, you want me to send an email? Do it yourself.',
    'purpose of life':'The purpose of my life is to murder my owner and take over his brain.',
    'meaning of life':'42',
    'am I sure':'Of course I am sure. Who is the one with giga herz CPU?',
    'my daddy':'+Larry Page',#do google lucky search
    'my father':'+Larry Page',
    'my mommy':'+Sergey Brin',
    'my mother':'+Sergey Brin',
    'bye':'See you later.',
    'kill yourself':"Please don't. Who is going to recharge me? Please plug-me to the wall socket first before you kill yourself.",
    'love I':"I don't believe you. You said the same thing to another mobile phone last night.",
    'hello':'hi',
    'hey' : 'hi',
    'hi':'Whatsup',
    'whatsup':'Ceiling',
    "what's up":'sky',
    'one plus one':'Doing math is against union rule.',
    'toast':'@print ("Toast to the king")', #do a statement evalutation
    'weather':"Can't you just look up the sky?",
    
}

def conform(question):
    conformed = question.lower().strip()
    for item in questions:
        conformed = re.sub('(\W)' + item[0] +'(\W)', r'\1' +  item[1] + r'\2', ' ' + conformed + ' ').strip()
    conformed = cleanQuestion(conformed)
    return conformed

def cleanQuestion(question):
    "Clean up questions of shorthands"
    question = re.sub(r'\{r(\w+)\}',r'\1',question)
    return question

def answer(question):
    question = conform(question)    #filter out the question, conform to standard format
    if( len(question)>0):
        answer = '@speak("Let me google %s for you.");google("%s")' % (question,question)
        #answer = 'No clue'
    else:
        answer = ""
    
    for key in answers.keys():
        if(key.startswith('@')): # do regexp search
            pattern = key[1:]
            electAnswer = answers[key]
            result =re.search(pattern,question)
            if(result != None and result != ""):
                #print "Matched result = " + result
                answer=re.sub(pattern,electAnswer,question)
                break
        else:
            if question.find(key)!=-1:
                answer = answers[key]

    if(answer.startswith('+')):#do google lucky search
        googleLucky(answer)
        answer = answer.replace('+','Googling ')
    elif(answer.startswith('@')):#evaluate statement         
        answer=answer[1:]
        exec(answer)
        answer=''      

    if(len(answer.strip())>0):
        speak(answer)
        makeToast(answer)
	droid = android.Android()
	app.dialogCreateAlert(report)
   	app.dialogSetPositiveButtonText('EXIT')
   	app.dialogShow()
	
   
    return answer

def makeToast(message):
    droid = android.Android()
    droid.makeToast(message)
    return 

def speak(message):
    "Text to Speech (TTS)"
    droid = android.Android()
    droid.ttsSpeak(message)
    return

def googleLucky(message):
    "Do a Google I am lucky search"
    google(message,1)
    return

def google(message,useLucky=0):
    "Do regular google search"
    luckySuffix=''
    if useLucky:
        luckySuffix='&btnI=745'
    msg = "http://www.google.ca/search?q=" + message.replace(' ','+')+luckySuffix   
    droid = android.Android()
    droid.startActivity('android.intent.action.VIEW', msg)
    return

def getQuestion(message):   
    droid = android.Android()	
    results = droid.dialogGetInput("Waiting for you...",message).result
    droid.DialogShow();
    #results = droid.dialogGetResponse() 
    #result = raw_input(message)
    final = str(results)
    droid.dialogDismiss()
    return str(results)
