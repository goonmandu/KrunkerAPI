# KrunkerAPI Documentation
## Usage
To call the API:
```py
from krunker_api import krunker_api
data = krunker_api(username)  # returns JSON/dict
```
## Structure
- `name`: **string** *[name of account]*
- `general`: **json** *[contains general account info]*
  - **string**: **bool**, **float**, **int**, or **json** *[actual data]*
    - (in the case of `helpful_reports`) **string**: **int**
- `class_xp`: **json** *[contains xp level per class]*
  - **string**: **json** *[contains details of class]*
    - **string**: **int** *[details of topic of class]*

## Debug options
When calling `krunker_api`, you can append the following named arguments:
- `show_window=True` (default `False`):
  - Disables headless mode
- `load_images=True` (default `False`):
  - Enables loading of images
- `debug=True` (default `False`):
  - Enables `show_window` and `load_images`
  - Lets you interact with the browser window and waits for you to press [Enter] in the console, then continues program flow

## Contributors
- GoonMandu - [Krunker](https://krunker.io/social.html?p=profile&q=GoonMandu) - [GitHub](https://github.com/goonmandu)
- a6a6 - [Krunker](https://krunker.io/social.html?p=profile&q=a6a6) - [GitHub](https://github.com/a7a7-7)

## Caveats
The Krunker Social page HTML is subject to change, and therefore this API might fail in the future.

If you happen to use this API and if it does not work, please edit the HTML div IDs that are hardcoded into the scraper yourself.

Thank you.
