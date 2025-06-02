# Snakes on a (2D) Plane
* A simulation of a multi-agent snake game, where each snagent (snake agent) chooses its next movement using direct sensorimotor links.
* The sensors are a grid of adjustable size (e.g. 3x3, 5x5), oriented around the head of the snake
* The modalities of these sensors are snake head, snake body, wall, food, and empty
* The movements of the snake are constricted to: turn left, turn right, and go straight
* The weights for each sensory modality and movement are stored in a genome
* This genome is evolved over time using a genetic algorithm


This project requires unicurses.

# Video demo

https://github.com/user-attachments/assets/d954b52a-5c69-474e-8ed0-babc217579da

