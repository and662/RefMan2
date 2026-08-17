
import sys, re, requests 

def check_scihub( doi ):

  doi = sys.argv[1]
  response = requests.get( f'https://sci-hub.box/{ doi }' )
  
  match response.status_code:
    case 200: 
      response_content = response.content.decode( 'utf-8' )
      str_matches = re.findall( r'/download/.+\.pdf', response_content )
      return True, str_matches 

    case 404: 
      return False, []

    case _:   
      return False, response.status_code
    
def scihub_download( download_url, file_name ):

  pdf_response = requests.get( f'https://sci-hub.box{ download_url }', stream = True )
  with open( file_name, 'wb' ) as f:
    for chunk in pdf_response.iter_content( 2000 ):
      f.write( chunk )

  return True

if __name__ == '__main__':

  doi = sys.argv[1] 
  found_match, url_matches = check_scihub( doi )

  if found_match:

    for url in url_matches:
      print( f'Possible download url: { url } ' )
      successful_download = scihub_download( url, 'Paper.pdf' )
      if successful_download:
        exit()

  elif url_matches == []:
    print( f'Did not find doi { doi } on scihub' )

  else:  
    print( f'Did not find doi { doi } on scihub, error code:' )
    print( url_matches )


'''
response = requests.get( 'https://sci-hub.box/10.1088/1367-2630/16/3/033034' )
print( response )
print( dir(response) )
print( response.content )

url = "https://sci-hub.box/download/2024/3970/1edf354ad50d7e7db8afb8c0e1c1b116/huang2014.pdf"
response = requests.get( url, stream = True )

with open( 'paper.pdf', 'wb' ) as f:
  for chunk in response.iter_content( 2000 ):
    f.write( chunk )
'''
    

