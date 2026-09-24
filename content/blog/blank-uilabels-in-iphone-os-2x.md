+++
title = "Blank UILabels in iPhone OS 2.x"
date = 2009-03-27T10:32:18Z
aliases = ["/2009/03/blank-uilabels-in-iphone-os-2x/"]

[taxonomies]
tags = ["cocoa", "mac", "projects"]

[extra]
archived_from = "frankschmitt.org, 2009"
+++

I spent about an hour yesterday carefully stepping through some code that was setting the text of a UILabel in an iPhone app I’m working on. It worked perfectly on my 3.0 development box and my 3.0 device, but for some inexpicable reason, the text wasn’t showing up on my client’s 2.0 machine or device.

I used the debugger to confirm that the UILabel’s text property was being set, and compared it to another screen in the same app that was using the same exact code to set a UILabel to the same text. We confirmed that the label hadn’t slipped behind some other interface elements (and that it wasn’t being hidden) by setting its background to red. We even set the label’s text manually in interface builder and commented out the code that set its value. Still no text appeared.

The client finally suggested removing and re-adding the label to the .xib. I humored him and tried it, and sure enough, the text showed up. So we adjusted the size of the label and set the font back to Courier New Bold and the text disappeared.

It turns out that Courier New Bold is *n**ew for iPhone OS 3.0*. Rather than falling back to the regular weight, iPhone OS 2.0 (both on the device and on the simulator) simply displays nothing.
