
import os, sqlite3, datetime 
import config as CFG


class database:

  def __init__( self, db_name, config = None ):
    if db_name == None:
      db_name = 'citekeys.db'
    self.db_name = db_name 
    if os.path.isfile( db_name ):
      self.db = sqlite3.connect( db_name )
    else:
      self.new_db( db_name )
  
  def new_db( self, db_name ):
    # create a new database file from scratch 
    self.db = sqlite3.connect( db_name )
    self.db.execute( """CREATE TABLE IF NOT EXISTS "Main Identifier"(
                        Citekey TEXT PRIMARY KEY,
                        "Content Type" TEXT,
                        "Main Identifier" TEXT,
                        "Main Identifier Type" TEXT );""" )
    self.db.execute( """CREATE TABLE IF NOT EXISTS "Related Identifiers"(
                        Number INTEGER PRIMARY KEY,
                        Citekey TEXT,
                        "Content Type" TEXT,
                        "Related Identifier" TEXT,
                        "Related Identifier Type" TEXT );""" )
    self.db.execute( """CREATE TABLE IF NOT EXISTS "Accessed Date"(
                        Citekey TEXT PRIMARY KEY,
                        "Last Accessed" TEXT,
                        "First Accessed" TEXT );""" )
    self.db.execute( """CREATE TABLE IF NOT EXISTS "Bibtex"(
                        Citekey TEXT PRIMARY KEY,
                        "Cite As" TEXT );""" )
 
   
  def add_main_id( self, citekey, content_type, main_id, main_id_type, cite_as ):
    # add a main identifier to the db 
    self.db.execute( "INSERT INTO 'Main Identifier' VALUES (?, ?, ?, ?); ",
                     (citekey, content_type, main_id, main_id_type) )
    date_time = datetime.datetime.today().strftime( "%Y-%m-%d %H:%M:%S" )
    self.db.execute( "INSERT INTO 'Accessed Date' VALUES (?, ?, ?); ",
                     (citekey, date_time, date_time) )
    self.db.execute( "INSERT INTO 'Bibtex' VALUES (?, ?); ", 
                     (citekey, cite_as) )
    self.db.execute( "COMMIT" )


  def update_accessed_date( self, citekey ):
    # update the "Last Accessed" column in the "Accessed Dates" table 
    date_time = datetime.datetime.today().strftime( "%Y-%m-%d %H:%M:%S" )
    self.db.execute( f'UPDATE "Accessed Date" SET "Last Accessed" = "{ date_time }" WHERE "Citekey" = "{ citekey }"; ' ) 
    self.db.execute( "COMMIT" )
 
 
  def change_citekey( self, old_citekey, new_citekey, config ):
    # note: this assumes "new_citekey" DNE in the DB    
    
    # change a citekey from "old_citekey" to "new_citekey"
    self.db.execute( f'UPDATE "Main Identifier" SET "Citekey" = "{ new_citekey }" WHERE "Citekey" = "{ old_citekey }"; ' ) 
    self.db.execute( f'UPDATE "Related Identifiers" SET "Citekey" = "{ new_citekey }" WHERE "Citekey" = "{ old_citekey }"; ' ) 
    self.db.execute( f'UPDATE "Accessed Date" SET "Citekey" = "{ new_citekey }" WHERE "Citekey" = "{ old_citekey }"; ' ) 
    self.db.execute( f'UPDATE "Bibtex" SET "Citekey" = "{ new_citekey }" WHERE "Citekey" = "{ old_citekey }"; ' )
    self.update_accessed_date( new_citekey )
    # rename the related resources 

    for folder in [ config.papers_dir, config.books_dir, config.websites_dir, config.responses_dir ]:
      for file_name in os.listdir( folder ):
        file_path = os.path.join( folder, file_name )
        if os.path.isfile( file_path ) and file_name.startswith( old_citekey ):
          new_file_path = os.path.join( folder, f'{ new_citekey }{ file_name.removeprefix( old_citekey ) }' ) 
          os.rename( file_path, new_file_path )
          if config.verbose_mode == True:
            print( f'Renamed "{ file_path }" to "{ new_file_path }"' )
  
  def delete_citekey( self, citekey, config ):
    # delete the resources
    for folder in [ config.papers_dir, config.books_dir, config.websites_dir, config.responses_dir ]:
      for file_name in os.listdir( folder ):
        file_path = os.path.join( folder, file_name )
        if os.path.isfile( file_path ) and file_name.startswith( citekey ):
          os.remove( file_path )
          if config.verbose_mode == True:
            print( f'Removed: "{ file_path }"' )
    # delete a citekey from the database
    self.db.execute( f'DELETE FROM "Main Identifier" WHERE "Citekey" = "{ citekey }";' )
    self.db.execute( f'DELETE FROM "Related Identifiers" WHERE "Citekey" = "{ citekey }";' )
    self.db.execute( f'DELETE FROM "Accessed Date" WHERE "Citekey" = "{ citekey }";' )
    self.db.execute( f'DELETE FROM "Bibtex" WHERE "Citekey" = "{ citekey }";' )
    self.db.commit()


  def db_row_select( self, table_name, cols_in = {}, cols_out = [] ):
    # select a row in table "table_name" 
    cols_out_str = '*'
    if not cols_out == []:
      cols_out_str = ','.join([ f'"{ s }"' for s in cols_out ])
    cols_in_str = '';
    if not cols_in == {}:
      settings = [ f'"{ k }" = "{ v }"' for k, v in cols_in.items() ]
      cols_in_str = ' AND '.join( settings )
    # create a selection:
    command = f'SELECT { cols_out_str } FROM "{ table_name }" WHERE { cols_in_str };'
    result = self.db.execute( command )
    return list( result )
    
  
  def citekey_from_id( self, identifier ):
    # find the citekey associated to an identifier 
    main_citekeys = self.db_row_select( 
      'Main Identifier', 
      cols_in = { 'Main Identifier' : identifier },   
      cols_out = [ 'Citekey', 'Main Identifier Type' ] )
    related_citekeys = self.db_row_select( 
      'Related Identifiers', 
      cols_in = { 'Main Identifier' : identifier },   
      cols_out = [ 'Citekey', 'Related Identifier Type' ] )

    all_citekeys = main_citekeys + related_citekeys
    if len( all_citekeys ) == 0:
      # no match 
      return None 
    elif len( all_citekeys ) > 1:
      # too many matches 
      all_ck_rmD = list(set( all_citekeys ))
      if len( all_ck_rmD ) == 1:
        print( f'Error: The citekey { all_ck_rmD[0][0] } of identifier type { all_ck_rmD[0][1] } is saved { len( all_citekeys ) } times with the same identifer: { identifier }' )
      else: 
        print( f'Error: The identifier: { identifier }, is saved { len( all_citekeys) } times with duplicate citekeys: { ", ".join([ v[0] for v in all_ck_rmD ]) }' )
    # TD: handle the above errors in some way... 

    # if we got here then there is only one match 
    return all_citekeys[0]


  def find_matching_citekeys( self, citekey ):
    # look up the row in the "Main Identifier" and "Realated Identifiers" corresponing to the citekey  
    main_citekeys = self.db_row_select( 
      'Main Identifier', 
      cols_in = { 'Citekey' : citekey },   
      cols_out = [ 'Citekey', 'Main Identifier', 'Main Identifier Type' ] )

    if len( main_citekeys ) == 0:
      # no match, ie. the citekey DNE in the DB 
      return None 
    elif len( main_citekeys ) > 1:
      # more than one match, ie. there is a problem... 
      all_ck_rmD = list(set( main_citekeys ))
      if len( all_ck_rmD ) == 1:
        print( f'Error: The citekey { all_ck_rmD[0][0] } is saved { len( main_citekeys ) } times with the same identifer: { identifier }' )
      else: 
        print( f'Error: The identifier: { identifier }, is saved { len( main_citekeys) } times with duplicate citekeys: { ", ".join([ v[0] for v in all_ck_rmD ]) }' )
    # TD: handle the above errors in some way... 
    
    # if we got here there is only one match 
    ck_match = [ main_citekeys[0] ]    
    related_citekeys = self.db_row_select( 
      'Related Identifiers', 
      cols_in = { 'Citekey' : citekey },   
      cols_out = [ 'Citekey', 'Related Identifier', 'Related Identifier Type' ] )

    return ck_match + list( related_citekeys )


if __name__ == '__main__':
  
  config = CFG.config 
  citekeysDB = database( CFG.config.db_file )

