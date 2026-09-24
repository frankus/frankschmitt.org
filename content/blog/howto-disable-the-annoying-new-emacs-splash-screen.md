+++
title = "HOWTO Disable that annoying Emacs Splashscreen"
date = 2007-12-05T18:55:21Z
aliases = ["/2007/12/howto-disable-the-annoying-new-emacs-splash-screen/"]

[extra]
archived_from = "frankschmitt.org, 2007"
+++

The new `emacs` included with OpenSuSE 10.3 includes a “feature” that displays this irritating little splash screen when you’re trying to edit a file. It’s almost irritating enough to switch to `vi`.Fortunately, there’s an easy way to disable it. Create or edit the file called `.emacs` in your home directory:$ vi ~/.emacsand add the following line:(setq inhibit-splash-screen t)and voila, it’s gone for good.
