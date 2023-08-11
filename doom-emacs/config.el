;; Some functionality uses this to identify you, e.g. GPG configuration, email
;; clients, file templates and snippets.
(setq user-full-name "FeistyKit"
      user-mail-address "eeveebeevee33@gmail.com")

(defun read-lines (filePath)
  "Return a list of lines of a file at filePath."
  (with-temp-buffer
    (insert-file-contents filePath)
    (split-string (buffer-string) "\n" t)))
  ;; http://ergoemacs.org/emacs/elisp_read_file_content.html

(defun trim-string (string)
        "Remove white spaces in beginning and ending of STRING.
        White space here is any of: space, tab, emacs newline (line feed, ASCII 10)."
        (replace-regexp-in-string "\\`[ \t\n]*" "" (replace-regexp-in-string "[ \t\n]*\\'" "" string)))
        
  ;; http://ergoemacs.org/emacs/modernization_elisp_lib_problem.html
  ;;
(remove-hook! rust-mode-hook #'racer-mode #'eldoc-mode)
(remove-hook! rustic-mode-hook #'racer-mode #'eldoc-mode)
(remove-hook! rustic-mode-local-vars-hook #'racer-mode)
(remove-hook! hack-local-variables-hook #'racer-mode)

(setq doom-theme 'zenburn)
(setq custom-font-size (cond ((file-exists-p "~/.config/doom/local-config") (string-to-number (trim-string ( nth 0 (read-lines "~/.config/doom/local-config"))))) (t 20)))
  ;; reading the size from a file so I can have different local configs for different computers

(setq doom-font (font-spec :family "Iosevka Nerd Font" :size custom-font-size :weight 'bold))

(setq racer-rust-src-path
      (concat (string-trim
               (shell-command-to-string "rustc --print sysroot"))
              "/lib/rustlib/src/rust/library"))

(setq lsp-rust-analyzer-cargo-watch-command "clippy")
(setq lsp-rust-analyzer-diagnostics-disabled (vector "inactive-code"))

(setq inferior-lisp-program "sbcl")

(require 'elfeed-goodies)
(elfeed-goodies/setup)
(when
    (and
     (boundp 'elfeed-show-mode-map)
     (boundp 'elfeed-search-mode-map)
     (boundp 'normal))
;; Taken from https://odysee.com/@DistroTube:2/is-the-best-rss-reader-an-emacs-package:6
    (cl-do (evil-define-key 'normal elfeed-show-mode-map
            (kbd "J") 'elfeed-goodies/split-show-next
            (kbd "K") 'elfeed-goodies/split-show-prev)
     (evil-define-key 'normal elfeed-search-mode-map
       (kbd "J") 'elfeed-goodies/split-show-next
       (kbd "K") 'elfeed-goodies/split-show-prev)))


(setq elfeed-goodies/entry-pane-size 0.5)
(setq elfeed-feeds (quote
                    (("https://www.reddit.com/r/rust.rss" reddit rust)
                     ("https://www.reddit.com/r/go.rss" reddit go)
                     ("https://www.reddit.com/r/linux.rss" reddit linux)
                     ("https://fasterthanli.me/index.xml" rust blog)
                     ("https://blog.joren.ga/feed.xml" c blog)
                     ("https://feeds.feedburner.com/geeklandlinux" blog))))



(set-lookup-handlers! 'lsp-mode :documentation nil)
(set-lookup-handlers! 'lsp-mode :documentation 'lsp-ui-doc-show)

(elcord-mode)

;; (require 'lsp-pyright)

;; (require 'lsp-ido)
(ido-mode 1)
(ido-everywhere 1)
(ido-ubiquitous-mode 1)

(setq rustic-lsp-server 'rust-analyzer)

;; If you use `org' and don't want your org files in the default location below,
;; change `org-directory'. It must be set before org loads!
(setq org-directory "~/org/")

;; This determines the style of line numbers in effect. If set to `nil', line
;; numbers are disabled. For relative line numbers, set this to `relative'.
(setq display-line-numbers-type 'relative)

(use-package! tree-sitter
  :config
  (require 'tree-sitter-langs)
  (global-tree-sitter-mode)
  (add-hook 'tree-sitter-after-on-hook #'tree-sitter-hl-mode))

(setenv "SHELL" "/usr/bin/zsh")

;; Set transparency: taken from https://askubuntu.com/questions/1007434/how-to-make-emacs-transparent-with-i3-wm
;; (set-frame-parameter (selected-frame) 'alpha '(90 . 90))
;; (add-to-list 'default-frame-alist '(alpha . (90 . 90)))

;; add indent-region functionality
(map! :leader
      :desc "Fix indentation of region" "c I" #'indent-region)

;; add indent-region functionality
(map! :leader
       :desc "Align by regex" "c b" #'align-regexp)

(setq hl-line-sticky-flag nil)
;; This configuration code is partially from https://gitlab.com/dwt1/dotfiles/-/blob/master/.config/doom/config.org#erc
;; I have edited it myself, too
(map! :leader
      (:prefix ("e". "ERC")
       :desc "Launch ERC with TLS connection" "e" #'erc-tls))

(setq erc-prompt (lambda () (concat "[" (buffer-name) "]"))
      erc-nick "daisyflare"
      erc-user-full-name "Daisy Flare"
      erc-track-shorten-start 24
      erc-kill-buffer-on-part t
      erc-fill-column 100
      erc-fill-function 'erc-fill-static
      erc-fill-static-center 20)
      ;; erc-auto-query 'bury
;; End taken code
