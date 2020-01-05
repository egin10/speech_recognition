import speech_recognition as sr
import webbrowser as wb
import urllib.request
import urllib.parse
import re
import pyttsx3
import datetime


def speak(text):
    engine = pyttsx3.init('espeak')
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()


def listening():
    r = sr.Recognizer()
    result = ''

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # here

        print("Say something!")
        audio = r.listen(source, phrase_time_limit=15)

    try:
        result = r.recognize_google(audio, language='un-US')
        print("You said : " + result)
        return result
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return None


def greetings():
    time = int(datetime.datetime.now().strftime('%H'))
    if time > 4 and time <= 12:
        speak('Hello, Good Morning Boss')
    elif time > 12 and time <= 17:
        speak('Hello, Good Afternoon Boss')
    else:
        speak('Hello, Good Evening Boss')


# Main Function
if __name__ == "__main__":
    # Greetings by the time
    # greetings()
    # speak('What can i help you ?')

    while True:
        # Listening
        result = ''
        if listening() is None:
            speak('Say something please!')
        else:
            result = listening().lower()

        # Time Today
        if 'time' in result:
            date = datetime.datetime.now()
            speak(
                f"Today is {date.strftime('%A')}")
            speak(
                f"{date.strftime('%d')} {date.strftime('%B')} {date.strftime('%Y')}")
            speak(
                f"{date.strftime('%H')}:{date.strftime('%M')} {date.strftime('%p')}")

        # Open Google
        elif 'open google' in result:
            wb.open('google.com')

        # Searching keywords on Google
        elif 'on google' in result:
            if len(result.split('find')) > 0:
                speak('OK')
                find_words = result.split('find')[1].strip()
                print('You want to find ' + find_words)
                keywords = find_words.replace('on google', '')
                url = "https://www.google.com.tr/search?q={}".format(keywords)
                wb.open(url)

        # Open Youtube
        elif 'open youtube' in result:
            speak('OK')
            wb.open('youtube.com')

        # Searching keywords on Youtube
        elif 'on youtube' in result:
            if len(result.split('find')) > 0:
                speak('OK')
                find_words = result.split('find')[1].strip()
                print('You want to find ' + find_words)
                keywords = find_words.replace('on youtube', '')
                url = "http://www.youtube.com/results?search_query={}".format(
                    keywords)
                wb.open(url)

        # Play Music from Youtube
        elif 'from youtube' in result:
            if len(result.split('play')) > 0:
                speak('OK')
                play_words = result.split('play')[1].strip()
                print('Playing ' + play_words)
                keywords = play_words.replace('from youtube', '')
                query_string = urllib.parse.urlencode(
                    {"search_query": keywords})
                html_content = urllib.request.urlopen(
                    "http://www.youtube.com/results?" + query_string)
                search_results = re.findall(
                    r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
                url = "http://www.youtube.com/watch?v=" + search_results[0]
                wb.open(url)

        # Exit
        elif 'exit please' or 'sleep now' or 'good bye' in result:
            speak('Good bye!')
            break
