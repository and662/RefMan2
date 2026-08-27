
(setq refman-papers-dir   "~/01-Notes/References/Papers")
(setq refman-books-dir    "~/01-Notes/References/Books")
(setq refman-websites-dir "~/01-Notes/References/Websites")
(setq refman-db-dir       "~/01-Notes/References/citekeys.db")


;; TD: increment the last accessed date when opening 
(defun refman-citekeys-menu ()
  "Open an ivy minibuffer for selecting a citekey"
	(interactive)
	(let* ((ck-database (sqlite-open refman-db-dir ))
	  		 (citekeys-list (sqlite-select ck-database "SELECT Citekey FROM \"Accessed Date\" ORDER BY \"Last Accessed\" DESC;"))
				 (selected-citekey (ivy-read "Select a Citekey: " citekeys-list)))
		(sqlite-close ck-database)
		(selected-citekey)))

(defun refman-open-citekeys ()
	"Open the citekey file" 
	(interactive)
	(let* ((ck-database (sqlite-open refman-db-dir ))
				 (citekeys-list (sqlite-select ck-database "SELECT Citekey FROM \"Accessed Date\" ORDER BY \"Last Accessed\" DESC;"))
				 (selected-citekey (ivy-read "Select a Citekey: " citekeys-list))
				 (content-type (sqlite-select ck-database (format "SELECT \"Content Type\" FROM \"Main Identifier\" WHERE \"Citekey\" = \"%s\";" selected-citekey)))
				 (ref-file-path 
					 (cond ((string= (car (car content-type)) "paper")   (format "%s/%s.pdf" refman-papers-dir   selected-citekey))
								 ((string= (car (car content-type)) "book")    (format "%s/%s.pdf" refman-books-dir    selected-citekey))
								 ((string= (car (car content-type)) "website") (format "%s/%s.pdf" refman-websites-dir selected-citekey)))))
		(sqlite-close ck-database)
		(shell-command (format "zathura %s" ref-file-path))))

(defun refman-create-link ()
	"Create a link to the file" 
	(interactive)
	(let* ((ck-database (sqlite-open refman-db-dir ))
				 (citekeys-list (sqlite-select ck-database "SELECT Citekey FROM \"Accessed Date\" ORDER BY \"Last Accessed\" DESC;"))
				 (selected-citekey (ivy-read "Select a Citekey: " citekeys-list))
				 (content-type (sqlite-select ck-database (format "SELECT \"Content Type\" FROM \"Main Identifier\" WHERE \"Citekey\" = \"%s\";" selected-citekey)))
				 (ref-file-path 
					 (cond ((string= (car (car content-type)) "paper") (format "%s/%s.pdf" refman-papers-dir selected-citekey))
								 ((string= (car (car content-type)) "book") (format "%s/%s.pdf" refman-books-dir selected-citekey))
								 ((string= (car (car content-type)) "website") (format "%s/%s.pdf" refman-websites-dir selected-citekey)))))
		(sqlite-close ck-database)
		(insert (format "[[file:%s][%s]] " ref-file-path selected-citekey))))

(defun refman-command (refman)
  "Send a command to refman" 
  (interactive "sRefMan: ")
	(shell-command-to-string (format "ref %s" refman)))

