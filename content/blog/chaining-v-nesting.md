+++
title = "Chaining vs. Nesting"
date = 2010-01-16T01:30:10Z
aliases = ["/2010/01/chaining-v-nesting/"]

[extra]
archived_from = "frankschmitt.org, 2010"
+++

Any UNIX sysadmin who’s been around the block a few times has probably written a line something like this:

`netstat -n | grep tcp | awk '{ print $5}' | sort | uniq -c | sort -n
`

Each command in this line produces output, and the end of the line, since it’s not shunted off to a file anywhere, prints to `stdout`. Every command (other than the first) accepts input on its `stdin` and has its output directed into the next command to the right.

If we were to write this in C-like pseudocode, it would look something like this:

`print(sort_n(uniq_c(sort(awk(grep(netstat_n(), "tcp"), 5)))));
`

Or we could use the Lisp convention of including the function name as the first element of an S-expression:

`(print (sort_n (uniq_c (sort (awk (grep (netstat_n) "tcp") 5)))))
`

This is essentially the same functionality as the command line, but this time each function passes its output to the enclosing function. Each function takes input from one of its arguments and optionally modifiers from the rest of its arguments. To the untrained eye it looks almost inside-out. You could reverse the order like so:

`(((((((netstat_n) grep "tcp") awk 5) sort) uniq_c) sort_n) print)
`

Which makes it read from left to right but doesn’t make it any more readable: the problem is that you’ve got the primary parameter, followed by the function name, followed by any secondary parameters. We can change it once more and loop very nearly back to the original command by translating it into a method-chaining style, as is common in Ruby or jQuery:

`puts netstat_n.grep("tcp").awk(5).sort.uniq_c.sort_n
`

This is certainly shorter (although I’ve cheated by omitting optional parentheses as allowed in Ruby) and arguably more readable. There is some evidence that non-programmers basically don’t really grok hierarchies, and I, for one, *definitely* have an easier time thinking about sequences than about hierarchies.

But making this happen is a bit more subtle than it appears at first glance. `netstat_n` would produce an array object, which would have a `grep` method that takes one argument (the expression to search for), and would output an array of the objects that match. `awk` would be another method on an array that would take an array of strings and return an array of substrings. `sort`, `uniq_c`, and `sort_n` would similarly be methods of the array object.

So at the very least you’re muddying up your array class with a bunch of things that are only peripherally related to arrays. Ruby solves this by making your write the more application-specific functionality as a block that gets passed to, say, the `select` and `collect` methods on array. So things are kept *relatively* in order.

Another to keep in mind is that the Lisp syntax may be easier for a program to manipulate: because the whole program consists of a giant nested list, any program with a nested-list-processing facility is able to manipulate the program with ease (it is likely, however, that one could define a relatively straightforward transformation from one form to the other).

Method chaining’s sweet spot seems to be in areas where functions have one dominant input (plus zero or more modifiers) and an equally obvious single output. Where the method chaining approach breaks down is in areas where two inputs have roughly the same importance. For instance, a conditional:

`(if (> price 50) "expensive" "cheap")
`

You almost have to introduce some kind of special syntax, e.g.:

`(price > 50) ? "expensive" : "cheap"
`

But this is the sort of muddling of statements and expressions that makes the Baby McCarthy cry. You could introduce a new syntax, for instance using a comma to separate two inputs that should be directed to a single consumer:

`"expensive","cheap".if(price > 50)
`

But I’m not sure if that’s unfamiliar or just plain ugly. The way this would work is that `if` would be a method of a two-element tuple object that would return the first value if its parameter were true or the second if it were false.

It would make more sense to have `if` be a method on a boolean expression, but I can’t think of a clean way to encode that without having a clean way to feed a function multiple inputs.

So it’s certainly doable, but that last code snippet is a good deal less readable (for both man and machine) than the Lisp version. A language based almost completely on method chaining might make for an interesting academic exercise, but it looks like it won’t buy too much in practice.
