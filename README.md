
# CVRP problem 

## Installation
1. Clone the repository: `git clone https://github.com/alaa672002/FYP.git`
2. Navigate to the project directory: `cd FYP`
3. Install dependencies: `pip install -r requirements.txt`


## Git Practices Workflow

After cloning the repository, 

### Checkout to the desired branch

`git checkout master`

### Pull Changes
Before starting your work or making changes, it's a good practice to pull the latest changes from the remote repository.

`git pull`

### Make Changes
Make your changes to the code.

### Stage Changes
After making changes, stage the files you want to commit.

`git add .`

### Commit Changes
Commit your changes with a descriptive message.

`git commit -m "Brief description of changes"`

### Push Changes
Push your changes to the remote repository.

`git push`

### Pulling Changes Made by Others
If your collaborator has pushed changes to the remote repository, you need to pull those changes before you push yours.

`git pull`

### Additional Notes
Before pushing changes, it's always a good idea to run tests locally to ensure that your changes are working as expected.

Communicate with your collaborator to avoid conflicts and coordinate changes effectively.


## Postcode Fetcher Script

This Python script fetches postcode data using the postcodes.io API and generates a CSV file with modified data.

### How to Run
1. Run the script: `python fetch_postcodes.py`

## Compute Distance Matrix Script

This Python script provides a solution for computing distance matrices between geographical points, enabling efficient analysis and utilization of location-based data. It uses google cloud api. 

### How to Run
1. Replace config.api_key in config.py with your API key.
2. Run the script: `python compute_distance_matrix.py`

## API Distance Matrix Script

This Python script utilizes an external API https://distancematrix.ai/nonprofit to calculate distance and duration matrices between pairs of geographical coordinates. The calculated matrices are stored in JSON files for further analysis. The API is free up to 1000 requests.

### How to Run
1. Replace config.api_key in config.py with your API key.
2. Run the script: `python apidistancematrix.py`