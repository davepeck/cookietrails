# cookietrails

Cookie inventory management tools for large Girl Scout troops.

## What is this?

Generally speaking, all Girl Scout troops nationwide use two pieces of software:

- `Digital Cookie`, an online storefront for customers to place cookie orders, and for families to manage their individual sales
- _Either_ `eBudde` _or_ `Smart Cookies`, back-office web apps for troop leaders to manage cookie inventory and orders

My council purchases cookies from Little Brownie Bakers, who use the `eBudde` app. Alas: `eBudde` (and the cookie selling best practices it attempts to enforce) is designed for small troops of fewer than 10 girls. My troop has 50.

The question becomes: which "rules" &mdash; both in software and in council policy &mdash; are designed for small troops, and which are essential for all troops?

In `eBudde`, when cookies are assigned to a family, it means two very different things at the same time:

1. The family is financially responsible for those cookies.
2. The family physically possesses those cookies.

There's one special "family" in the system: the troop itself. Cookies assigned to the troop are financially the troop's responsibility and the _expectation_ is that the troop physically possesses those cookies in a single known location, like a troop cookie cupboard or someone's garage.

This works fine for small troops, but for large troops it creates problems. A troop with 50 girls cannot realistically store all its shared cookies in a single location. At our peak sales week, my troop needs 5,000+ boxes of shared cookies on hand, which requires considerable space. Also, because families need to pick up (and return) cookies to the troop inventory with some regularity, and it's impossible to coordinate a single time to do so with 50 families, the foot traffic pressure on a single location is high.

Cookie Trails allows us to break a single assumption in eBudde: that cookies assigned to the troop are physically in one place. With Cookie Trails, cookies assigned to the troop can be tracked as they are distributed to families, and then returned from families back to the troop inventory.

In order to manage this, Cookie Trails records just three types of events:

- **Distributions**: cookies moving from the troop inventory to a family
- **Returns**: cookies moving from a family back to the troop inventory
- **Counts**: physical counts of how many boxes of each cookie variety are currently held by the troop or a family

Distributions and returns are entered into the system as they occur, by the troop cookie managers. Counts are performed periodically by every family.

Combined, these three event types allow Cookie Trails to track troop inventory accurately without requiring all troop-assigned cookies to be in a single location. Specifically, when a family reports a count N of a cookie variety, Cookie Trails can see that the family is _personally_ repsonsible for M boxes of that variety. If N > M, then the family has extra boxes that must have come from the troop inventory.

## What is this, technically?

Cookie Trails is a simple Django 6.x web app, written in Python 3.14. It presents a very basic interface to families for cookie counts, and a more advanced interface to troop cookie managers for distributions, returns, and reporting.

## Running your own instance

I currently run this using [Dokku](https://dokku.com/) on a home server, with CloudFlare wrapped around it. But you could run this on Heroku's ultra-cheap tier, or any other platform that supports 12-factor web apps and offers a Postgres database. (This being Django, you can also use SQLite or MySQL if you prefer; I have not tested those configurations myself.)
