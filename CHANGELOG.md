## 0.9.8 (02 June 2020)

IMPROVEMENTS:

* Fix imbox.delete regression ([#138](https://github.com/martinrusev/imbox/issues/138))
* Fixed handling for attachments with filenames longer than 76 characters ([#186](https://github.com/martinrusev/imbox/pull/186)) -  Contributed by @nirdrabkin
* Improved character encoding detection ([#184](https://github.com/martinrusev/imbox/pull/184)) -  Contributed by @py-radicz

## 0.9.7 (03 May 2020)

IMPROVEMENTS:

* Gmail: IMAP extension searches label and raw are not supported.
* Searches in mail bodies and UID ranges are now supported.
* Attachments have a Content-ID now (#174)

## 0.9.6 (14 August 2018)

IMPROVEMENTS:

 * Vendors package, adding provider specific functionality ([#139](https://github.com/martinrusev/imbox/pull/139)) -  Contributed by @zevaverbach
 * Type hints for every method and function ([#136](https://github.com/martinrusev/imbox/pull/136)) -  Contributed by @zevaverbach
 * Move all code out of __init__.py and into a separate module ([#130](https://github.com/martinrusev/imbox/pull/130)) - Contributed by @zevaverbach
 * Enhance `messages' generator: ([#129](https://github.com/martinrusev/imbox/pull/129)) - Contributed by @zevaverbach


## 0.9.5 (5 December 2017)

IMPROVEMENTS:

 * `date__on` support: ([#109](https://github.com/martinrusev/imbox/pull/109)) - Contributed by @balsagoth
 * Starttls support: ([#108](https://github.com/martinrusev/imbox/pull/108)) - Contributed by @balsagoth
 * Mark emails as flagged/starred: ([#107](https://github.com/martinrusev/imbox/pull/107)) - Contributed by @memanikantan
 * Messages filter can use date objects instead of stringified dates: ([#104](https://github.com/martinrusev/imbox/pull/104)) - Contributed by @sblondon
 * Fix attachment parsing when a semicolon character ends the Content-Disposition line: ([#100](https://github.com/martinrusev/imbox/pull/100)) - Contributed by @sblondon
 * Parsing - UnicecodeDecodeError() fixes: ([#96](https://github.com/martinrusev/imbox/pull/96)) - Contributed by @am0z
 * Imbox() `with` support: ([#92](https://github.com/martinrusev/imbox/pull/92)) - Contributed by @sblondon


## 0.9 (18 September 2017)

IMPROVEMENTS:

 * Permissively Decode Emails: ([#78](https://github.com/martinrusev/imbox/pull/78)) - Contributed by @AdamNiederer
 * "With" statement for automatic cleanup/logout ([#92](https://github.com/martinrusev/imbox/pull/92)) - Contributed by @sblondon
 


## 0.8.6 (6 December 2016)

IMPROVEMENTS:

 * Add support for Python 3.3+  Parsing policies: ([#75](https://github.com/martinrusev/imbox/pull/75)) - Contributed by @bhtucker
 
BACKWARDS INCOMPATIBILITIES / NOTES:

  * Remove support for Python 2.7

## 0.8.5 (9 June 2016)


IMPROVEMENTS:

 * ssl_context: Check SSLContext for IMAP4_SSL connections  ([#69](https://github.com/martinrusev/imbox/pull/69)) - Contributed by @dmth
