+++
title = "Easier “Sub-Account” for GMail"
date = 2008-01-12T19:40:23Z
aliases = ["/2008/01/easier-sub-account/"]

[taxonomies]
tags = ["mac", "projects"]

[extra]
archived_from = "frankschmitt.org, 2008"
+++

In anticipation of getting an iPhone for Christmas, I moved my personal email account from my hosting company to [GMail](http://gmail.com/), using [Google Apps for my domain](https://www.google.com/a/). GMail gives me [IMAP](http://5thirtyone.com/archives/862), first-rate spam filtering, and more storage than I can shake a stick at. I couldn’t be happier with my arrangement, in particular how well it works with my iPhone.

However, there is a [project](http://t3ev.blogspot.com/) I’m involved with that would benefit from subscribing to a couple of high-traffic [mailing](http://www.evdl.org/help/index.html) [lists](http://vwtype3.org/list/). While I’d like to be able to peruse and participate in these lists, I don’t want them clogging up my iPhone’s inbox.

It turns out this is pretty easy to accomplish. First, sign into the web interface for your GMail and add a label (click “Edit Labels” in the left sidebar) for the mailing list. Since I followed the advice on the GMail link above and added the `[Gmail]` IMAP prefix to the account in Mail.app, I will also need to prefix the friendly name of my label with `[Gmail]/` (e.g. `[Gmail]/List`). On my Mac this will show up as an additional IMAP folder at the bottom of the sidebar.

Now you just have to create a filter (click the “Filters” tab under your GMail settings) that will automatically apply the label if the email in question is involved in the mailing list. Choose the appropriate criteria (the “Has the words” setting might be best, since often times “to” address isn’t what you’d expect). After clicking “Next Step” to continue, select the label, and — to keep it from showing up in your inbox — check the “Skip the Inbox” setting as well.

I can now receive email from the mailing list and it goes directly to my archive folder, receives the proper label, does not pass go, and does not collect $200.

One last thing: to get the label/folder to show up, I had to right-click the account in Mail.app and select Synchronize. YMMV.

These steps will let you follow one or more high-traffic mailing lists without them interrupting you every time a message is sent, but also without the latency of receiving digests instead of individual messages. It turns the mailing list “workflow”, if you will, into something closer to that of an RSS feed.
