# COE418_Project (Locatable Webapp)

## File Structure

- `server.py` Main Flask Server File - Includes Backend and Routing
- `utils.py` Python Database Utilities - Functions and Queries
- **templates** folder - Contains all **HTML** files
- **static** folder - Contains all static files including **CSS** and **media**

## Usage Instructions
**Clone repository to local directory & change directory to project folder**
1. Create python vitrual environment
   ```python
      python3 -m venv venv
   ```
2. Activate virtual machine
   ``` python
      source venv/bin/activate
   ```
3. Install python modules
   ```python
      pip install -r requirements.txt
   ```
4. Start Flask Server
   ```python
      python3 server.py
   ```
> Flask Server will launch at http://localhost:5000
