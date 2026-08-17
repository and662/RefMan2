
import os 

class Config:
  
  def __init__( self, config_file = None, verbose_mode = False ):

    self.verbose_mode = verbose_mode 

    # Set default values 
    self.use_crossref = True
    self.use_datacite = True
    self.use_arxiv    = True
    
    # self.db_file = 'citekeys.db'     
    self.papers_dir    = '../Papers'
    self.books_dir     = '../Books'
    self.websites_dir  = '../Websites'
    self.responses_dir = '../.responses'
    
    # self.pdf_viewer = 'zathura' 

    self.autodownload_papers = True
    self.autodownload_books  = True
    self.autodownload_scihub = False # in case you like copyright law 
    self.autodownload_libgen = False # in case you like copyright law
    
    # the following are used by the various APIs
    self.api_rate_lim   = 0.5 
    self.api_user_agent = '' 
    self.api_mailto     = ''
    
    # Modify the default values with the config file
    if not config_file == None:
      print( f'TD: load the following config file: { config_file }' )

    # Make sure the correct directories exist:
    for required_folder in [self.papers_dir, self.books_dir, self.websites_dir, self.responses_dir]:
      if not os.path.exists( required_folder ):
        os.makedirs( required_folder )
        if self.verbose_mode:
          print( f'Created the folder: { required_folder }' )
    

# feel free to modify the template 
def citekey_template( fist_author_lastname, second_author_lastname, year, title ):

  ''' for a really verbose citekey:
  if second_author_lastname == '':
    return f'{ fist_author_lastname }{ year }'
  return f'{ fist_author_lastname }-{ second_author_lastname }{ year }'
  '''
  return f'{ fist_author_lastname }{year}' 



