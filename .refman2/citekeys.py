
import os, sys, csv, json, datetime
from unidecode import unidecode
from collections import deque

import config as CFG
import database as DB
import bibtex as BIBTEX


def enforce_unique_citekey( citekey, citekeyDB ):

  ck_dne = False
  while ck_dne == False:
    ck_match = citekeyDB.find_matching_citekeys( citekey )
    if ck_match == None:
      ck_dne = True
    else:
      if len( ck_match ) == 1:
        result = ck_match[0]
        print( f'Citekey { citekey } already exists with id: { result[1] } of type "{ result[2] }" ' )
        valid_selection = False
        while valid_selection == False:
          selection = input( """Quit (q) or create (c) a different citekey for this reference? """ )
          if selection in [ 'Q', 'q', 'Quit', 'quit', 'Exit', 'exit' ]:
            exit()
          elif selection in [ 'C', 'c', 'Create', 'create' ]:
            valid_selection = True
            citekey = input( 'Custom citekey: ' )
  
  return citekey 


def make_citekey( metadata_summary, citekeyDB ):

  def simplify_name( name ):
    if len( name ) == 1:
      # only one name was given for the author (try to detect a last name)
      name_components = name[0].split( ' ' )
      last_name = name_components[0].replace( '.', '' ) # no periods
      return unidecode( last_name ) # convert the result from unicode to ascii 
    else:
      # a lastname was specified 
      last_name = unidecode( name[0] )        # convert unicode to ascii 
      last_name = last_name.replace( ' ', '' ) # if they have multiple last names, remove spaces 
      last_name = last_name.replace( '.', '' ) # no periods 
      return last_name 

  author_list = metadata_summary['authors']
  
  first_author_lastname = simplify_name( author_list[0] )
  second_author_lastname = ''
  if len( author_list ) > 1:
    second_author_lastname = simplify_name( author_list[1] )
  
  year = str( metadata_summary['publication-date'] )[0:4]
  title = metadata_summary['title']
  
  citekey = CFG.citekey_template( first_author_lastname, second_author_lastname, year, title )
  return citekey


def ensure_citekey_exists( ckDB, citekey ):
  ck_rows = ckDB.db_row_select( 'Main Identifier', cols_in = { 'Citekey' : citekey } )
  if len( ck_rows ) == 0: 
    print( f'Citekey: { citekey } does not exist in the database' )
    exit()


def bibtex( ckDB, citekey ):
  ensure_citekey_exists( ckDB, citekey )
  ckDB.update_accessed_date( citekey )
  ck_rows = ckDB.db_row_select( 'Bibtex', cols_in = { 'Citekey' : citekey }, cols_out = [ 'Cite As' ] )
  for row in ck_rows:
    print( row[0] )


def open_pdf( citekey, citekeysDB, config ):

  results = citekeysDB.db.execute( f'SELECT "Content Type" FROM "Main Identifier" WHERE "Citekey" = "{ citekey }";' )
  results = list( results )
  content_type = results[0][0]

  match content_type:
    case 'paper':
      file_name = os.path.join( config.papers_dir, f'{ citekey }.pdf' )
    case 'book':
      file_name = os.path.join( config.books_dir, f'{ citekey }.pdf' )
    case 'website':
      file_name = os.path.join( config.websites_dir, f'{ citekey }.pdf' )
  
  # TD: check if there is actually a file there 
  os.system( f'{ config.pdf_viewer } { file_name }' )


if __name__ == '__main__':

  citekey = sys.argv[1] 
  citekeysDB = DB.database( CFG.config.db_file )
  print_citekey_info( citekeysDB, citekey )

              
