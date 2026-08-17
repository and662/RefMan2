
import os, sys, json, time, datetime 
from collections import deque 

import urllib, logging, requests, arxiv, itertools
from requests.exceptions import HTTPError 

import config as CFG
import citekeys as CK
import database as DB
import bibtex as BIBTEX


def prompt_url_metadata( citekey, url ):

  metadata = {}
  metadata[ 'url' ] = url 
  metadata[ 'urldate' ] = datetime.datetime.today().strftime( "%Y-%m-%d" )
  NA_options = [ 'na', 'NA', 'N.A.', 'n.a', 'na.', 'NA.' ]

  author_list = input( 'Author(s): ' )
  if not author_list in NA_options:
    author_list = author_list.split( ',' )
    for n, author in enumerate( author_list ):
      author = [ name for name in author.split( ' ' ) if not name == '' ]
      author_list[n] = author  
    metadata[ 'authors' ] = author_list 

  title = input( 'Title: ' )
  if not title in NA_options:
    metadata[ 'title' ] = title 

  year = input( 'Year: ' )
  if not year in NA_options:
    metadata[ 'year' ] = year 
  
  return metadata     


def add_url( url, citekey = None, citekeysDB = None, config = None, verbose_mode = False ):

  if config == None: 
    config = CFG.Config( config_file = None, verbose_mode = verbose_mode )
  if citekeysDB == None:
    citekeysDB = DB.database( None, config = None )
  
  # check if that url is saved already 
  citekeys_match = citekeysDB.citekey_from_id( url )
  if not citekeys_match == None:
    citekeysDB.update_accessed_date( citekeys_match[0] )
    print( f'The identifier { url } (of type "{ citekeys_match[1] }") already has the citekey: { citekeys_match[0] }' )
    return 
  
  # prompt the user for a citekey 
  if citekey == None:
    citekey = input( 'Citekey: ' )
  citekey = CK.enforce_unique_citekey( citekey, citekeysDB )
  metadata = prompt_url_metadata( citekey, url )
  
  save_to_folder = os.path.join( config.websites_dir, citekey )
  if not os.path.exists( save_to_folder ):
    os.makedirs( save_to_folder )
  os.system( f'wget ‐‐page-requisites ‐‐span-hosts ‐‐convert-links ‐‐adjust-extension -P { save_to_folder } { url }' )
  contents = os.listdir( save_to_folder )
  if len( contents ) == 0:
    print( f'Error: Failed to download the link: { url }' )
    os.system( f'rm -r { save_to_folder }' )
  elif len( contents ) == 1:
    print( contents )

  with open(os.path.join( config.responses_dir, f'{ citekey }.json' ), 'w') as json_file:
    json.dump( metadata, json_file, indent = 2 )
  
  cite_as = BIBTEX.bibtex_online( citekey, metadata )
  citekeysDB.add_main_id( citekey, 'website', url, 'url', cite_as )

  return 
  

if __name__ == '__main__':

  url = sys.argv[1]   
  citekeysDB = DB.database( CFG.config.db_file )
  add_url( url, citekeysDB, CFG.config ) 

