# Going multi-region


I recently shared a high level idea, on the infrastructure needed to evolve a
single-region system into a multi-region system. This is a bit abstract, but I
wanted to share this with you, to illustrate one of the most important system
design principles I employ: pushing complexity down the stack.

So, say you want to move your system to a multi-region system. What would you
need to do to evolve that system?

### 1\. You need a multi-region deploy train

In a service’s configuration, the service owner should be able to write
regions they can deploy to

[code]

        {US-East, US-West, China, Sweden}
[/code]

Then, the deploy train should be able to deploy to all regions

To do this, you need deployment infrastructure which takes this configuration
and can reserve and update machines in all regions.

### 2\. You need a multi-region DNS service

A service owner should be able to make a request out to another service, by
some url:

[code]

    curl service-b.internal-dns
[/code]

Once the request is made, the DNS service should find a machine that’s
geographically closest to the origin request. It needs to be able to handle
failures, and find different machines if that is the case

To do this, you need infrastructure for service routing. This should be a tool
that lets a service owner associate specific machines to a route, and allows
them to set specific rules: things like default timeouts and failover
behaviors.

This infrastructure should come with a library available on all system
languages, which lets them send requests.

### 3\. You need a distributed database

A service owner should be able to create tables and specify: where the source
of truth should live, privacy rules, and compliance rules. The database should
expose a friendly API that abstracts away how it fetches the data, as well as
how it determines privacy and compliance rules.

To do this, you first need to introduce a database like cassandra or spanner.
After that you likely also need to add an extra layer of infrastructure on
top, to abstract away privacy and compliance rules.

* * *

If you have these three pieces of infrastructure, you can begin to migrate
leaf services with significant velocity. **A key thing to notice: much of the
leg work is done by infrastructure**.

Pushing complexity down the stack is what will allow you to scale your
organization. It can be easy to leave much of this complexity in the product
domain. If you do this, you will slow down every product engineer, and force
them to have enough context to make significant system decisions for most
changes. It will also leave your infrastructure engineers scrambling to manage
and maintain numerous esoteric solutions, which were brought up in product
land and now need to be maintained. By managing most of the complexity with
your infrastructure, your product engineers can focus and maximize their
impact with product, and your infra engineers can maximize theirs by
empowering the whole company.

 _Thanks to Daniel Woelfel for reviewing drafts of this essay_

