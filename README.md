
# Undertabler
Experimental tool for generating foregrounds for TUCMC schedule generator.

## Installation:
### prerequisites:
- python 3.12 or later
- cloned this entire repo

1. Install playwright through pip
	`pip install playwright` or `py -m pip install playwright`
2. Chromium on Playwright
	`playwright install chromium`
## Usage:
Upon running, this program automatically finds .json files in a folder named "input" in the same directory as the script, and outputs it in a folder called "output" in the same directory. 

Expected json format is provided in sampledata folder or more can be get from https://github.com/triamudomcmc/schedule-generator/tree/main/_keep/data 
(ONLY DATA AFTER 2567 IS SUPPORTED)

## Documentation:
### Modifications:
- If any stylistic changes is required is it recommended to edit it in template.py as the css file is stored there.
- Changing text color is done through
### Workflow:
Json --> Playwright Renderer --> gets CSS info from template.py --> Screenshot headless chromium from playwright --> output
