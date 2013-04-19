import socket
import lxml.html
import praw
from random import randint

channel = raw_input("Channel: ")
nick = raw_input("Nick: ")
class Bot:
    def __init__(self, server='irc.quakenet.org', port=6667):
        """creates the socket object and connects to the server"""
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect( (server, port ) )
        self.data = self.irc.recv ( 4096 )
        self.reddit = praw.Reddit(user_agent='just a simple irc bot')
        
    def nickname(self, realname = 'BOTchii'):
        self.irc.send('NICK ' + nick + '\r\n')
        self.irc.send('USER Botty bot botty bot bot: Python IRC\r\n')

    def join_channel(self):
        self.irc.send('JOIN ' + channel + '\r\n')
        
    def work(self):
        data = self.irc.recv ( 4096 )
        if data.find('PING') != -1:
            self.irc.send('PONG ' + data.split()[1] + '\r\n')
            self.irc.send('JOIN ' + channel + '\r\n')
        
        if data.find(':bajs') != -1:
        	self.irc.send('PRIVMSG ' + channel + ' :mer bajs\r\n')

        #reddit first post
        if data.find(':!firstpost') != -1:
            try:
                terms = data.split(' :')
                terms = terms[1].split()
                sub = 'all'
                if len(terms)>1:
                    sub = terms[1]
                title = ''
                url = ''
                ups = ''
                downs = ''
                firstposts = self.reddit.get_subreddit(sub).get_hot(limit=1)
                for firstpost in firstposts:
                    ups = firstpost.ups
                    downs = firstpost.downs
                    title = firstpost.title
                    url = firstpost.url
                self.irc.send('PRIVMSG ' + channel + ' :\x02Top post from ' + sub + ': \x02<\x037 ' + str(ups) + '\x03 |\x0311 ' + str(downs) +'\x03 > - \x034' + title + '\x03 - ' + url + '\r\n')
            except:
                pass
        

        #reddit first post
        if data.find(':!randompost') != -1:
            try:
                terms = data.split(' :')
                terms = terms[1].split()
                sub = 'all'
                if len(terms)>1:
                    sub = terms[1]
                title = ''
                url = ''
                ups = ''
                downs = ''
                firstposts = self.reddit.get_subreddit(sub).get_hot(limit=100)
                stopnumb = randint(1,100)
                for x in range(0, stopnumb):
                    firstpost = next(firstposts)
                ups = firstpost.ups
                downs = firstpost.downs
                title = firstpost.title
                url = firstpost.url
                self.irc.send('PRIVMSG ' + channel + ' :\x02Post #' + str(stopnumb) + ' from ' + sub + ': \x02<\x037 ' + str(ups) + '\x03 |\x0311 ' + str(downs) +'\x03 > - \x034' + title + '\x03 - ' + url + '\r\n')
            except:
                pass

        #YouTube links
        if data.find(':http://youtu.be') != -1 or data.find(':http://www.youtube.com') != -1:
            try:
            	split = data.split(' :')
            	split = split[1].split()
            	url = split[0]
            	title = lxml.html.parse(url).find(".//title").text
            	self.irc.send('PRIVMSG ' + channel + ' :\x02YouTube: \x02' + title +'\r\n')
            except:
                pass

        #imgur links
        if data.find('http://i.imgur.com/') != -1:
            try:
                split = data.split(' :')
                split = split[1].split()
                url = split[0]
                split = url.split('.')
                url = split[0]
                for x in range(1, len(split)-1):
                    url = url + '.' + split[x]
                title = lxml.html.parse(url).find(".//title").text
                if not title.find("the simple image sharer") != -1:
                    self.irc.send('PRIVMSG ' + channel + ' :\x02Imgur: \x02' + title +'\r\n')
                else:
                    print "not found"
            except:
                pass

        #roll
        if data.find(':!roll') != -1:
            try:
            	data = data.split(' :')
                nick = data[0].split('!')[0]
                nick = nick[1:]
            	msg = data[1].split()
            	#print msg
            	if len(msg) > 2:
            		self.irc.send('PRIVMSG ' + channel + ' :\x02' + nick + ' rolls ' + str(randint(int(msg[1]), int(msg[2]))) +'\x02\r\n')
                elif len(msg) == 1:
                    self.irc.send('PRIVMSG ' + channel + ' :\x02' + nick + ' rolls ' + str(randint(1, 100)) +'\x02\r\n')
            except:
                pass
        
    def parseMessage(self):
        data = self.data
        msg = data.split(':')[2]
        author = data.split(':')[1].split('!')[0]
        print "%s : %s" % (author,msg)

bot = Bot()
bot.nickname()
bot.join_channel()

while True:
    bot.work()
