
import config as CFG
import citekeys as CK
import database as DB

import add_doi as ADD_DOI
import add_isbn as ADD_ISBN 
import add_url as ADD_URL


config = CFG.Config( config_file = None, verbose_mode = True )
citekeysDB = DB.database( '../citekeys_test.db', config = config )

# BCS superconductivity paper
ADD_DOI.add_doi( '10.1103/PhysRev.106.162', citekeysDB = citekeysDB, config_file = config )  

# TBG Superconductivity paper 
ADD_DOI.add_doi( '10.1038/nature26160', citekeysDB = citekeysDB, config_file = config )

# Perelman papers
ADD_DOI.add_doi( 'math/0211159', citekeysDB = citekeysDB, config_file = config )  
ADD_DOI.add_doi( 'math/0303109', citekeysDB = citekeysDB, config_file = config )  
# ADD_DOI.add_doi( 'math/0307245', citekeysDB = citekeysDB, config_file = config )  

# Peskin & Schroeder 
ADD_ISBN.add_isbn( '0201503972', citekeysDB = citekeysDB, config_file = config )  

# Jackson Electrodynamics 
ADD_ISBN.add_isbn( '0-471-30932-X', citekeysDB = citekeysDB, config_file = config )

# Xiao Gang Wen Topological QFT 
ADD_ISBN.add_isbn( '019922725X', citekeysDB = citekeysDB, config_file = config )

# Algebraic Topology by Hatcher 
ADD_ISBN.add_isbn( '0521795400', citekeysDB = citekeysDB, config_file = config )

# Org Chem by Czako and Kurti 
ADD_ISBN.add_isbn( '0123694833', citekeysDB = citekeysDB, config_file = config )

# Bernevig's superconductivity book
ADD_ISBN.add_isbn( '069115175X', citekeysDB = citekeysDB, config_file = config )


