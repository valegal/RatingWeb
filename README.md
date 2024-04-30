# Movie Ranking Web Application

A web application built with Flask that allows users to rank and review movies. Users can add movies to the ranking list, rate them out of 10, and provide reviews. The movie data is fetched from the MovieDB API.

## Features

- View a list of movies ranked by their rating
- Add new movies to the ranking list
- Edit the rating and review of existing movies
- Delete movies from the ranking list

## Prerequisites

- Python 3.x
- MovieDB API Key

## Getting Started

1. Clone the repository.

2. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

3. Set up the environment variables:
   - Create a `.env` file in the project root directory.
   - Add the following variables to the `.env` file:
     - `MOVIE_DB_API_KEY`: Your MovieDB API key.
     - `SECRET_KEY`: Secret key for Flask session management.

4. Run the application:

   ```shell
   python main.py
   ```

5. Access the application in your web browser at `http://localhost:5000`.

## Usage

- Home Page: Displays a list of movies ranked by their rating. Users can view the movie title, year, description, and the current rating. The movies are sorted in ascending order based on their rating.

- Add Movie: Allows users to add a new movie to the ranking list. Users enter the movie title, and the application fetches the movie details from the MovieDB API. If the movie is found, users can select it from the search results.
- Edit Movie: Users can edit the rating and review of a movie. Enter the rating out of 10 and provide a review. Click "Done" to update the movie's information.

- Delete Movie: Users can delete a movie from the ranking list. Click the delete button next to the movie to remove it from the list.

## Error Handling

The application provides error handling for common errors:

- 404 Page Not Found: If a user tries to access a page that doesn't exist, a 404 error page is displayed with a message indicating the page was not found.

- 500 Internal Server Error: If an internal server error occurs, a 500 error page is displayed with a message indicating the error.

## Technologies Used

- Flask: Web framework used for building the application.
- SQLAlchemy: ORM (Object-Relational Mapping) library for database management.
- Flask-WTF: Flask extension for handling web forms.
- Flask-Bootstrap: Flask extension for integrating Bootstrap styles.
- MovieDB API: External API used to fetch movie data.
