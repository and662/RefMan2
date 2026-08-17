
import os, sys, json, time, datetime 
from collections import deque 

import urllib, logging, requests, arxiv, itertools
from requests.exceptions import HTTPError 

import config as CFG
import citekeys as CK


def openlib_response( isbn, config ):
  
  time.sleep( config.api_rate_lim )  
  
  url_uenc = urllib.parse.quote( isbn, safe = '' ) 
  openlibrary_url = f'https://openlibrary.org/api/books?bibkeys=ISBN:{ url_uenc }&jscmd=data&format=json'
  req = requests.get( openlibrary_url )
  req.encoding = 'UTF-8'
  
  match req.status_code:
    case 200: 
      response = json.loads(str( req.text ))
    case 404: 
      return {}
    case _: 
      # print( f'The openlibrary.org API returned code: { req.status_code }' )
      return {}

  return response 


def summarized_metadata( response, isbn ):

  key = f'ISBN:{ isbn }'
  data = response[ key ]
  all_keys = data.keys()
  
  summary = {}
  summary[ 'isbn' ] = isbn 
  
  if 'title' in all_keys:
    summary[ 'title' ] = data[ 'title' ]
		
  if 'authors' in all_keys:
    author_list = deque([])
    all_authors = data[ 'authors' ]
    for author in all_authors:
      auth_name = author[ 'name' ]
      name_parts = auth_name.split( ' ' )
      name_parts = name_parts[::-1] # reverse the order (lastname first) 
      author_list.append( name_parts )
    summary[ 'authors' ] = list( author_list )
  
  if 'publishers' in all_keys and 'publish_date' in all_keys:
    date_str = data[ 'publish_date' ]
    
    try: 
      pub_date = datetime.datetime.strptime( date_str, '%B %d, %Y' )
      date_str = pub_date.strftime( "%Y-%m-%d" ) # reformat it for consistency 
    except:
      date_str = data[ 'publish_date' ]
    finally:
      summary[ 'publication-date' ] = date_str
      summary[ 'publisher' ] = data[ 'publishers' ][0][ 'name' ]
  
  return summary 


def save_metadata_json( metadata, citekey, config ):

  metadata_file = os.path.join( config.metadata_dir_openlib,  
                                f'{ citekey }.json' )
  
  with open( metadata_file, 'w') as mdfile:
    json.dump( metadata, mdfile )  



def download_pdf( citekey, summary, config ):

  def download_from_link( link, save_to ):
    # "link" is a url that shows a pdf 
    pdf_response = requests.get( url, stream = True )
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

  save_to = os.path.join( config.books_dir, f'{ citekey }.pdf' )

  if 'links' in summary.keys():
    for link in summary['links']:
      print( link )
      if download_pdf( link, save_to ): 
        return 

