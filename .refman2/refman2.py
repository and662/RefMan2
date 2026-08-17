import os, sys, argparse

import config as CFG
import citekeys as CK
import database as DB

import add_doi as ADD_DOI
import add_isbn as ADD_ISBN 
import add_url as ADD_URL


class RefMan2:

  def __init__( self, database = None, config_file = None, verbose_mode = False ):
    self.config = CFG.Config( config_file = config_file, verbose_mode = verbose_mode )
    self.citekeysDB = DB.database( database, config = self.config )

  def bibtex( self, citekey ):
    CK.bibtex( self.citekeysDB, citekey )

  def add_doi( self, doi, citekey = None ):
    ADD_DOI.add_doi( doi, citekey = citekey, citekeysDB = self.citekeysDB, config = self.config )

  def add_isbn( self, isbn, citekey = None ):
    ADD_ISBN.add_isbn( isbn, citekey = citekey, citekeysDB = self.citekeysDB, config = self.config )

  def add_url( self, url, citekey = None ):
    ADD_URL.add_url( url, citekey = citekey, citekeysDB = self.citekeysDB, config = self.config )

  def rename( self, old_citekey, new_citekey ):
    CK.ensure_citekey_exists( self.citekeysDB, old_citekey )
    if old_citekey == new_citekey:
      print( 'Error: This is the same citekey' )  
    new_citekey = CK.enforce_unique_citekey( new_citekey, self.citekeysDB )
    self.citekeysDB.change_citekey( old_citekey, new_citekey, self.config )
   
  def remove( self, citekey ): 
    CK.ensure_citekey_exists( self.citekeysDB, citekey )
    self.citekeysDB.delete_citekey( citekey, self.config )

  def list( self ):
    print( 'TD: set up listing of citekeys' )


citekey_parser = argparse.ArgumentParser( prog = 'REFMAN2', 
  description = 'RefMan2 is a reference manager for tracking articles, books, academic papers, and websites' )
citekey_parser.add_argument( 'citekey',            type = str, nargs = '+', help = 'Print a summary of the following citekey(s)' )
citekey_parser.add_argument( '--verbose',  '-v',   action = 'store_true',   help = 'Enable verbose mode' )
citekey_parser.add_argument( '--config',   '-cfg', type = str,   help = 'Path of the configuration folder' )
citekey_parser.add_argument( '--database', '-db',  type = str,   help = 'Path of the SQLite database' )

bibtex_parser = argparse.ArgumentParser( prog = 'REFMAN2 bibtex', 
  description = 'A menu for printing a bibtex citation for the specified citekey(s)' )
bibtex_parser.add_argument( 'citekey',            type = str, nargs = '+', help = 'One or more citekeys' )
bibtex_parser.add_argument( '--verbose',  '-v',   action = 'store_true',   help = 'Enable verbose mode' )
bibtex_parser.add_argument( '--config',   '-cfg', type = str,  help = 'Path of the configuration folder' )
bibtex_parser.add_argument( '--database', '-db',  type = str,  help = 'Path of the SQLite database' )

doi_parser = argparse.ArgumentParser( prog = 'REFMAN2 add-doi', 
  description = 'A menu for adding a DOI to the database' )
doi_parser.add_argument( 'doi',                type = str, nargs = '+', help = 'One or more DOIs' )
doi_parser.add_argument( '--citekey',  '-ck',  type = str, nargs = '+', help = 'One or more citekeys' )
doi_parser.add_argument( '--verbose',  '-v',   action = 'store_true',   help = 'Enable verbose mode' )
doi_parser.add_argument( '--config',   '-cfg', type = str,   help = 'Path of the configuration folder' )
doi_parser.add_argument( '--database', '-db',  type = str,   help = 'Path of the SQLite database' )

isbn_parser = argparse.ArgumentParser( prog = 'REFMAN2 add-isbn', 
  description = 'A menu for adding a ISBN to the database' )
isbn_parser.add_argument( 'isbn',                type = str, nargs = '+', help = 'One or more ISBNs' )
isbn_parser.add_argument( '--citekey',  '-ck',  type = str, nargs = '+', help = 'One or more citekeys' )
isbn_parser.add_argument( '--verbose',  '-v',   action = 'store_true',   help = 'Enable verbose mode' )
isbn_parser.add_argument( '--config',   '-cfg', type = str,  help = 'Path of the configuration folder' )
isbn_parser.add_argument( '--database', '-db',  type = str,  help = 'Path of the SQLite database' )

url_parser = argparse.ArgumentParser( prog = 'REFMAN2 add-url', 
  description = 'A menu for adding a URL to the database' )
url_parser.add_argument( 'url',                type = str, nargs = '+', help = 'One or more URLs' )
url_parser.add_argument( '--citekey',  '-ck',  type = str, nargs = '+', help = 'One or more citekeys' )
url_parser.add_argument( '--verbose',  '-v',   action = 'store_true',   help = 'Enable verbose mode' )
url_parser.add_argument( '--config',   '-cfg', type = str,   help = 'Path of the configuration folder' )
url_parser.add_argument( '--database', '-db',  type = str,   help = 'Path of the SQLite database' )

rm_parser = argparse.ArgumentParser( prog = 'REFMAN2 remove', 
  description = 'A menu for removing one or more citekeys from the database' )
rm_parser.add_argument( 'citekey',            type = str, nargs = '+', help = 'One or more citekeys' )
rm_parser.add_argument( '--verbose',  '-v',   action = 'store_true',   help = 'Enable verbose mode' )
rm_parser.add_argument( '--config',   '-cfg', type = str,   help = 'Path of the configuration folder' )
rm_parser.add_argument( '--database', '-db',  type = str,   help = 'Path of the SQLite database' )

mv_parser = argparse.ArgumentParser( prog = 'REFMAN2 rename', 
  description = 'A menu for renaming a citekey in the database' )
mv_parser.add_argument( 'citekey',            type = str, nargs = 2, help = 'The name of the old citekey followed by the name of the new citekey' )
mv_parser.add_argument( '--verbose',  '-v',   action = 'store_true', help = 'Enable verbose mode' )
mv_parser.add_argument( '--config',   '-cfg', type = str,  help = 'Path of the configuration folder' )
mv_parser.add_argument( '--database', '-db',  type = str,  help = 'Path of the SQLite database' )

ls_parser = argparse.ArgumentParser( prog = 'REFMAN2 list', 
  description = 'A menu listing relevant citekeys' )
group = ls_parser.add_mutually_exclusive_group()
group.add_argument( '--last-accessed',  '-la', nargs = '?', type = int, const = -1, help = 'List in the order of last accessed' )
group.add_argument( '--first-accessed', '-fa', nargs = '?', type = int, const = -1, help = 'List in the order of first accessed' )
ls_parser.add_argument( '--verbose',  '-v',   action = 'store_true',                help = 'Enable verbose mode' )
ls_parser.add_argument( '--config',   '-cfg', type = str,               help = 'Path of the configuration folder' )
ls_parser.add_argument( '--database', '-db',  type = str,               help = 'Path of the SQLite database' )


if __name__ == '__main__':
  
  if len(sys.argv) == 0:
    exit()
  
  match sys.argv[1]:
    case 'bibtex':
      bibtex_args = bibtex_parser.parse_args(sys.argv[2:])
      refman2 = RefMan2( database = bibtex_args.database, config_file = bibtex_args.config, verbose_mode = bibtex_args.verbose )
      for ck_num, citekey in enumerate( bibtex_args.citekey ):
        if ck_num > 0:
          print( '' )
        refman2.bibtex( citekey )
    
    case 'add-doi':
      doi_args = doi_parser.parse_args(sys.argv[2:])
      refman2 = RefMan2( database = doi_args.database, config_file = doi_args.config, verbose_mode = doi_args.verbose )
      if not doi_args.citekey == None:
        if len( doi_args.doi ) == len( doi_args.citekey ):
          for doi, citekey in zip( doi_args.doi, doi_args.citekey ): 
            refman2.add_doi( doi, citekey )
        elif len( doi_args.citekey ) == 1:
          main_doi = doi_args.doi[0] 
          citekey = doi_args.citekey[0] 
          refman2.add_doi( main_doi, citekey )
          for doi in doi_args.doi[1:]:
            print( f'TD: add DOI { doi } as related identifier to citekey { citekey }' )
        else:
          print( 'Error: Ambiguous input, cannot match the number of citekeys to DOIs' )
      else:
        for doi in doi_args.doi:
          refman2.add_doi( doi )
  
    case 'add-isbn':
      isbn_args = isbn_parser.parse_args(sys.argv[2:])
      refman2 = RefMan2( database = isbn_args.database, config_file = isbn_args.config, verbose_mode = isbn_args.verbose )
      if not isbn_args.citekey == None:
        if len( isbn_args.isbn ) == len( isbn_args.citekey ):
          for isbn, citekey in zip( isbn_args.isbn, isbn_args.citekey ): 
            refman2.add_isbn( isbn, citekey )
        elif len( isbn_args.citekey ) == 1:
          main_isbn = isbn_args.isbn[0] 
          citekey = isbn_args.citekey[0] 
          refman2.add_isbn( main_isbn, citekey )
          for isbn in isbn_args.isbn[1:]:
            print( f'TD: add ISBN { isbn } as related identifier to citekey { citekey }' )
        else:
          print( 'Error: Ambiguous input, cannot match the number of citekeys to ISBNs' )
      else:
        for isbn in isbn_args.isbn:
          refman2.add_isbn( isbn )
    
    case 'add-url':
      url_args = url_parser.parse_args(sys.argv[2:])
      refman2 = RefMan2( database = url_args.database, config_file = url_args.config, verbose_mode = url_args.verbose )
      if not url_args.citekey == None:
        if len( url_args.url ) == len( url_args.citekey ):
          for url, citekey in zip( url_args.url, url_args.citekey ): 
            refman2.add_url( url, citekey )
        elif len( url_args.citekey ) == 1:
          main_url = url_args.url[0] 
          citekey = url_args.citekey[0] 
          refman2.add_url( main_url, citekey )
          for url in url_args.url[1:]:
            print( f'TD: add URL { url } as related identifier to citekey { citekey }' )
        else:
          print( 'Error: Ambiguous input, cannot match the number of citekeys to URLs' )
      else:
        for url in url_args.url:
          refman2.add_url( url )
    
    case 'remove':
      rm_args = rm_parser.parse_args(sys.argv[2:])
      refman2 = RefMan2( database = rm_args.database, config_file = rm_args.config, verbose_mode = rm_args.verbose )
      for citekey in rm_args.citekey:
        refman2.remove( citekey )
    
    case 'rename':
      mv_args = mv_parser.parse_args(sys.argv[2:])
      refman2 = RefMan2( database = mv_args.database, config_file = mv_args.config, verbose_mode = mv_args.verbose )
      old_citekey = mv_args.citekey[0]
      new_citekey = mv_args.citekey[1]
      refman2.rename( old_citekey, new_citekey )
  
    case 'list':
      ls_args = ls_parser.parse_args(sys.argv[2:])
      refman2 = RefMan2( database = ls_args.database, config_file = ls_args.config, verbose_mode = ls_args.verbose )
      if not ls_args.first_accessed == None:
        if ls_args.first_accessed == -1:
          print( 'TD: print all citekeys in the order that they were first accessed' )
        else:
          print( f'TD: print { ls_args.first_accessed } citekeys in the order that they were first accessed' )
      else:
        if ls_args.last_accessed in [-1, None]:
          print( 'TD: print all citekeys in the order that they were last accessed' )
        else:
          print( f'TD: print { ls_args.last_accessed } citekeys in the order that they were last accessed' )
  
    case _:
      citekey_args = citekey_parser.parse_args( sys.argv[1:] )
      refman2 = RefMan2( database = citekey_args.database, config_file = citekey_args.config, verbose_mode = citekey_args.verbose )
      for ck_num, citekey in enumerate( citekey_args.citekey ):
        if ck_num > 0:
          print( '' )
        refman2.bibtex( citekey )
  
