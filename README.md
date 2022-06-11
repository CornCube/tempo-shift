# tempo-shift
Downloads and converts tracks from YouTube into a specific rhythm. 

![](demo.gif)

## Features
* Download songs straight from YouTube using individual links, public playlists, or video titles
* Converts tracks into an inputted tempo with the option to add a click track in the background
* Automatically finds the tempo of a song using librosa bpm estimation
* Combines tracks into a single file for ease of use

## Installation
Download dist.zip from the releases tab and extract to a folder.

## Usage
To get started, just run 'main.exe'. Original songs are saved in the 'data' folder, results are saved in the 'adjusted' folder.

**NOTE: Works best with songs that are 1) similar in tempo to the desired tempo and 2) have a fairly consistent rhythm**

**NOTE part 2: If the tempo of the song in question is much higher/lower than the tempo that you are shifting to, it is better to use a halved/doubled tempo to avoid distorting the original song too much. 
For example, 'The Top' by Ken Blast is 160 bpm. If we are shifting it to 88 bpm, use 80 bpm as the actual value instead of 160 bpm to prevent the song from being slowed by ~50%.**

### Options
1. Enter a link to a youtube playlist
   * Playlist *must* be public
2. Enter links to youtube videos
3. Enter song names
   * Pulls the first result that comes up, so be as specific as possible
4. Continue to track creation 
   * Choose bpm to shift to
   * Decide whether or not to combine all the tracks into one file
   * Decide whether or not to add a click track to files
   * Enter the actual bpm of the song or accept an estimation (Remember to double/halve bpm as needed to prevent distortion)
5. Exit

## Resources
Automatic tempo calculation is just an approximate estimation, so it is recommended to find accurate information online instead. 

* https://songbpm.com/
* https://tunebat.com/Analyzer
* https://www.beatsperminuteonline.com/

## Issues
* Click track (metronome) is not accurate all of the time
* If using an estimation, the factor that the song is multiplied by is slightly off resulting in a less accurate track
* Song tempo should be divided/multiplied by 2 to stay as close as possible to the tempo you are shifting to

## Dependencies
* ffmpeg
* ffprobe
* [rubberband](https://pypi.org/project/pyrubberband/)
* [pytube](https://pypi.org/project/pytube/)
* [librosa](https://pypi.org/project/librosa/)
* [pydub](https://pypi.org/project/pydub/)
