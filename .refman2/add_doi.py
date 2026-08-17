
import os, sys, json, time, datetime 
from collections import deque 

import urllib, logging, requests, arxiv, itertools
from requests.exceptions import HTTPError 

import config as CFG
import citekeys as CK
import bibtex as BIBTEX

import crossref_api as CROSSREF 
import datacite_api as DATACITE 
import arxiv_api as ARXIV 

import database as DB


def describe_new_ref( citekey, summary ):
  print( f'Created new reference with citekey: { citekey }' ) 
  # TD: print authors, title etc. 


def format_arXiv_id( doi ):
  if doi.startswith( 'arXiv:' ):
    return True, doi.removeprefix( 'arXiv:' )
  else:
    components = doi.split( '/arXiv.' )
    if len( components ) == 2:
      return True, components[1] 
  return False, doi 


def identifier_exists( doi, citekeysDB ):
  citekeys_match = citekeysDB.citekey_from_id( doi )
  if not citekeys_match == None:
    citekeysDB.update_accessed_date( citekeys_match[0] )
    print( f'The identifier { doi } (of type "{ citekeys_match[1] }") already has the citekey: { citekeys_match[0] }' )
    return True
  return False 


def add_doi( doi, citekey = None, citekeysDB = None, config = None, verbose_mode = False ):
  if config == None: 
    config = CFG.Config( config_file = None, verbose_mode = verbose_mode )
  if citekeysDB == None:
    citekeysDB = DB.database( None, config = None )

  # check if it's an arxiv id 
  is_arXiv, doi = format_arXiv_id( doi )
  
  # check if that doi is saved already 
  if identifier_exists( doi, citekeysDB ):
    return 
  
  if is_arXiv == False:
  
    # check crossref 
    response = CROSSREF.crossref_response( doi, config )
    if not response == {}:
      print( 'Found a match on crossref.org' )

      summary = CROSSREF.summarized_metadata( response )
      if citekey == None:
        citekey = CK.make_citekey( summary, citekeysDB ) 
      citekey = CK.enforce_unique_citekey( citekey, citekeysDB )
          
      '''
        TD:
         - If the citekey was already created check if it seems like the same work
         - Search for related preprints or ISBNs 
         - Look for .pdf versions on the web 
         - Autodetect if it is a book or paper 
      '''
      
      with open(os.path.join( config.responses_dir, f'{ citekey }.json' ), 'w') as json_file:
        json.dump( response, json_file, indent = 2 )
      
      if config.autodownload_papers:
        CROSSREF.download_pdf( citekey, summary, config )
      
      cite_as = BIBTEX.bibtex_article( citekey, summary )
      citekeysDB.add_main_id( citekey, 'paper', doi, 'crossref-doi', cite_as )
      describe_new_ref( citekey, summary )
      return
  
  
  # check the arxiv 
  responses = ARXIV.arXiv_doi_response( doi, config )
  # TD: loop over responses and look for related dois that are already saved
  # if one is found then append the arxiv-id to it and download the preprint 

  if len( responses ) > 0: # TD: detect related identifiers 

    response = responses[0] 
    print( 'Found a match on arxiv.org' )

    metadata = ARXIV.get_arXiv_metadata( response, config )
    if metadata['doi'] == '':
      metadata['doi'] = f'arXiv:{ doi }' 
    
    if citekey == None:
      citekey = CK.make_citekey( metadata, citekeysDB )
    citekey = CK.enforce_unique_citekey( citekey, citekeysDB )
    
    '''
      TD:
       - If the citekey was already created check if it seems like the same work
       - Search for related papers or ISBNs 
       - Autodetect if it is a book or paper 
    '''
    
    with open(os.path.join( config.responses_dir, f'{ citekey }.json' ), 'w') as json_file:
      json.dump( metadata, json_file, indent = 2 )
    
    if config.autodownload_papers:
      resource_name = ARXIV.save_paper_pdf( response, citekey, config )
    
    cite_as = BIBTEX.bibtex_article( citekey, metadata )
    citekeysDB.add_main_id( citekey, 'paper', doi, 'arxiv-id', cite_as )    
    describe_new_ref( citekey, metadata )
    return 

  print( f'The doi: { doi } was not found' )

if __name__ == '__main__':

  doi = sys.argv[1] 
  citekeysDB = DB.database( CFG.config.db_file )
  add_doi( doi, citekeysDB, CFG.config ) 

