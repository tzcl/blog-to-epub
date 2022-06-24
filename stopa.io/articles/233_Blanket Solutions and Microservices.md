# Blanket Solutions and Microservices


Much of my system design philosophy was forged during my time at Facebook. We
did a lot of things differently that I think was responsible for our technical
success. I want to share one of them with you. It’s the most common pitfall
I've see prevalent in our industry, and it relates how we solve problems at
the system level. I’ll illustrate it with a story:

### Beginning

You kick off your startup. One service, one repo, one database. Version zero
ships quickly. You iterate and iterate until you sense product market fit.

All of a sudden, you’ve got it and you’re on a rocket ship. You grow your
team, you’re onboarding customers, and you’ve got some great problems on your
hands.

### Emergency

One of those problems: your systems break.

Your build infrastructure slows down. Deployment becomes an all-day, panic-
ridden affair. Commits start to break unrelated components more and more
frequently. The development environment becomes slower and slower. You get
incidents left and right. Oncall becomes more demanding than a newborn at
night.

Slow down productivity and you’ll get grumpy engineers, but take away their
sleep and you’ll get rioting engineers. Now you have an emergency on your
hands.

### Light in the Darkness

You look around, and the technical debt is overwhelming. You think: it’s time
to grow up. You research and land on microservices as the answer. It seems to
solve all your biggest pain points:

 ** _Speed up deployments_**

Teams can manage their own deployments. Because deploying smaller systems is
easier and safer than larger ones, your teams can now deploy faster. Heck,
they could even roll back now.

 ** _Separate concerns_**

You’ll force stronger code boundaries. No more commits breaking unrelated
components

 ** _Empower teams_**

You’ll be able to use the right tools for the job. No more need to have the
same language or stack. Teams can use whatever will make the most productive
at solving their particular problem.

 ** _Ensure quality_**

You’ll be able to clarify ownership. No more spaghetti code because service
owners will ultimately be responsible

### Uh Oh

This is the dream. You kick off that initiative. But…you see some serious
costs:

 ** _Hardened boundaries are harder to change_**

Those strict code boundaries come with their own costs. If you split
incorrectly, you’re prone to dupe your data and your logic. But, even if you
split correctly, what happens when your business needs change? What if you get
new regulation that requires system-wide changes? All of a sudden, the way you
split those services won’t make sense anymore, and evolving those boundaries
become a magnitude more difficult.

 ** _Hardened boundaries make it more difficult to ship unanticipated
changesets_**

What if you need to make changes that your org and service structure didn’t
anticipate? These changes won’t cleanly fit into one service, or even groups
of services. All of a sudden a change that could have been done by one
engineer before requires teams to align to deliver.

**_Hardened boundaries reduce the potential impact of your engineers_**

What if one of your engineers comes up with a performance improvement, or a
new idea for the business? Their impact is now constrained by the services
they have control over. If the languages are different they won’t be able to
actualize that performance improvement for the whole company. Even if we force
all services to use the same language, delivering that to all services becomes
a difficult affair.

 ** _More Incidental complexity_**

Sharing code, managing deploys, logging infrastructure, service orchestration,
rpc are all made more difficult by a change to multiple services. None of the
added difficulty helps you move faster or ship with higher quality.

### Root Cause

Why so many unanticipated issues? Because microservices as a strategy is a
**blanket solution.**

Blanket solutions don’t _specifically_ address any one issue, but try to
address a multitude of issues. This is often done with philosophy (new
principles we will follow to build things) then with technology (how exactly
we will solve problems). Whenever a solution addresses a multitude of issues
with philosophy, it’s likely to come with a multitude of unanticipated
problems.

### An Alternative Path

The alternative path is evolution. As a rule of thumb, the changes you
introduce should concretely solve the problems you care about. This doesn’t
mean that all solutions need to be iterative, but it does mean that all
solutions need to be under strong selection pressure. Every solution should
have immediate wins in sight.

For example:

**_Deployment, CI, logging issues?_**

_What if you built a centralized team that owned that complexity, and built
infrastructure so product engineers didn’t have to worry about it? For
example, most product engineers did not have to worry about deploys,
observability, or logging at Facebook. Infra was already in place that they
could leverage, managed by an underlying team._

 ** _Code boundary issues?_**

_What if you evolved your system to use_ _immutable structures_ _and_ _smaller
interfaces between boundaries**? What if you pushed some of these problems
down the stack? For example, there may be a lot of complexity introduced with
privacy. You can centralize that concern, into building infrastructure with a
small interface, that product engineers can use. Facebook did this with viewer
context_

 ** _Scaling issues?_**

_This may be a true concern, but instead of applying a general philosophy,
could we focus on solving this problem directly? Do all systems need to scale
independently, or does it only matter that just a few things scale
independently? exactly are the problems? Could you address with_ _only
changing the hottest, most intensive paths?_

 ** _Complexity issues?_**

_Where is the complexity exactly? Could we evolve modules so you could
localize the reasoning behind them? Could we abstract the difficult portions?
Sophie Alpert gives a great example of this_
[_here_](https://sophiebits.com/2020/01/01/fast-maintainable-db-patterns.html)

This kind of thinking leads to a philosophy of system design based on
simplicity:

 _You address problems concretely with a view towards evolving your system._
At each step of the way, you constantly optimize for engineering velocity.
Engineering velocity is a great metric to use, because it implies correctness
and quality alongside with speed. It’s impossible to ship if you don’t have
confidence in your system. You push and centralize complexity down the stack.
You evolve your system so product engineers can think locally within the
module they’re working on. You make changes that empower any engineer to drive
impact throughout the stack.

Doing this won’t be a magic pill — it will look like your system is constantly
broken and in need of improvement — but that is its secret weapon. You’re
constantly evolving it.

_Thanks to Daniel Woelfel, Jacky Wang, Kam Leung, Joe Averbukh, Phil Nachum,
Alexandre Lebrun, for reviewing drafts of this essay_

