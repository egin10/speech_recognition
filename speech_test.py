import speech_recognition as sr
import webbrowser as wb
import urllib.request
import urllib.parse
import re

r = sr.Recognizer()
result = ''

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)  # here

    while True:
        print("Say something!")
        audio = r.listen(source)
        result = r.recognize_google(audio)

        try:
            print("You said : " + result)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        # DO SOMETHING BY VOICE RESULT
        result = result.lower()

        # Open Google
        if 'open google' in result:
            wb.open('google.com')

        # Searching keywords on Google
        elif 'on google' in result:
            find_words = result.split('find')[1].strip()
            print('You want to find ' + find_words)
            keywords = find_words.replace('on google', '')
            url = "https://www.google.com.tr/search?q={}".format(keywords)
            wb.open(url)

        # Open Youtube
        elif 'open youtube' in result:
            wb.open('youtube.com')

        # Searching keywords on Youtube
        elif 'on youtube' in result:
            find_words = result.split('find')[1].strip()
            print('You want to find ' + find_words)
            keywords = find_words.replace('on youtube', '')
            url = "http://www.youtube.com/results?search_query={}".format(
                keywords)
            wb.open(url)

        # Play Music from Youtube
        elif 'from youtube' in result:
            play_words = result.split('play')[1].strip()
            print('Playing ' + play_words)
            keywords = play_words.replace('from youtube', '')
            query_string = urllib.parse.urlencode({"search_query": keywords})
            html_content = urllib.request.urlopen(
                "http://www.youtube.com/results?" + query_string)
            search_results = re.findall(
                r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            url = "http://www.youtube.com/watch?v=" + search_results[0]
            wb.open(url)

        # Exit
        elif 'exit please' in result:
            break
