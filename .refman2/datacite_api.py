
import os, sys, json, time, datetime 
from collections import deque 

import urllib, logging, requests, arxiv, itertools
from requests.exceptions import HTTPError 

import config as CFG
import citekeys as CK


def datacite_response( doi, config ):

  time.sleep( config.api_rate_lim )  
  datacite_url = f"https://api.datacite.org/dois/{ doi }"
  try:
    response = urllib.request.urlopen( datacite_url )
    response = json.loads(response.read().decode( 'utf-8' ))

  except HTTPError as error:
    return {}

  except Exception as exc: # Catch other potential errors like network issues
    # print( f'The api.datacite.org website produced an unexpected error: { exc }' )
    return {}
    
  return response 


def summarized_metadata( metadata ):
  
  data = metadata[ 'data' ]
  all_keys = data.keys()
  summary = {}

  if 'id' in all_keys:
    summary[ 'doi' ] = data[ 'id' ]

  if 'attributes' in all_keys:
    attribute = data[ 'attributes' ]
    all_keys = attribute.keys()

    if 'creators' in all_keys:
      authors = attribute[ 'creators' ]
      author_list = deque([])    
      
      for author in authors:

        author_keys = author.keys()
        if ('givenName' in author_keys) and ('familyName' in author_keys):
          author_list.append([ author[ 'familyName' ], 
                               author[ 'givenName' ]  ]) 
        elif 'name' in author_keys:
          author_list.append([ author[ 'name' ] ]) 
      
      summary[ 'authors' ] = list( author_list )
    
  if 'titles' in all_keys:
    summary[ 'title' ] = attribute[ 'titles' ][0][ 'title' ]

  if 'dates' in all_keys:
    date_str = attribute[ 'dates' ][0][ 'date' ]
    pub_date = datetime.datetime.strptime( date_str, '%Y-%m-%dT%H:%M:%SZ' )
    date_str = pub_date.strftime( "%Y-%m-%d" ) # reformat it for consistency 
    summary[ 'publication-date' ] = date_str
    
  elif 'publicationYear' in all_keys:
    summary[ 'publication-date' ] = attribute[ 'publicationYear' ]
  
  if 'url' in all_keys:
    summary[ 'url' ] = attribute[ 'url' ]

  if 'publisher' in all_keys:
    summary[ 'publisher' ] = attribute[ 'publisher' ]

  return summary


def save_metadata_json( metadata, citekey, config ):
  
  with open( f'responses/{ citekey }.json', 'w') as json_file:
    json.dump( metadata, mdfile )


def add_doi( datacite_doi, configuration ):
  
  citekeys_table = CK.get_citekeys_table( configuration )
  
  matching_indices = [ idx for idx, row in enumerate(citekeys_table) if row[1] == datacite_doi ]
  if not matching_indices == []:
    matching_ck = [ row[0] for row in citekeys_table[matching_indices] ]
    matching_ck = list(set( matching_ck )) # remove duplicates
  
    if len( matching_ck ) == 1:
      print( f"DOI: { datacite_doi } already has citekey: { matching_ck }" )
      exit()

    elif len( matching_ck ) > 1:
      print( f"DOI: { datacite_doi } already has citekeys: { ', '.join( matching_ck ) }" )
      exit()
  
  
  found_data, doi_metadata = get_doi_metadata( datacite_doi, configuration ) 
  if found_data:
    print( 'Found a match in datacite' )
  else: 
    return None 

  summary = summarized_metadata( doi_metadata )
  
  # TD: look for associated papers 
  # TD: check for conflicting citekeys again (in case of renaming)

  citekey = CK.make_citekey( summary )
  save_metadata_json( doi_metadata, citekey, configuration )
  
  todays_date = datetime.datetime.today().strftime( "%Y-%m-%d" )
  citekeys_table.append([ citekey, datacite_doi, 'doi', 'NULL', 'NULL', todays_date ]) 
  
  CK.save_citekeys_table( citekeys_table, configuration )
  


