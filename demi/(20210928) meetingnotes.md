# Meeting Note 1

## Project: Masked Facial Recognition
## Date: 2021/09/28

## Participants
**Student**: Zhang Yuwei (DB827468)<br />
**Supervisor**: Prof. Bob Zhang

## Discussion
- The main target of this final year project<br />
  This project aims to construct a high-accuracy facial recognition system that can recognize enrollee even if there is a mask on enrollee’s face. The whole project can be divided into two parts: algorithm (model training and adjusting) and implementation (software construction). 
- How to conduct a literature survey and what to include.
- The selection of dataset used in this project.<br />
  For the dataset selection, there are two possible choices: 
   1.	using the dataset with masked face 
   2.	using normal facial recognition dataset (e.g. CASIA-WebFace) and then covering the image with the tool MaskTheFace to generate masked face. <br />

  The current decision is first trying simulated masked face.
  
- Determine the regular meeting time in the rest of semester.<br />
The meeting in this semester is determined on Tuesday every week starting from October 12th).

## Next Meeting Targets
Algorithm part
- Check the testing performance of simulated masked face images.<br />
If the result is not very good, the dataset will be changed to these with real world mask face images.

Implementation part
- Discuss about the structure of the recognition system to be build.<br />
For example, on what kind of server and platform should the facial recognition system runs. 

## Literature Survey
- Masked Face Recognition for Secure Authentication (The paper introducing the tool MaskTheFace)
