+++
title = "Things I Hate, Part II: Web Forms that Auto-Tab"
date = 2008-04-10T11:42:55Z
aliases = ["/2008/04/things-i-hate-part-ii-web-forms-that-auto-tab/"]

[taxonomies]
tags = ["things i hate"]

[extra]
archived_from = "frankschmitt.org, 2008"
+++

There seem to be quite a few web designers with too much time on their hands out there, with just enough knowledge of JavaScript to be dangerous.

What else can explain the fascination with taking what could be a simple text field (for entering a phone number, IP address, or SSN, for instance) and instead making it three or four separate text fields plus a half-baked script to “conveniently” yank the cursor into the next field when the current one is full? This violates at least three common-sense principles of user interface design.

The first violation is of the KISS principle. There is no reason why a phone number can’t be one field that accepts 5558675309, (555) 867-5309, or +1-555-867-5309 and figures out with a regular expression or two that the area code is 555, the prefix 867, and the number 5309.

Secondly, it violates the principle of least surprise. Other fields in web forms don’t do this: I don’t finish typing “Frank” in the First Name field only to have the cursor magically jump into the Last Name field. Because, of course, my name might be Franklin (it’s not — in Germany “Frank” is a *bona fide* first name and that’s what my birth certificate says) and if the web form knew my name it wouldn’t be asking for it. But while it’s possible to do this for certain classes of text fields it’s a Bad Idea, because it’s never the expected behavior.

Finally, it’s fundamentally broken. At least, every implementation of this “feature” that I’ve ever dealt with has been broken. When I screw up and type my area code as “666”, I want to be able to hit the delete key and correct it. Failing that, I at least want to be able to shift-tab back to the screwed-up field and correct it without having the cursor jump right back to the next field. I also want to be able to type 5 5 5 tab 8 6 7 without the “867” appearing in the number field, leaving the prefix blank.

It may in fact be impossible to implement this in JavaScript in a cross-platform way that doesn’t confuse grandmas and confound compulsive keyboard users like myself. Which doesn’t mean you should take a stab at it and make something that kinda works most of the time. It means you should back off, take a deep breath, and take a different approach.
