# Cube

Cube is a 3 dimentional texting platform which it's aim is to combine emotions with text. The emotion is captured from the webcam and the user's emotion will be determined by an Artificial Intelligence (AI) which will then be represented in the chat using emojis. This project is a university project made for grading in a class called "Cognitive Computing".

## How does it work?

### Overall

[![1682407723120](image/README/1682407723120.png)]()

*Block diagram of how the overall chat works*

The app works as seen in the flowchat. First, the sender sends message which will be stored on the Firebase's Real Time Database. Next, the thread on the reciever's side will detect change on the number of messages stored on the Firebase's message database and would retrieve the updated message as a dictionary. The message is then displayed and updates on the Tkinter. After the message is shown, the reciever's camera will turn on and the AI would record the emotion of the reader for a period of time. Then it would return the information on the current emotion and send it to Firebase. The sender's emotion thread would detect change on the message emotions and updates the emotion's emoji. This works in both ways as the reciever can be sender and the sender can also be reciever.

### Emotion AI using YOLO

## Required Libraries

- Firebase_admin
- Tkinter
- Pillow
- Customtkinter

## Collaborators

Chissanu Kittipakorn 64011728

Pattarapark Chutisamoot 64011532

Phanuruj Sotthidat 64011544

Puttipong Aunggulsant 64011595

Siraphop Mukdaphetcharat 64011614

Thanakrit Paisal 64011666
