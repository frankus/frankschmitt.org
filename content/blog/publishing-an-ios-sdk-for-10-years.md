+++
title = "What I Learned Publishing an iOS SDK for 10 Years"
date = 2026-09-30
description = "Ten commandments from a decade of maintaining an SDK that shipped in a thousand apps and ran on hundreds of millions of devices."

[taxonomies]
tags = ["ios", "sdk"]
+++

Until a couple of weeks ago, I was responsible for building, maintaining, and releasing updates to an SDK for iOS apps called ApptentiveKit. It’s a customer-feedback SaaS product primarily aimed at consumer-focused apps. There’s also an Android version, as well as wrapper SDKs for Flutter, React Native, Cordova and .NET MAUI (as well as one that I recently completed but that hasn’t released yet). 

That SDK’s job is to connect your app to the backend API, while also presenting some user-facing UI where needed. 

The feature that would get customers in the door (and did legitimately make number go up) was improving app ratings by way of trying to prod normies into reviewing the app in the App Store, an activity which will otherwise be dominated by a smattering of superfans and a horde of detractors. 

A secondary aim was to redirect complaints and confusion from a bad App Store review (which at the time it launched couldn’t be replied to) to an actual two-way feedback mechanism. Basically the old “If you love our service, tell your friends, and if you don’t, tell us” sign in code form. 

The SDK has made it into roughly a thousand apps, and has run on hundreds of millions of devices. If an app on your iPhone ever asked you “Do you love $AppName”, that was probably my code. I’m sorry. 

> A quick note on terminology: I’m going to use our internal guideline and refer to the company paying for our SaaS as the *customer*, and the people actually using the app (and the handful of pieces of user-facing UI in the SDK) as the *consumer*. 

I joined Apptentive in April of 2015 along with five other new hires, becoming part of a company that had a couple dozen employees. The SDK I inherited was a four-year-old Objective-C codebase (with manual reference counting) that had grown out of a hackathon project. 

It did the job, but there were some issues below the surface: it used `NSUserDefaults` for nearly all persistence (with a smattering of Core Data), almost every internal call was routed back through the `[ApptentiveConnection sharedConnection]` singleton, and most everything was happening on the main thread. 

Over the years—largely on my own but with occasional help—I was able to shore up the reliability of that SDK: a more testable persistence system using `NSCoding`, a more observable logic engine (compared with the `NSPredicate`-based one it replaced), and most processing taking place off the main thread. 

Then around 2020 I was given the opportunity to start fresh with a rewrite of the SDK in Swift. While this was costly, and required maintaining two completely separate codebases, in the intervening years it paid off handsomely in terms of reliability and ease of adding features. 

Over that time I’ve collected a number of observations and lessons, which I present to you here in the form of Ten Commandments of SDK publishing:

<ol type="I">
  <li>Don’t crash the customer’s app</li>
  <li>Don’t break the customer’s build</li>
  <li>The SDK should do as little as possible</li>
  <li>Avoid development dependencies</li>
  <li>The app-facing API should be idiomatic to the platform</li>
  <li>Avoid third-party dependencies</li>
  <li>Add a kill switch</li>
  <li>Add monitoring</li>
  <li>UI should match the platform</li>
  <li>Customers won’t use that</li>
</ol>

## I: Don’t Crash the Customer’s App

The likelihood that your SDK is the thing standing between your customer and untold riches is slim. The likelihood that your SDK is the reason a *consumer* installed the app on their phone is basically zilch. 

This means that the SDK going into a failsafe do-nothing mode is *vastly* preferable to something in the SDK crashing the whole app. 

There are of course easy-to-avoid sources of potential crashes, like force unwrapping an optional, and slightly more subtle ones like array out-of-bounds and—now largely a thing of the past—`UITableView` internal inconsistency exceptions. But there’s also that innocent-looking view-sizing code with a divide-by-zero condition that’s only triggered when an image fails to load. 

## II: Don’t Break the Customer’s Build

Again, aside from conscientiousness, this only requires a bit of self-awareness on the part of the SDK developer to realize that their SDK is at best an ancillary feature of the customer’s app. 

We strove to make our SDK respect the conventions of semantic versioning, but there were a few times when we fell short: a new API added during a patch release, or that one time the new guy corrected the spelling of a property without preserving a deprecated copy with the incorrect spelling (and I didn’t catch it in my code review). 

Customers’ developers want to think about your SDK as little as possible, and the best way to avoid their ire is for a minor or patch version upgrade to Just Work. 

## III: The SDK Should Do as Little as Possible

Some parts of an SDK need to run on the device. Things like consumer-facing UI, offline capability, persistence, and the client-side code involved in communicating with an API. 

At the same time some parts of the overall system only really make sense to run on a server, quite possibly one that you control. 

There’s a third category of code that could theoretically run on either the device or the server (for example, assembling the instructions for how to answer a survey question), and the rule for this is almost always that it should run on the server. 

The reason for this is twofold: First, SDK Code is Forever. 

If you publish an app with any appreciable reach, chances are excellent that there will be a version installed somewhere that will literally never be updated. If your product is an SDK, the situation is several times worse: you have to publish a release of your SDK with the updated code, your customer has to migrate their app to your new SDK version, and then release an updated version of their app, and finally the consumer has to be convinced to install the updated app. Any one of these steps could simply never happen, and all but the first are out of your control. This sucks if there’s a minor UI glitch. This *really* sucks if there’s a runaway condition that hammering your server or requires an ugly workaround. 

Secondly, few SDKs are published for a single platform. Chances are your iOS SDK will have an Android counterpart, and quite possibly even a web version. If you want to avoid development dependencies (see below) this means you’ll be writing the same code at least twice (and possibly several times) in different languages and with standard libraries that have significantly different capabilities. 

Both the lack of updatability and the likely requirement to reimplement features in several languages point to erring on the side of server-side code whenever it’s in question.[^1]

## IV: Avoid Development Dependencies

There exist a few tools that promise the ability to ship the same code on multiple platforms: from cross-platform app development tools like Flutter and React Native, to compilation tools like Kotlin Multiplatform and Swift Android. 

If you publish an app, it’s worth considering whether these sorts of tools make sense (although again, it’s preferable to just run on your server wherever that’s practical). 

If you publish an SDK, one of the hardest problems is getting customers to actually integrate with your SDK (we had customers with a signed contract and monthly/annual payments flowing who might wait *months* to actually get around to integrating).

Even customers with a sophisticated web presence might lack the in-house expertise to publish or update a mobile app, so often their mobile development work is outsourced. In that case any friction in integrating your SDK may well show up as actual billable hours in your customer’s outsourcing contract, and that’s likely to color their opinion of your product at renewal time. 

One way to greatly complicate the integration process is, for example, to require an iOS developer to install a Kotlin toolchain simply to continue to build their app after your SDK is integrated.[^2] But even something as commonplace as Fastlane or CocoaPods can be a stumbling block if your customer doesn’t have a working Ruby environment. 

You should strive to have your SDK integrate cleanly on a development machine with nothing installed other than the typical toolchain used by a developer of the platform in question. 

## V: Your API Should be Idiomatic to the Platform

As a corollary to the previous, the folks integrating your SDK likely live and breathe the platform they’re developing for, and can sniff out an awkward or non-idiomatic API from a mile away. They’ll expect your API to be similar to first-party APIs on their favored platform, and appreciate using platform-specific language features (like Swift’s subscripting). 

This sometimes means compromising on cross-platform consistency. For example our SDK’s methods were almost all static methods on a class for Android, and instance methods on a singleton on iOS.[^3] 

## VI: Avoid Third-Party Dependencies

Another excellent way to frustrate a developer trying to integrate your SDK is to introduce some flavor of “dependency hell” alongside your SDK. 

This isn’t a hard-and-fast rule, but if there’s a straightforward way to just reimplement something simple that you might (in the context of an app) just use a library for, it’s probably worth just reimplementing it (and hopefully leaving out any expensive bits of generality). Particularly with agentic coding, it’s often easier to generate a small piece of what might otherwise be library code than to introduce a dependency that your customers will have to manage. 

## VII: Add a Kill Switch

This is one that we learned (and acted on) relatively late. The best time to add a kill switch to your SDK is before you publish the first version. The second best time is now. 

There will likely come a day when a customer does something unexpected, or simply reaches a scale that your infrastructure will struggle under, where you’ll be well-served by an ability to throttle or even disable your SDK’s functionality remotely. 

This is doubly true if the customer has churned and—often only through the fault of consumers who don’t update their app—is still sending traffic.  

## VIII: Add Monitoring

By successfully obeying the first commandment (don’t crash), you do sacrifice one channel for conveying the fact that something went wrong in your code, namely crash reports. 

In place of crashing, the SDK will likely simply log the failure and continue on its way. 

This has two downsides: first, customers or consumers could be experiencing frustrating failures—with no indication as to the cause—and you might very well be completely unaware of it happening. 

The second is that a change to your server could abruptly break a large fraction of your SDK’s installed base (possibly even causing crashes), and you’ll only learn about this after your customers start complaining. Having an early warning that something went wrong is extremely valuable. 

## IX: UI should match the platform

There’s a widespread tendency among product and design folks to attempt to make user-facing interface elements be as identical as possible across platforms. I suspect this is because this is pretty explicitly the goal when developing for web: customers might very well access your website from different browsers, and will be confused if things look or work differently. 

But users switching platforms (either hour-to-hour or, really, ever) is pretty rare compared with users who expect the UI to work like every other app on their phone. 

A desire for brand consistency across platforms is perfectly natural, but consumers are much more likely to have used other apps on their platform than your app on another platform. 

## X: Customers won’t use that

This last one is a bit of a downer, but one of the hard lessons that I learned over the last decade is that a cool new capability I added to the SDK is most often met by customers’ developers staying away in droves. 

When I did the Big Swift Rewrite one of the shortcomings of the Objective-C SDK that we wanted to address was the difficulty of customizing the consumer-facing interface elements beyond the basics of fonts and colors. 

So we designed the UI around an MVVM design pattern, with the goal that customer with heavy customization needs could reimplement (or subclass) our view controllers and use our view models to drive them. This would allow extreme freedom in customization without requiring the customer to fork our SDK. 

While this enforced some useful discipline in architecting our user interface code, in the end not a single customer even expressed the desire to use the capability. 

This is just one example but the pattern repeated itself often. As an SDK author you’re often reminded that what you live and breathe all day every day is just a small part of the code your customers write for a living, and it pays to have some self-awareness about that. 

## Takeaways

The common thread here is that your SDK is a guest in someone else’s app, and should aim to be as unobtrusive as possible: minimal integration steps, keeps working silently in the background, and requires zero attention until a new feature makes the upgrade worthwhile. 

The best compliment an SDK author can get is silence—no crash reports, no integration questions, no GitHub issues, and nothing overloading our server.

[^1]: There is a potential way to sidestep both of these—but until recently it required violating the commandment against third-party dependencies. That is to ship your business logic as JavaScript code. JavaScript runs natively on the web, and via a built-in framework (`JavaScriptCore`) on iOS, and Android recently added decent first-party support for doing this. This avoids the “SDK code is forever” because the code can be updated in flight, and avoids the need to “write everything twice” by being able to run on almost every platform of interest.

[^2]: Of course if your SDK—or at least parts of it—ship as a binary, you may be able to use cross-platform tools without inflicting them on your customers’ developers.

[^3]: When I rewrote the original Objective-C SDK in Swift, I made sure that it was an “incidental singleton”—with no internal references to the shared instance—which did wonders for making things easier to test.
