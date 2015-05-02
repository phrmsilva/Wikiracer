# Wikiracer

A bot for Wikipedia races.

## Abstract
#### What did I do in a nutshell? 


This project consists of a Wikipedia crawler. It attempts to find a path between two different articles in Wikipedia, in which the article pages are the nodes and the links on a article's page is a directed edge towards the article it links to. It can apply either Depth First Search or Breadth First Search algorithms to it. There are also a couple of implementation optimization tools for it.

-----


## Introduction

#### What is the problem? 
The goal here is to determine short paths from one article to the other. Given the size of Wikipedia, it is a similar process to finding a short path between two locations within a certain limited area with a large amount of different paths. The secondary goal is to do it in a time shorter than a human would be able to do it.

#### Why is it interesting?
The motivation behind this project is the game Wikipedia Race. In it, two or more players try to go from one mutual page to a certain page by only clicking on links on their current article. While humans can make fast associations between topics and try to predict what articles will bring them closer to the destination, machines cannot. Therefore, this is an attempt to make an algorithm in order to test the human intuition  versus the optimal computation.

The approach for this problem is to do a Breadth First Search on the paths. That is, to go down all possible paths one step at a time simultaneously (or in an ordered fashion, just so that no path gets two steps before any other). The destination's search, however, will move slower, as it has to check the edges coming out of it for a 2-node cycle. In addition, it will not identify *all* nodes that connect to it, but rather the ones that do and vice-versa.

#### What have others done?
There is a running theory of the '6 degrees of Hitler' on Wikipedia that, similar to the better known '6 degrees of Bacon', any page on Wikipedia is 6 pages away from Hitler. As it does not seem to be true (there are plenty of pages that are 'dead' pages and won't link to it), no formal work has been done on it, but there are strategies about it. The most common of these strategies is to look for articles relevant in the Hitler page (such as World War II, his date of birth, or the location he was born in) instead of blindly looking for one page. I tried to apply a similar approach in this project - one with less Hitler on it.

Other than that, the user aaasen created 'Kapok: A Knowledge Graph of Wikipedia'. While very interesting and useful to iterate through Wikipedia, it was not applicable to the specific implementation suggested for this project.

Robert West, a computer scientist at Stanford, has also done significant research on human behaviour vs automatic navigation. He helped develop Wikispeedia, which is a resource for which a user can try to get from one random page to another in the least amount of clicks.

----

## Materials and Methods
The approach to this problem was to apply graph search on the pages.
The code makes three approaches available:

#### Depth First Search
Generally on Wikipedia, the first paragraph of a page is an introduction and therefore the pages linked in the beginning are more general links (such as concepts, professions, locations, etc). If there is a reason for a strong suspicion that the destination falls among one of these categories, than this may be the best alternative.
Eg: Miley_Cyrus -> Canada
Output: Miley_Cyrus -> Franklin,_Tennessee -> State_of_Franklin -> District_of_Franklin -> Canada

#### Breadth First Search
Probably the most common approach, it aims at finding close pages. It will find the shortest path, but it will also require a lot of processing and memory power. Generally most recommended for destinations one suspects are closely related to the source page. Its runtime grows very fast.
Eg: Miley_Cyrus -> Los_Angeles
Output: Miley_Cyrus -> Los_Angeles

#### Breadth First Search With "Preparation"
This is an approach with a similar algorithm to Breadth First Search, just adapted similarly to the approaches used in the '6 Degrees of Hitler' (see 'Introduction'). Before running the search, it prepares a list of pages that are known to link to the destination. While that process may consume a relevant amount of runtime, it makes the overall algorithm more efficient, as the search becomes aims at a set of pages instead of only one.

------

## Results & Discussion
The main question in this project has been if an average computer, with no prior information on Wikipedia, could beat a human at finding a path from one page to another in the shortest amount of time.

The answer, in most cases is no.
The consumption of memory and processing power to find the pages makes it extremely hard on average machines. With the current implementation, the computer will likely either run out of memory (as in the implementation for the BFS approaches) or, when the implementation accounts for the memory consumption, the Python framework will run out of callbacks.

In my personal computer, all 8GB of RAM were consumed within a few steps of the Breadth First Searches. For the Depth First Search, it only took a few hundred steps as well for the processor to time out.

However, the performance improves when the pages are not randomly selected. That is, humans have a higher likelihood of choosing well connected pages when deciding by themselves. With that, its not necessary to go into every page and would replicate more closely a human behaviour by not going too far into certain parts.

Perhaps the biggest lesson to take away from this is the functionality of map services. While Wikipedia is big, so is the map between New York and Boston and a route from specific location in the two cities can be easily calculated within seconds by many engines. It shows the weakness of BFS and DFS in scalability for large settings.

------

## Future Work
One of the main things that I tried to approach was to make sure I had the concurrency of program working correctly - hence that use of the Queue implementation. Initially, the goal was to develop this project with a typed language that could handle this better, as Go. Unfortunately for this implementation it doesn't make too much of a difference - the runtime in the abstract is the same, the change would be how the frameworks are implemented differently between the two languages.

An improvement that could come out of its own project would be categorizing the pages in Wikipedia so that it is possible to rank the pages being linked and so that it is possible to choose pages that are more likely to link to the destination. Currently one of the main problems is going into pages that have a lot of links - just not useful ones. For example, the page of Franklin, Tennessee starting from Miley Cyrus. While it is one of the first pages in the article and one of the first to be explored, Franklin is not related to many big events or locations other than Miley herself.

With enough preparation time, it should also be possible to record the Wikipedia pages' links to others beforehand in a database. Currently one of the main things that throws off runtime is how long it takes to request the HTML page, parse it and 'sanitize' it.

-----

## Literature Cited and Referenced
- Robert West, Joelle Pineau, and Doina Precup. Wikispeedia: An Online game for Inferring Semantic Distances between Concepts. In 21st International Joint Conference on Artificial Intelligence (IJCAI’09), pp. 1598-1603, Pasadena, Calif., 2009 

- Robert West and Jure Leskovec. Human Wayfinding in Information Networks. In 21st International World Wide Web Conference (WWW’12), pp. 619-628, Lyon, France, 2012. 

- Robert West and Jure Leskovec. Automatic versys Human Navigation in Information Networks. In 6th International AAAI Conference on Weblogs and Social Media (ICWSM ‘12), pp. 362-369, Dublin, Ireland, 2012

- S. Dobrev, R. Kralovic, E. Markou:  Online Graph Exploration with Advice

- L. Aasen, Kapok: a knowledge graph of Wikipedia https://github.com/aaasen/kapok

- Python Software Foundation https://hg.python.org/

- MediaWiki: http://www.mediawiki.org/wiki/API:Main_page

- Wikispeedia: http://cs.mcgill.ca/~rwest/wikispeedia

-----

## Acknowledgments
Thanks to Luke for helping me figuring out regex and with Go when this was a Go project.

------

## Usage
To run the program, simply clone the code and run from the command line:
```console
$ python pages.py [MODE] [SOURCE] [DESTINATION]
```
I suggest the following for demo:
```console
$ python pages.py dfs Miley_Cyrus Canada
```
```console
$ python pages.py bfs Miley_Cyrus City
```
