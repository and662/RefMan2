
import os, sys, json, time, datetime 
from collections import deque 

import urllib, logging, requests, arxiv, itertools
from requests.exceptions import HTTPError 

import config as CFG
import citekeys as CK


def crossref_response( doi, config ):
  
  time.sleep( config.api_rate_lim )  
  
  # if we defined a "user_agent" and/or "mailto" variable in config.py
  # include that information in the request header 
  headers = {}
  if not config.api_user_agent == '': 
    headers[ 'User-Agent' ] = config.api_user_agent
  if not config.api_mailto == '':
    headers[ 'Mailto' ] = config.api_mailto 
  
  url_uenc = urllib.parse.quote( doi, safe = '' ) # dois often break urls
  crossref_url = f'https://api.crossref.org/works/{ url_uenc }'
  
  req = requests.get( crossref_url, headers = headers )
  req.encoding = 'UTF-8'
  
  # check if we found that doi 
  match req.status_code:
    case 200: 
      response = json.loads(str( req.text )).get( 'message' )
    case 404: 
      return {}
    case _: 
      print( f'For doi: { crossref_doi }' ) 
      print( f'The crossref.org API returned code: { req.status_code }' )
      return {}

  return response 


def summarized_metadata( metadata ):
  
  all_keys = metadata.keys()
  summary = {}  
  
  if 'title' in all_keys:
    summary[ 'title' ] = metadata[ 'title' ][0]
  
  if 'author' in all_keys: 
    author_list = deque([])
    authors = metadata[ 'author' ]

    for author in authors:
      name = [ author[ 'family' ], author[ 'given' ] ]
      if author[ 'sequence' ] == 'first': 
        author_list.appendleft( name )
      else:
        author_list.append( name ) 

    summary[ 'authors' ] = list( author_list ) 
  
  if 'DOI' in all_keys: 
    summary[ 'doi' ] = metadata[ 'DOI' ]
  
  if 'URL' in all_keys: 
    summary[ 'url' ] = metadata[ 'URL' ]
  
  if 'ISBN' in all_keys: 
    summary[ 'isbn' ] = [ val[0] for val in metadata[ 'ISBN' ] ]
  
  if 'ISSN' in all_keys:
    summary[ 'issn' ] = [ val[0] for val in metadata[ 'ISSN' ] ]
  
  if 'indexed' in all_keys: 
    indexed = metadata[ 'indexed' ]

  if 'publisher' in all_keys:
    summary[ 'publisher' ] = metadata[ 'publisher' ]

  if 'issue' in all_keys: # written as no. when citing 
    summary[ 'number' ] = metadata[ 'issue' ]

  if 'volume' in all_keys: 
    summary[ 'volume' ] = metadata[ 'volume' ]
  
  if 'published' in all_keys: 
    sub_dict = metadata[ 'published' ] 
    if 'date-parts' in sub_dict.keys():
      date_parts = sub_dict[ 'date-parts' ][0]
      pub_date = datetime.datetime( date_parts[0], date_parts[1], date_parts[2] )
      date_str = pub_date.strftime( "%Y-%m-%d" )
      summary[ 'publication-date' ] = date_str

  pdf_links = deque([])
  if 'link' in all_keys:  
    links = metadata[ 'link' ]
    for link in links:
      if not link[ 'intended-application' ] == 'syndication':
        pdf_links.append(link[ 'URL' ])
  if len( pdf_links ) > 0:
    summary[ 'links' ] = list( pdf_links )

  return summary 


def download_pdf( citekey, summary, config ):

  def download_from_link( link, save_to ):
    # "link" is a url that shows a pdf 
    pdf_response = requests.get( link, stream = True )
    match pdf_response.status_code:
      case 200:
        with open( save_to, 'wb' ) as f:
          for chunk in pdf_response.iter_content( 2000 ):
            f.write( chunk )
        return True 
      case 404: 
        return False
      case _:   
        return False

  save_to = os.path.join( config.papers_dir, f'{ citekey }.pdf' )

  if 'links' in summary.keys():
    for link in summary['links']:
      print( link )
      if download_from_link( link, save_to ): 
        return 

