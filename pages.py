import re
import urllib2
import sys

from sets import Set

from Queue import *

MAXSIZE = 10000
VISITED = Set()
VISITED_LIST = []
LINKS_TO_DEST = []
QUEUE = Queue(maxsize = MAXSIZE)

class Node:
  def __init__(self, current, path=[]):
    self.curr = current # String
    self.path = path    # Array of String

  def addNode(self, node):
    self.path.append(node.curr)

  def addLink(self, link):
    self.path.append(link)

  def printNode(self):
    out = ''
    for n in self.path:
      out += (n + ' - ')
    out += self.curr
    print out

def getPage(title):
  url = 'http://en.wikipedia.org/wiki/' + title
  req = urllib2.Request(url)
  response = urllib2.urlopen(req)
  return response.read()

def getLinks(page):
  match = 'href="/wiki/[A-Z]+[^:\s]+."'
  links = re.findall(match, page)
  prefix = 'href="/wiki/'
  for i in range(0, len(links)):
    links[i] = links[i][len(prefix):len(links[i]) - 1]
  return links

def DFSearch(src_node, destination):
  linkables = getLinks(getPage(src_node.curr))[:5]

  for link in linkables:
    if link == destination:
      end = Node(link, VISITED_LIST)
      end.printNode()
      return
    elif ((not (link in VISITED_LIST)) and  
      (link != 'Main_Page') and
      (not ('disambiguation' in link)) and
      (not ('(' in link))):
      print 'visiting: ' + link
      VISITED_LIST.append(link)
      new = Node(link)
      DFSearch(new, destination)
      return
    else:
      pass

def BFSearch(src_node, str_destination):
  linkables = getLinks(getPage(src_node.curr))

  for link in linkables:
    if link == str_destination:
      end = Node(link, src_node.path)
      if not (src_node.curr in src_node.path):
        end.addNode(src_node)
      end.printNode()
      return
    elif link in LINKS_TO_DEST:
      end = Node(str_destination, src_node.path)
      end.addNode(src_node)
      end.addNode(Node(link))
      end.printNode()
      return
    elif ((not (link in VISITED))and  
        (link != 'Main_Page') and
        (not ('disambiguation' in link)) and
        (not ('(' in link))):
      VISITED.add(link)
      new = Node(link, src_node.path)
      if not (src_node.curr in src_node.path):
        new.path.append(src_node.curr)
      QUEUE.put(new)

  while(not (QUEUE.empty() or QUEUE.full())):
    next = QUEUE.get(0)
    print 'visiting: ' + next.curr
    BFSearch(next, str_destination)

    return
def FindLinks(src):
  linkables = getLinks(getPage(src))
  dcycle = []

  for link in linkables:
    link_linkables = getLinks(getPage(link))
    if src in link:
      dcycle += link

  return dcycle

def main():
  if (len(sys.argv) < 4):
    print 'Wrong call. Try: python pages.py MODE SOURCE DESTINATION'
    print 'Eg: python pages.py bfs Miley_Cyrus Los_Angeles'
    exit()

  src = sys.argv[2]
  dest = sys.argv[3]

  if (sys.argv[1] == 'bfs'):
    BFSearch(Node(src), dest)
  elif (sys.argv[1] == 'dfs'):
    DFSearch(Node(src), dest)
  elif (sys.argv[1] == 'bfsp'):
    LINKS_TO_DEST = FindLinks(dest)
    BFSearch(Node(src), dest)
  else:
    print 'Wrong call. Modes are: bfs, dfs, bfsp'

if __name__ == '__main__':
  main()