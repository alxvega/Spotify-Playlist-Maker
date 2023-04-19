# Spotify Playlist Creator

This is a Python script that automates the process of creating a Spotify playlist with the albums of the given artists.

## Prerequisites

To run this script, you need to have the following:

- Python 3.8 or higher
- Chrome web browser
- ChromeDriver

## Installation

1. Clone this repository.
2. Install the required Python packages by running `pip install -r requirements.txt`.
3. Download and install ChromeDriver from [here](https://chromedriver.chromium.org/downloads). Make sure to add the location of the `chromedriver` executable to your system's `PATH` environment variable.

## Usage

To use this script, follow these steps:

1. Create a .env file which has your login credentials as follows:

```
EMAIL=myemail@email.com
PASSWORD=mypassword
```

2. Open your terminal and navigate to the directory where the script is located.
3. Run the script with the following command:

```
python spotify_playlist_creator.py -playlistname <playlist_name> -artists <artist_1>,<artist_2>,...,<artist_n>
```

Replace `<playlist_name>` with the name you want to give to your playlist, and `<artist_1>,<artist_2>,...,<artist_n>` with the names of the artists whose albums you want to add to the playlist. Separate the artist names with commas and do not include any spaces before or after the commas.

For example:

```
python spotify_playlist_creator.py -playlistname "My Playlist" -artists "The Beatles","Pink Floyd","Led Zeppelin"
```

This script will run in windowed mode by default. If you'd like to run it in a headless manner, add --headless flag at the end of the command.

This will create a new playlist called "My Playlist" and add all the albums of The Beatles, Pink Floyd, and Led Zeppelin to the playlist.

4. The script will open a Chrome window and navigate to the Spotify website. It will then log in to your Spotify account and create a new playlist with the given name.
5. For each artist in the list, the script will search for the artist's page on Spotify, select the "Albums" section, and add all the albums of the artist to the playlist.
6. After all the artists have been processed, the script will rename the playlist to the given name.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### TODOS:

- Dockerizing
