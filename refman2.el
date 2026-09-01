
(setq refman-papers-dir   "References/Papers")
(setq refman-books-dir    "References/Books")
(setq refman-websites-dir "References/Websites")
(setq refman-db-dir       "References/.refman/citekeys.db")


(defun refman-update-last-accessed-db (citekey ck-database)
  "Update when a given citekey was last accessed from a given database" 
  (let* ((date-time-str (format-time-string "%Y-%m-%d %H:%M:%S")))
    (sqlite-execute ck-database (format "UPDATE \"Accessed Date\" SET \"Last Accessed\" = \"%s\" WHERE \"Citekey\" = \"%s\"; " date-time-str citekey)) ))


(defun refman-update-last-accessed (citekey)
  "Update when a given citekey was last accessed"
  (let* ((ck-database (sqlite-open refman-db-dir)))
    (progn (refman-update-last-accessed-db citekey ck-database)
           (sqlite-close db)) ))


(defun refman-citekeys-menu ()
  "Open an ivy minibuffer for selecting a citekey"
	(interactive)
	(let* ((ck-database (sqlite-open refman-db-dir ))
	  		 (citekeys-list (sqlite-select ck-database "SELECT Citekey FROM \"Accessed Date\" ORDER BY \"Last Accessed\" DESC;"))
				 (selected-citekey (ivy-read "Select a Citekey: " citekeys-list)))
		(progn (sqlite-close ck-database)
           (refman-update-last-accessed-db selected-citekey ck-database))
		(selected-citekey)))


(defun refman-pdf-link ()
	"Create a link to the pdf of a citekey" 
	(interactive)
	(let* ((ck-database (sqlite-open refman-db-dir ))
				 (citekeys-list (sqlite-select ck-database "SELECT Citekey FROM \"Accessed Date\" ORDER BY \"Last Accessed\" DESC;"))
				 (selected-citekey (ivy-read "Select a Citekey: " citekeys-list))
				 (content-type (sqlite-select ck-database (format "SELECT \"Content Type\" FROM \"Main Identifier\" WHERE \"Citekey\" = \"%s\";" selected-citekey)))
				 (ref-file-path 
					 (cond ((string= (car (car content-type)) "paper") (format "%s/%s.pdf" refman-papers-dir selected-citekey))
								 ((string= (car (car content-type)) "book") (format "%s/%s.pdf" refman-books-dir selected-citekey))
								 ((string= (car (car content-type)) "website") (format "%s/%s.pdf" refman-websites-dir selected-citekey)))))
    (progn (refman-update-last-accessed-db selected-citekey ck-database)
		       (sqlite-close ck-database))
		(insert (format "[[file:%s][%s]] " ref-file-path selected-citekey))))


(defun refman-url-link ()
	"Create a link for the citekey which is a url" 
	(interactive)
	(let* ((ck-database (sqlite-open refman-db-dir ))
				 (citekeys-list (sqlite-select ck-database "SELECT Citekey FROM \"Accessed Date\" ORDER BY \"Last Accessed\" DESC;"))
				 (selected-citekey (ivy-read "Select a Citekey: " citekeys-list))
				 (db-result (nth 0 (sqlite-select ck-database (format "SELECT \"Main Identifier Type\", \"Main Identifier\" FROM \"Main Identifier\" WHERE \"Citekey\" = \"%s\";" selected-citekey))))
         (link-str (pcase (nth 0 db-result)
                     ("crossref-doi" (format "[[https://doi.org/%s][%s]]" (nth 1 db-result) selected-citekey))
                     ("arxiv-id"     (format "[[https://arxiv.org/abs/%s][%s]]" (nth 1 db-result) selected-citekey))
                     ("openlib-isbn" (format "[[https://www.worldcat.org/isbn/%s][%s]]" (nth 1 db-result) selected-citekey))
                     ("url"          (format "[[%s][%s]]" (nth 1 db-result) selected-citekey)))))
    (progn (refman-update-last-accessed-db selected-citekey ck-database)
		       (sqlite-close ck-database))
		(insert link-str)))


(defun refman-open ()
	"Open the pdf of a citekey if it exists" 
	(interactive)
	(let* ((ck-database (sqlite-open refman-db-dir))
				 (citekeys-list (sqlite-select ck-database "SELECT Citekey FROM \"Accessed Date\" ORDER BY \"Last Accessed\" DESC;"))
				 (selected-citekey (ivy-read "Select a Citekey: " citekeys-list))
				 (content-type (sqlite-select ck-database (format "SELECT \"Content Type\" FROM \"Main Identifier\" WHERE \"Citekey\" = \"%s\";" selected-citekey)))
				 (ref-file-path 
					 (cond ((string= (car (car content-type)) "paper")   (format "%s/%s.pdf" refman-papers-dir   selected-citekey))
								 ((string= (car (car content-type)) "book")    (format "%s/%s.pdf" refman-books-dir    selected-citekey))
								 ((string= (car (car content-type)) "website") (format "%s/%s.pdf" refman-websites-dir selected-citekey)) )))
    (progn (refman-update-last-accessed-db selected-citekey ck-database)
		       (sqlite-close ck-database))
    (start-process "view-pdf" nil "zathura" ref-file-path))) 


(defun refman-open-at-point ()
  "Will try to open the corresponding pdf of a refman link"
  (interactive)
  (if (org-in-regexp org-link-any-re)
    ;; There is an org link at point so check if it has a description: 
    (let* ((context (org-element-context))
           (begin   (org-element-property :contents-begin context))
           (end     (org-element-property :contents-end context)))
      (if (and begin end)
        ;; The link has a description so assume it's a citekey: 
				(let* ((citekey (buffer-substring-no-properties begin end))
               (ck-database (sqlite-open refman-db-dir))
               (content-types (sqlite-select ck-database 
                 (format "SELECT \"Content Type\" FROM \"Main Identifier\" WHERE \"Citekey\" = \"%s\";" citekey))))
          (progn (refman-update-last-accessed-db citekey ck-database)
		             (sqlite-close ck-database)
                 (if (null content-types)
                   ;; The description of this link is not in the database 
                   (progn (message (format "RefMan Error: %s is not a citekey, opening the link normally" citekey)) 
                          (org-open-at-point))
                   (let* ((first-db-result (nth 0 content-types))
                          (pdf-path (pcase (nth 0 first-db-result)
                            ("paper"   (format "%s/%s.pdf" refman-papers-dir   citekey))
                            ("book"    (format "%s/%s.pdf" refman-books-dir    citekey))
                            ("website" (format "%s/%s.pdf" refman-websites-dir citekey)))))
                     (start-process "view-pdf" nil "zathura" pdf-path) )) ))
				;; The link has no description so open the link target:
        (org-open-at-point)))
    ;; There is no org link at point so print an error: 
    (message "RefMan Error: There is no link at point")))


(defun refman-bib-cite ()
	"Create a citation of the form: \\cite{citekey}" 
	(interactive)
	(let* ((ck-database (sqlite-open refman-db-dir ))
				 (citekeys-list (sqlite-select ck-database "SELECT Citekey FROM \"Accessed Date\" ORDER BY \"Last Accessed\" DESC;"))
				 (selected-citekey (ivy-read "Select a Citekey: " citekeys-list)))
    (progn (refman-update-last-accessed-db selected-citekey ck-database)
		       (sqlite-close ck-database)
					 (insert (format "\\cite{%s}" selected-citekey)) )))


(defun refman-bibtex ()
	"Create a bibtex citation from a citekey" 
	(interactive)
	(let* ((ck-database (sqlite-open refman-db-dir ))
				 (citekeys-list (sqlite-select ck-database "SELECT Citekey FROM \"Accessed Date\" ORDER BY \"Last Accessed\" DESC;"))
				 (selected-citekey (ivy-read "Select a Citekey: " citekeys-list))
				 (bibtex-citation (nth 0 (sqlite-select ck-database (format "SELECT \"Cite As\" FROM Bibtex WHERE Citekey = \"%s\"; " selected-citekey)))))
    (progn (refman-update-last-accessed-db selected-citekey ck-database)
		       (sqlite-close ck-database)
					 (insert (nth 0 bibtex-citation)) )))


(defun refman-command (refman)
  "Send a command to refman" 
  (interactive "sRefMan: ")
	(shell-command-to-string (format "refman %s" refman)))
