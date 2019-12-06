# Github Statistics & Screenshots Crawler

From the list of the website, gets the numbers of

- Watches
- Stars
- Forks
- Issues
- Commits
- Branches
- Releases
- Contributors
- Clones: Permission needed
- Visitors: Permision needed
- Visitors(unique): Permision needed

## Usage

1. Install Chromedriver

   > I'm not sure this step correctly works.
   > If the installation method below does not work well,
   > I recommend you to google about installing chromedriver.

   The commands below is for version 79.0.  
   **Chrome must be installed**

   - Ubuntu

   ```bash
   wget https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip
   unzip chromedriver_linux64.zip
   chmod +x chromedriver
   sudo mv chromedriver /usr/local/bin/
   ```

   - Mac

   ```bash
   wget https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_mac64.zip
   unzip chromedriver_linux64.zip
   chmod +x chromedriver
   sudo mv chromedriver /usr/local/bin/
   ```

   - Windows: To be updated(I do not recommend)

2. Install requirements

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `options.py.sample` and edit `options.py`

   ```python
   CREDENTIAL = {
     'id': 'YOURID',
     'pw': 'YOURPW'
   }
   ```

4. Copy `url_list.csv.sample` and edit `url_list.csv`

   > Warning: All urls in the csv must not end with /(slash).

5. Execute `crawl.py`

   ```bash
   python crawl.py
   # If you don't have permission to all repositories
   python crawl.py --no_permission
   # If you want to change timeout
   python crawl.py --timeout=<SECONDS>
   ```
