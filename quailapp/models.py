from django.db import models
import sys, os, cgi, urllib, re

class Question(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    text = models.TextField()
    votes = models.IntegerField()    

# for CAS login..
class CASClient:
   def __init__(self, request):
      self.cas_url = 'https://fed.princeton.edu/cas/'
      self.request = request
   def Authenticate(self):
      # If the request contains a login ticket, try to validate it
      if 'ticket' in self.request.GET:
         netid = self.Validate(self.request.GET['ticket'])
         if netid != None:
            return netid
   
   def redirect_url(self):
      login_url = self.cas_url + 'login' + '?service=' + urllib.quote(self.ServiceURL())
      return login_url
      
   def Validate(self, ticket):
      val_url = self.cas_url + "validate" + \
         '?service=' + urllib.quote(self.ServiceURL()) + \
         '&ticket=' + urllib.quote(ticket)
      r = urllib.urlopen(val_url).readlines()   # returns 2 lines
      if len(r) == 2 and re.match("yes", r[0]) != None:
         return r[1].strip()
      return None
   def ServiceURL(self):
      ret = 'http://' + self.request.META['HTTP_HOST'] + self.request.META['PATH_INFO']
      ret = re.sub(r'ticket=[^&]*&?', '', ret)
      ret = re.sub(r'\?&?$|&$', '', ret)
      return ret
      #if os.environ.has_key('REQUEST_URI'):
      #   ret = 'http://' + os.environ['HTTP_HOST'] + os.environ['REQUEST_URI']
      #   ret = re.sub(r'ticket=[^&]*&?', '', ret)
      #   ret = re.sub(r'\?&?$|&$', '', ret)
      #   return ret
         #$url = preg_replace('/ticket=[^&]*&?/', '', $url);
         #return preg_replace('/?&?$|&$/', '', $url);
      #return "something is badly wrong"
 
def main():
  print "CASClient does not run standalone"
if __name__ == '__main__':
  main()
