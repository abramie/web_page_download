# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from ebooklib import epub
import urllib3
import html5lib
import xml.etree.ElementTree as ET

import timeit



"""Creation de l'epub"""
book = epub.EpubBook()

# set metadata


book.add_author('Angry squirrel')

url = 'https://boxnovel.com/novel/the-experimental-log-of-the-crazy-lich'
title = url.split('/')[4]
book.set_identifier(title)
book.set_title(title)
book.set_language('en')
debut = 1
fin = 841
start = timeit.timeit()
spine = ['nav']
for i in range(debut, fin+1):
    url_chapter = url + '/chapter-' + str(i) +'/'
    http = urllib3.PoolManager()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    
    r = http.request('GET',url_chapter, headers=headers )
    r.status
    r.data
    
    document = html5lib.parse(r.data)
    
    document = html5lib.parse(r.data,namespaceHTMLElements=False)
    
    
    for meta in document.iter('meta'):
        if meta.attrib.get("property") == "og:title":
            title_chapter = (meta.attrib.get("content").split('-')[1]) #+ str(i)
            
    
    c = epub.EpubHtml(title=title_chapter, file_name='chap_'+str(i)+'.xhtml', lang='hr')
    c.content=u'<h2>'+title_chapter+'</h2>'
    #print(document.iter('div'))
    for div in document.iter('div'):
        #print(div.attrib.get("class"))
        if div.attrib.get("class") == "reading-content":
            for para in div.iter('p'):
                text = ''
                em = para.findtext('em')
                strong = para.findtext('strong') 
                span = para.findtext('span')
               
                
               
                c.content = c.content + '<p>'
                
                def add_paragraphe(para):
                    if para.text:
                        c.content = c.content + para.text 
                    for thing in para:
                        if thing.text:
                            texte = thing.text
                            if thing.tag == 'em' :
                                texte = '<i>'+ texte +'</i>'
                            if thing.tag == 'strong' :
                                texte = '<b>'+ texte +'</b>'
                            c.content = c.content + texte
                        else:
                            
                            if thing.tail:
                                texte = thing.tail
                                if thing.tag == 'br':
                                    texte = '<br>' + texte
                                if thing.tag == 'em' :
                                    texte = '<i>'+ texte +'</i>'
                                if thing.tag == 'strong' :
                                    texte = '<b>'+ texte +'</b>'
                                c.content = c.content + texte
                            else:
                                add_paragraphe(thing)
                            
                add_paragraphe(para)            
                c.content = c.content + '</p>'
                # if em :
                #     c.content = c.content + '<p><i>' + em + '</i></p>'
                # elif para.text:
                #     c.content = c.content + '<p>'+ para.text +'</p>'
                #     #print(para.text)
                # elif strong :
                
                #     c.content = c.content + '<p><b>'+ strong +'</b></p>'
                # elif span:
                #       c.content = c.content + '<p>'+ span +'</p>'
                # else : 
                #     if para.find('*') and para.findtext('*'):
                #         print("missing text in chapter " + str(i))
                #         print(para.find('*'))
                #         print(para.findtext('*'))
                #     elif para.find('span') and para.find('span').tail:
                #         #print(para.find('span').tail)
                        
                #         c.content = c.content + '<p>'+ para.find('span').tail+'</p>'
                        
                #     elif para.find('strong') and para.find('strong').find('em') and para.find('strong').find('em').text:
                #         #(print(para.find('*').findtext('*'))
                #         c.content = c.content + '<p><b><i>'+ para.find('strong').find('em').text +'</i></b></p>'
                    
                        
                #print(para.text)
    print("add chapter" + str(i))
    book.add_item(c)
    spine.append(c)
    print("fin add")
end = timeit.timeit()
print("temps telechargement : " + str(end - start))
# create chapter



# add chapter


# define Table Of Contents
book.toc = (spine)

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
style = 'BODY {color: white;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
style_text = '.italic {font-style: italic}'
text_css = epub.EpubItem(uid="text_nav", file_name="style/text.css", media_type="text/css", content=style_text)

# add CSS file
book.add_item(nav_css)
book.add_item(text_css)
# basic spine
book.spine = spine
print("temps complet : " + str(timeit.timeit() - start))
# write to the file
epub.write_epub(title+''+'.epub', book, {})