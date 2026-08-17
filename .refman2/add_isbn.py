
import os, sys, json, time, datetime 
from collections import deque 

import urllib, logging, requests, arxiv, itertools
from requests.exceptions import HTTPError 

import config as CFG
import citekeys as CK
import openlibrary_api as OPENLIB 
import database as DB
import bibtex as BIBTEX


def describe_new_ref( citekey, summary ):
  print( f'Created new reference with citekey: { citekey }' ) 
  # TD: print authors, title etc. 


def add_isbn( isbn, citekey = None, citekeysDB = None, config = None, verbose_mode = False ):

  if config == None: 
    config = CFG.Config( config_file = None, verbose_mode = verbose_mode )
  if citekeysDB == None:
    citekeysDB = DB.database( None, config = None )

  # check if that isbn is saved already 
  citekeys_match = citekeysDB.citekey_from_id( isbn )
  if not citekeys_match == None:
    print( f'The identifier { isbn } (of type "{ citekeys_match[1] }") already has the citekey: { citekeys_match[0] }' )
    citekeysDB.update_accessed_date( citekeys_match[0] )
    return 

  # check openlibrary 
  response = OPENLIB.openlib_response( isbn, config )
  if not response == {}:

    print( 'Found a match at openlibrary.org' )
    summary = OPENLIB.summarized_metadata( response, isbn )

    if citekey == None:
      citekey = CK.make_citekey( summary, citekeysDB )
    citekey = CK.enforce_unique_citekey( citekey, citekeysDB )
    
    '''
      TD:
       - If the citekey was already created check if it seems like the same work
       - Search for related preprints or DOIs 
       - Look for .pdf versions on the web 
       - Autodetect if it is a book or paper  
    '''
    
    with open(os.path.join( config.responses_dir, f'{ citekey }.json' ), 'w') as json_file:
      json.dump( response, json_file, indent = 2 )

    if config.autodownload_papers:
      OPENLIB.download_pdf( citekey, summary, config )
    
    cite_as = BIBTEX.bibtex_book( citekey, summary )
    citekeysDB.add_main_id( citekey, 'book', isbn, 'openlib-isbn', cite_as )    
    describe_new_ref( citekey, summary )
    

if __name__ == '__main__':

  isbn = sys.argv[1] 
  citekeysDB = DB.database( CFG.config.db_file )
  add_isbn( isbn, citekeysDB, CFG.config )  

