"""This is the simple python script that does all the work for setting up the beautiful 
   bioinformatics site. First we look into site.info were all pages are defined by the 
   triple of page name, which will determine the file names, page title, which determines 
   the link text shown on the page, and page description, which determines the tool tip that 
   is shown on mouse over i.e. what the title property of the html tag. Then we get the 
   main.tpl template.
   each page defined in site.info must have a corresponding file called <file_name>.page 
   the html code in this file will then be inerted into the main template 
   we also generate a list of links for all pages defined in site.info which we insert into 
   all the generated pages. 
   finally each page is written to <file_name>.html, if this file already exists it is 
   ERASED (!) and replaced"""

"""To change a site (e.g. index.html) change what you want in the .page (e.g. index.page) file 
   and run python bioinf_cms.py"""
"""To create a page (e.g. test.html) start a new .page document (e.g. test.page) and just write some text in html
   you don't need to bother about header footer whatsoever. then add an entry on a new line to site.info (e.g. test, this is a test, Test)
   then run bioinf_cms.py. 
   the new page (e.g. test.html) will be generated and a link added to the sidebar (on all pages) 
   e.g. link to test.html, with text: this is a test, and on mouse over your browser will show you a tooltip with the text: Test,"""
"""To hide a page simply remove its entry from the site.info and remove <file_name>.html, 
   this could be useful if you write something but don't want to show it until some time later.
   if you also remove <file_name>.page the page will be completely deleted."""

"""Software written by Florian Klinglmueller <float_at_lefant.net>
   Use as you like, credit where due"""

   


import os,re

def getLinks(info='site.info'):
    """look in the info, check for files, and make a list of links"""
    infoFile = open(info)
    links = infoFile.readlines()[1:]
    links = [link.strip() for link in links]
    linkInfo = [[item.strip() for item in name.split(',')] for name in links]
    infoFile.close()
    return(linkInfo)

def mergeLists(lists):
    merged = []
    for l in lists:
        for s in l:
            merged.append(s)
    return merged

def buildLinkHtml(links):
    """Take the link list and build the html tags"""
    def buildTag(link):
        return "<p><a href=\""+link[0]+".html\" title=\""+link[2]+"\">"+link[1]+"</a></p>"
    return [buildTag(link) for link in links]

def buildPagesHtml(links,template='main.tpl',altlinks=''):
    def getTemplate(template):
        templateFile = open(template)
        templateHtml = templateFile.readlines()
        templateFile.close()
        return templateHtml
    def getContentLine(templateHtml):
        print 'works'
        try: 
            return templateHtml.index('[[content]]\n')
        except: 
            return 0
    def getLinkLine(templateHtml):
        return templateHtml.index('[[links]]\n')
    def getPageHtml(link):
        pageFile = open(link + '.page')
        pageHtml = pageFile.readlines()
        pageFile.close()
        return pageHtml
    def buildPage(page,templateHtml):
        return mergeLists([templateHtml[:getContentLine(templateHtml)],getPageHtml(page),templateHtml[(getContentLine(templateHtml)+1):]])
    def addLinks(page,linkHtml):
        return mergeLists([page[:getLinkLine(page)],linkHtml,page[(getLinkLine(page)+1):]])
    
    if altlinks == '':
        altlinks = links
    templateHtml = getTemplate(template)
    pages = [page for [page,a,b] in links]
    pagesHtml = [buildPage(page,templateHtml) for page in pages]
    pagesHtml = [addLinks(page,buildLinkHtml(altlinks)) for page in pagesHtml]
    return(pagesHtml)

def makeFiles(links,pagesHtml,suf='.html'):
    files = [f+suf for [f,a,b] in links]
    for i in range(len(files)):
        try: 
            os.remove(files[i])
        except OSError:
            pass
        pageFile = open(files[i],'w')
        pageFile.writelines(pagesHtml[i])
        pageFile.close()

    



if __name__ == "__main__":
    links = getLinks()
    pagesHtml = buildPagesHtml(links)
#    footerInc = buildPagesHtml([['footer','',''],],template='footer.tpl',altlinks=links)
    makeFiles(links,pagesHtml)
#    makeFiles([['includes/footer','',''],],footerInc,'.inc')
