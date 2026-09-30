+++
title = "Flush your Leopard’s DNS Cache"
date = 2007-11-20T11:27:50Z
aliases = ["/2007/11/flush-your-leopards-dns-cache/"]

[taxonomies]
tags = ["mac"]

[extra]
archived_from = "frankschmitt.org, 2007"
+++

For those of you used to running `lookupd -flushcache` to clear out stale entries from your DNS cache in Mac OS X, the new version (10.5) has [replaced the old NetInfo](http://www.macworld.com/news/2007/11/16/netinfo/index.php?pf=1) suite with a bunch of new, more compatible utilities. The new way to do this is `dscacheutil -flushcache`.
