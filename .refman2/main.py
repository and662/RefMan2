
import sys, os 

import config as CFG
import citekeys as CK
import database as DB

import add_doi as ADD_DOI
import add_isbn as ADD_ISBN 
import add_url as ADD_URL


if __name__ == '__main__':

  citekeysDB = DB.database( CFG.config.db_file )
  config = CFG.config  

  if len( sys.argv ) == 1:
    print( 'TD: print a help menu' ) 
    exit() 

  elif len( sys.argv ) == 3:
    match sys.argv[1]:
      case '--add-doi': 
        ADD_DOI.add_doi( sys.argv[2], citekeysDB, config )
        exit() 
      
      case '--add-isbn':
        ADD_ISBN.add_isbn( sys.argv[2], citekeysDB, config )
        exit() 
      
      case '--add-url': 
        ADD_URL.add_url( sys.argv[2], citekeysDB, config )
        exit() 
      
      case '--delete':
        CK.ensure_citekey_exists( citekeysDB, sys.argv[2] )
        citekeysDB.delete_citekey( sys.argv[2], config )
        exit() 

      case '--open':
        CK.ensure_citekey_exists( citekeysDB, sys.argv[2] )
        CK.open_pdf( sys.argv[2], citekeysDB, config )
        exit()

  elif len( sys.argv ) == 4:
    match sys.argv[1]:
    
      case '--rename':
        old_citekey = sys.argv[2]
        new_citekey = sys.argv[3]
        CK.ensure_citekey_exists( citekeysDB, old_citekey )
        # do nothing if the same citekey was entered 
        if old_citekey == new_citekey:
          print( 'This is the same citekey' )
          exit()
        new_citekey = CK.enforce_unique_citekey( new_citekey, citekeysDB )
        citekeysDB.change_citekey( old_citekey, new_citekey, config )
        exit() 
  
  for citekey in sys.argv[1:]:
    CK.print_citekey_info( citekeysDB, citekey )


