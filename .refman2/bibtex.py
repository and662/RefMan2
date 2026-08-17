
from collections import deque

import crossref_api as CROSSREF 
import datacite_api as DATACITE 
import arxiv_api as ARXIV 


def bibtex_article( citekey, metadata ):

  all_keys = metadata.keys()  
  elements = deque([])

  if 'title' in all_keys: 
    title = metadata[ 'title' ]
    elements.append( 'title = {' + title + '}' )
  
  if 'authors' in all_keys: 
    authors = metadata[ 'authors' ]
    author_names = deque([])
    for author in authors:
      author_names.append( ' '.join(author[::-1]) )
    elements.append( "author = {" + ' and '.join(list( author_names )) + "}" )

  if 'doi' in all_keys:
    elements.append( 'doi = {' + metadata[ 'doi' ] + '}' )

  if 'publisher' in all_keys: 
    journal = metadata[ 'publisher' ]
    elements.append( 'journal = {' + journal + '}' )

  if 'issue' in all_keys: 
    issue = metadata[ 'issue' ] 
    elements.append( 'number = {' + issue + '}' )

  if 'volume' in all_keys: 
    vol = metadata[ 'volume' ]
    elements.append( 'volume = {' + str(vol) + '}' )

  if 'publication-date' in all_keys: 
    year = metadata[ 'publication-date' ][0:4]
    elements.append( 'year = {' + year + '}' )

  # now put it all together 
  bibtex = '@article{' + citekey + ', \n'
  bibtex += ', \n'.join(list( elements )) + '}'
  return bibtex 


def bibtex_book( citekey, metadata ):
    
  all_keys = metadata.keys()
  elements = deque([])
  
  if 'title' in all_keys: 
    title = metadata[ 'title' ]
    elements.append( 'title = {' + title + '}' )
  
  if 'authors' in all_keys: 
    authors = metadata[ 'authors' ]
    author_names = deque([])
    for author in authors:
      author_names.append( ' '.join(author[::-1]) )
    elements.append( "author = { " + ' and '.join(list( author_names )) + " }" )

  if 'isbn' in all_keys:
    elements.append( 'isbn = {' + metadata[ 'isbn' ] + '}' )

  if 'publication-date' in all_keys: 
    year = metadata[ 'publication-date' ][0:4]
    elements.append( 'year = {' + year + '}' )

  # now put it all together 
  bibtex = '@book{' + citekey + ', \n'
  bibtex += ', \n'.join(list( elements )) + '}'
  return bibtex 


def bibtex_online( citekey, metadata ):

  all_keys = metadata.keys()
  elements = deque([])

  if 'title' in all_keys:
    elements.append( 'title = {' + metadata['title'] + '}' )
  
  if 'authors' in all_keys: 
    author_names = deque([])
    for author in metadata[ 'authors' ]:
      author_names.append( ' '.join(author) )
    elements.append( "author = { " + ' and '.join(list( author_names )) + " }" )
   
  if 'year' in all_keys:
    elements.append( 'year = {' + metadata[ 'year' ] + '}' )
  
  if 'url' in all_keys:
    elements.append( 'url = {' + metadata[ 'url' ] + '}' )

  if 'urldate' in all_keys:
    elements.append( 'urldate = {' + metadata[ 'urldate' ] + '}' )

  # now put it all together 
  bibtex = '@online{' + citekey + ', \n'
  bibtex += ', \n'.join(list( elements )) + '}'
  return bibtex 

