# Presentation Coach!

This project was made in 24 hours by our team (Justin, Isaac, Brice). However, some changes were made after the competition.

The project earned us an honorable mention, only being 1 of 2 teams to do so.

## Problem
Effective communication is crucial for engaging audiences during presentations, yet many speakers struggle with maintaining audience attention, delivering content clearly, and optimizing their delivery style. Common challenges include:

1. **Audience Engagement**: Speakers often lack real-time feedback on audience attention, leading to disengagement and reduced retention of information.

2. **Content Delivery**: Presenters frequently experience difficulties in synchronizing their speech with visual aids, leading to confusion and a disjointed experience for the audience.

3. **Self-awareness**: Many speakers are unaware of their speaking habits, such as excessive filler words, repetitive phrases, or inappropriate pacing, which can detract from their message.

4. **Skill Development**: Aspiring presenters often lack access to personalized coaching and feedback that can help them refine their skills and enhance their performance.

The Presentation Coach project addresses these challenges by providing a comprehensive tool that analyzes both verbal and visual presentation elements. By leveraging audio analysis, unique word tracking, and audience engagement metrics through eye-tracking technology, the system offers actionable insights and real-time coaching. This enables users to enhance their presentation skills, maintain audience attention, and deliver information more effectively, ultimately leading to more impactful and memorable presentations.

## How it Works
First, the user must record a video of the audience. Then they will upload 2 files: the video file and the PowerPoint file. Our code then looks through every slide of the powerpoint and assigns keeps track of the unique words on every slide. It also splits the recording into a video file and an audio file.

Then, it will match up the audio file with each slide, using the unique words to direct which slide the user is currently talking about. As seen below with the vertical lines on the graph, the program will detect these slide changes by recognizing that a new set of unique words is being used. For example, if the second slide were to talk about "updates," a word not found on any other slide, it would be identified as unique. Then, when fuzzy sort takes in the word "updates" from the audio file, it knows that a new slide is being talked about, so it can draw a new vertical line.

The program also utilizes OpenCV to track the eyes. Based on how many people are looking at the screen provides the retention stat. When someone starts to look away or stop paying attention, OpenCV will recognize that. As graphed below, this retention is graphed over time, and vertical lines are drawn whenever there is a slide change.

With the audio file, we are also able to pull repeated words, words per minute, and filler words. Through this, we can use AI to "coach" the user, telling them to stop repeating/stuttering, slow/speed up their words per minute, or take out filler words.

All of the backend/AI/CV/data storage done in Python/Flask. The frontend was done using Next.js
 <img width="1679" alt="image" src="https://github.com/user-attachments/assets/2c7b9787-19fc-4850-bc94-686f2e745164">

## Future implementations
- Add a page that takes in the pptx file upload and mp4 file upload (for now it is done locally)
- Add a loading screen page
- Scale the project to work with multiple cameras from different angles to use in a larger classroom setting
