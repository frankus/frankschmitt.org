+++
title = "Creating a “Sub Account” with GMail and Mail.app"
date = 2008-01-12T19:06:36Z
aliases = ["/2008/01/gmail-sub-account/"]

[taxonomies]
tags = ["mac", "projects"]

[extra]
archived_from = "frankschmitt.org, 2008"
+++

**Update:** [Here](/blog/easier-sub-account/)’s an easier way.

In anticipation of getting an iPhone for Christmas, I moved my personal email account from my hosting company to [GMail](http://gmail.com/), using [Google Apps for my domain](https://www.google.com/a/). GMail gives me [IMAP](http://5thirtyone.com/archives/862), first-rate spam filtering, and more storage than I can shake a stick at. I couldn’t be happier with my arrangement, in particular how well it works with my iPhone.

However, there is a [project](http://t3ev.blogspot.com/) I’m involved with that would benefit from subscribing to a couple of high-traffic [mailing](http://www.evdl.org/help/index.html) [lists](http://vwtype3.org/list/). While I’d like to be able to peruse and participate in these lists, I don’t want them clogging up my iPhone’s inbox.

By combining a few esoteric features of GMail and Mail.app, I have come up with an arrangement that works superbly.

The first trick is a little-known GMail feature, where appending a plus sign followed by a suffix to a GMail address will result in the email being delivered as though the suffix wasn’t there. So if I want to subscribe to the electric vehicle discussion list, I can subscribe as `frank+ev@example.com`, and assuming example.com’s mail is handled by GMail, it will be delivered to the `frank@example.com` account.

That’s great, but the email ends up in my inbox like any other, which gets to be annoying when a high-traffic list is used in conjunction with an iPhone. So the next step is to sign into the web interface for my GMail domain and add a label (click “Edit Labels” in the left sidebar) for the mailing list. Since I followed the advice on the GMail link above and added the `[Gmail]` IMAP prefix to the account in Mail.app, I will also need to prefix the friendly name of my label with `[Gmail]/` (e.g. `[Gmail]/EV`). On my Mac this will show up as an additional IMAP folder at the bottom of the sidebar.

Now I just have to create a filter (click the “Filters” tab under your GMail settings) that will automatically apply the label if the email in question is involved in the mailing list. I’m using the “Has the words” setting for this, as often times the “to” address isn’t what I would have expected for a mailing list. After clicking “Next Step” to continue, I need to select the label, and — to keep it from showing up in my inbox — check the “Skip the Inbox” setting as well.

I can now receive email at my `frank+ev@example.com` address, and it goes directly to my archive folder, receives the proper label, does not pass go, and does not collect $200.

But what if I want to send a message from this address? For instance, to subscribe to the mailing list? I’d like something easier than `telnet`ting to port 25 on the whatever the mx record for the listserv is.

Like the preceeding, the is a multi-step process. First, I need to add the aliased address to your GMail account. To do this, visit the settings page and click the “Accounts” tab. Then I need to click the “Add another email address” link and type in the alias (e.g. `frank+ev@frankschmitt.org`) as the additional address.

Finally, I need to open the Accounts tab under the preferences in Mail.app (once for every machine from which I want to send mail to the list) and take advantage of another little-known feature. I need to select the IMAP account that I’m using with GMail and and in the “Email Address” field, add a comma and the alias I’m using (it will look like `frank@example.com, frank+ev@example.com`). Tada! I now have the alias as an option for the “from” address when I create a new email.

One last thing: to get the label/folder to show up, I had to right-click the account in Mail.app and select Synchronize. YMMV.

These steps will let you follow one or more high-traffic mailing lists without them interrupting you every time a message is sent, but also without the latency of receiving digests instead of individual messages. It turns the mailing list “workflow”, if you will, into something closer to that of an RSS feed.
