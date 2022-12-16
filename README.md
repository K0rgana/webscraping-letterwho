# webscraping-letterwho

web scraping doctor who content for letterwho

### Run the project

1. Clone this repository
   ```bash
   git clone https://github.com/K0rgana/webscraping-letterwho.git
   ```
1. Create <b>& activate</b> the python virtual environment
   ```bash
   python -m venv venv # create py virtual environment
   .\venv\Scripts\activate.ps1 #activate virtual environment on windows
   ```
1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
1. Edit the variable <b>"u_range"</b> (line 12) of the file <b>"bigfinish.com/bigfinish/spiders/bf_stories.py"</b> to the url of choice

   ```python
   #bigfinish.com>bigfinish>spiders>bf_stories.py

   # See who the url is divided:
   #              |           base         |      range       | page |           filters
   #urlExemple = 'https://www.bigfinish.com/ranges/v/torchwood/page:{}?url=ranges/v/torchwood&sort_ordering=date_asc'

   #PASTE INSIDE THE ' ' AND AFTER THE "/v/" THE RANGE NAME/URL FROM BIG FINISH SITE
   u_range= 'ranges/v/torchwood' # Before
   u_range= 'ranges/v/doctor-who---companion-chronicles' # After
   ```

1. Run the file of choice with python. This will generate a file with the data
   ```bash
   python bigfinish.com/bigfinish/spiders/bf_stories.py
   ```
