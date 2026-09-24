+++
title = "text-rendering:optimizeLegibility;"
date = 2010-06-25T15:28:56Z
aliases = ["/2010/06/text-renderingoptimizelegibility/"]

[extra]
archived_from = "frankschmitt.org, 2010"
+++

Safari has historically had [lousy kerning](http://www.textism.com/2008/04/07/renderance) on its text rendering. This was particularly notable for [headlines](http://textism.com/).

A while back, [a fix was implemented](https://bugs.webkit.org/show_bug.cgi?id=6136). It wasn’t turned on browser-wide because of the performance implications, but it can be turned on by a web developer by setting the appropriate style.

The attribute to set is `text-rendering` and the value to set it to to enhance kerning and enable ligatures is `optimizeLegibility`.

The examples below show two pairs of headlines. The first in each pair has this style attribute set, and the second does not (technically, the second is set to `optimizeSpeed`). If you have Heveltica and Zapfino installed on an OS X device, you should see nicely rendered text below:

Text

Text

baffle

baffle

Find more about [**thc/marijuana detox**](http://www.atotaldetox.com/thc-marijuana-detox-kits/).
