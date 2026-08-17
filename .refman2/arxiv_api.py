
import os, sys, json, time, datetime 
from collections import deque 

import urllib, logging, requests, arxiv, itertools
from requests.exceptions import HTTPError 

import config as CFG
import citekeys as CK


def arXiv_doi_response( arXiv_id, config ):
  
  time.sleep( config.api_rate_lim )  
  client = arxiv.Client()
  search = arxiv.Search(id_list = [ arXiv_id ])
  
  try:
  
    results_list = list(client.results( search ))
    if len( results_list ) == 0:
      return {}
    return results_list

  except HTTPError as error:
    return {}
  except Exception as exc: # Catch other potential errors like network issues
    # print( f'An unexpected error occurred: { exc }' )
    return {}


def get_arXiv_metadata( arXiv_result, configuration ):
  
  def format_str( item ):
    if item == None:
      return ''
    else:
      return str( item )
  
  doi_metadata = {}
  doi_metadata[ 'entry_id' ]         = format_str( arXiv_result.entry_id )
  doi_metadata[ 'updated' ]          = arXiv_result.updated.strftime( '%Y-%m-%d %H:%M:%S' )
  doi_metadata[ 'publication-date' ] = arXiv_result.published.strftime( '%Y-%m-%d %H:%M:%S' )
  doi_metadata[ 'title' ]            = format_str( arXiv_result.title )
  doi_metadata[ 'summary' ]          = format_str( arXiv_result.summary )
  doi_metadata[ 'comment' ]          = format_str( arXiv_result.comment )
  doi_metadata[ 'journal_ref' ]      = format_str( arXiv_result.journal_ref )
  doi_metadata[ 'doi' ]              = format_str( arXiv_result.doi )
  doi_metadata[ 'primary_category' ] = format_str( arXiv_result.primary_category )
  
  author_list = deque([])
  for author in arXiv_result.authors:
    # for consistency: print last name first 
    author_name = author.name
    author_name_components = author_name.split( ' ' )
    author_name = ' '.join( author_name_components[::-1] )
    author_list.append([ author_name ])
  doi_metadata[ 'authors' ] = list( author_list ) 
  
  categories_list = deque([])
  for category in arXiv_result.categories:
    categories_list.append( category )
  doi_metadata[ 'categories' ] = list( categories_list )

  links_list = []
  for link in arXiv_result.links:
    link_dict = {} 
    link_dict[ 'href' ] = link.href 
    link_dict[ 'title' ] = format_str( link.title ) 
    link_dict[ 'rel' ] = link.rel 
    link_dict[ 'content_type' ] = format_str( link.content_type ) 
  doi_metadata[ 'links' ] = link_dict 
  
  return doi_metadata   


def save_paper_pdf( result, citekey, config ):
  todays_date = datetime.datetime.today().strftime( "%Y-%m-%d" )
  resource_name = f'{ citekey }_preprint.pdf'
  result.download_pdf( dirpath = config.papers_dir, 
                       filename = resource_name, 
                       download_domain = 'export.arxiv.org' )
  return resource_name


