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

# Plots
# Score over 1000 generations
Plots the top 5 snakes from each Generation over 1000 generations
![win_score_vs_time_2](https://github.com/user-attachments/assets/32f44c36-8ce0-4c7d-8c06-2f5b00fa10f0)

# Score over 5000 generations
Plots the top 5 snakes from each Generation over 5000 generations
![5000_score_vs_time](https://github.com/user-attachments/assets/d3357e79-9cbd-45ae-81c6-df1a77144a80)

# Age over 1000 generations
Plots the top 5 snakes from each Generation over 1000 generations
![win_age_over_time_2](https://github.com/user-attachments/assets/807738a1-c6fb-4722-8130-d836eb27326e)


# Food sensors
The lighter the colour, the higher the weight. Map from 0 (dark purple) to 1.0 (light yellow)
![food_sensors_5000](https://github.com/user-attachments/assets/a8761e0f-358f-4ab6-8631-323b245ecace)
