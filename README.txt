Read work process in work_process.txt
Works on python 2.7

Installation:
------------------
Open terminal in project directory.
pip install -e .


Run Code:
-------------------

To run and test modules, go to example_usage/bcc and example_usage/flights.
In example_usage/flights, change `CHROME_DRIVER_LOCATION` to the location of your chrome driver.
First execute download module, then extract + save module, then search module.

After first download you can re-extract without dependency on the download module.
After first extraction and save of the raw material you can search for text without dependency on
the "extract + save" module.


Design:
---------------
`DataDownloader` is the base class for all download materials before extraction.
Each instance downloads material from a certain web page and saves it to a directory.
`DataDownloader` subclasses must only implement one-time download of material, some may also
implement repetitive download, such as FlightLandingScheduleDownloader.


`RawMaterial` is the "heart" of the system. It contains raw data after extraction, that can be later
searched by analyzers.
It is a serializable object which can be loaded from a file or dumped to a file.
Other serialization methods can also be added and be useful for analyzers to search for data.


`MaterialExtractor` extracts a single file that was previously downloaded by a `DataDownloader`, to
a respective list of raw material `RawMaterial`, meaning that each downloaded file can be extracted
to one or many `RawMaterial` object.


analyzers.py contains functions that perform analysis on raw material.
So far analyzer only perform analysis on files' text only, but one can implement analyzers that work
directly with `RawMaterial` objects and/or can perform other analysis, e.g. search for text only in
BBC article headers, search for delayed flights etc.


utils.py contains extra manipulations that are not given out of the box by the above
classes/modules.
Current functions are for the use of this assignment example usage.

common.py contains variable/functions common to more than one module.
