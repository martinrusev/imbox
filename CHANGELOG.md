## 0.9.5 (5 December 2017)

IMPROVEMENTS:

 * `date__on` support: ([#109](https://github.com/martinrusev/imbox/pull/109))
 * Starttls support: ([#108](https://github.com/martinrusev/imbox/pull/108))
 * Mark emails as flagged/starred: ([#107](https://github.com/martinrusev/imbox/pull/107))
 * Messages filter can use date objects instead of stringified dates: ([#104](https://github.com/martinrusev/imbox/pull/104))
 * Fix attachment parsing when a semicolon character ends the Content-Disposition line: ([#100](https://github.com/martinrusev/imbox/pull/100))
 * Parsing - UnicecodeDecodeError() fixes: ([#96](https://github.com/martinrusev/imbox/pull/96))
 * Imbox() `with` support: ([#92](https://github.com/martinrusev/imbox/pull/92))


## 0.9 (18 September 2017)

IMPROVEMENTS:

 * Permissively Decode Emails: ([#78](https://github.com/martinrusev/imbox/pull/78))
 * "With" statement for automatic cleanup/logout ([#92](https://github.com/martinrusev/imbox/pull/92))
 


## 0.8.6 (6 December 2016)

IMPROVEMENTS:

 * Add support for Python 3.3+  Parsing policies: ([#75](https://github.com/martinrusev/imbox/pull/75))
 
BACKWARDS INCOMPATIBILITIES / NOTES:

  * Remove support for Python 2.7

## 0.8.5 (9 June 2016)


IMPROVEMENTS:

 * ssl_context: Check SSLContext for IMAP4_SSL connections  ([#69](https://github.com/martinrusev/imbox/pull/69))
