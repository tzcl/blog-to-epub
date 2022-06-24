# How to Pick a Language


Say you're about to build a new project. You're an expert in a few languages,
and you have a sense of the ecosystem in general. How do you choose the
language you build with? I wanted to share my decision framework with you.

## Start with Constraints

Some requirements can eliminate entire categories of choices. Let’s use that
to our advantage: start by narrowing down your choices. For example:

 **Do you need extreme efficiency?** This would mean your code may need to be
compiled and that you can’t have run-time garbage collection. Well, that
narrows down your choices quite a bit.

**Do you need math-level proofs that your code works as expected?** This would
mean you need an _extremely_ strong type system. Bam, narrows choices down
quite a bit

**Do you need concurrency?** There are only a few VMs and a few languages that
are known to be _excellent_ for concurrency. Depending on what you need, this
will narrow your choices down to a few families.

 **Do you work in a larger environment?** If you are building something, and
your entire company is on one stack, there’s so much power to the existing
ecosystem that this effectively narrows down your choice to the language of
your environment.[1]

 **Is your problem in a domain where the ecosystem in one language is
strongest?** If you’re in machine learning, the ecosystem in python is so
powerful that it almost guarantees to narrow down your choice to that
language.

 **Is your problem a small script that needs to run everywhere?** This narrows
your choices down to the languages that are available by default on Linux

Now, there’s a leverage point here: constraints narrow down your choices in a
significant way. If you add a constraint you didn’t need, you risk sacrificing
a large set of options. For example, many think their system needs to scale
from the get-go. This is rarely the case and kills some of the choices that
contributed to the success of the biggest companies today [2]

So pick your constraints carefully. Once you do though, you’ll be pleasantly
surprised with how much clarity they give you: your choices will have gone
through a significant filter.

## Optimize for Effectiveness

The next filter is effectiveness. Choose the language that maximizes your
output on a time scale you care about.

At this stage, there is often a tradeoff between what you’re comfortable with
and what you need to discover. Say you’re comfortable in assembly, but don’t
know any other languages. What should you do?

Well, for some very small problems, it _does_ make sense to just write them in
assembly. If they’re urgent, you have no other choice. But for any significant
work, you’ll outstrip the productivity of assembly within a few days of ramp-
up.

The same kind of spectrum exists in higher-level languages, but the
differences take longer to show up. If you’re comfortable with Java, for
example, you can get a lot done pretty quickly. But within _some_ period, the
productivity benefits pale in comparison to more powerful languages.

Making this choice is a bit of an art, but it works like this. You want to
think about a time-frame that you’d like to optimize and pick the language
that optimizes for effectiveness within that timeframe.

If you’re in a hurry, you have no choice but to use what you’re comfortable
with, no matter how limiting. There are two ways to avoid the dilemma. You can
either play with different languages before you start your project, so you
have a wider array of comfortable choices to pick from, or give yourself a few
months to ramp up and select the language that’s most effective for your
problem.

With that, the question comes, _what time frame_ should you optimize for? This
is in itself an art. For startups, I would say about 8-12 months. Planning
further than that is over-optimization. For larger companies, I’d think 2-5
years.

## Break Ties with Fun

Now you’ve gone through two filters. Say you narrowed down to just a few
choices, but you aren’t sure which one to take. How should you break the tie?

I’d say fun. There are so many schleps in a startup that programming should be
as fun as possible. Once. I narrowed down. I’d choose the language I’m most
excited about.

* * *

 _Thanks to Sean Grove, Daniel Woelfel, Joe Averbukh, Alex Reichert for
reviewing drafts of this essay_

