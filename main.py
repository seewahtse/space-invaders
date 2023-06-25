import turtle
import os
import math
import random

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("triangle")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerspeed = 15

# Choose a number of enemies
number_of_enemies = 5
# Create an empty list of enemies
enemies = []

# Add enemies to the list
for i in range(number_of_enemies):
    # Create the enemy
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.color("red")
    enemy.shape("circle")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)

enemyspeed = 2

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 20

# Define bullet state
# ready - ready to fire
# fire - bullet is firing
bulletstate = "ready"

# Score
score = 0

# Score pen
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" % score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Game over pen
game_over_pen = turtle.Turtle()
game_over_pen.speed(0)
game_over_pen.color("white")
game_over_pen.penup()
game_over_pen.setposition(0, 0)
game_over_pen.hideturtle()

# Move the player left and right
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = - 280
    player.setx(x)


def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)


def fire_bullet():
    # Declare bulletstate as a global if it needs changed
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "fire"
        # Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()


def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        # Draw an explosion at the location of the collision
        explosion_pen = turtle.Turtle()
        explosion_pen.speed(0)
        explosion_pen.color("orange")
        explosion_pen.penup()
        explosion_pen.setposition(t2.xcor(), t2.ycor())
        explosion_size = 1
        for i in range(10):
            explosion_pen.dot(explosion_size)
            explosion_size += 5
            explosion_pen.forward(10)
            explosion_pen.right(10)
        # Hide the enemy and remove it from the game
        enemy.hideturtle()
        enemies.remove(enemy)
        explosion_pen.clear()
        return True
    else:
        return False

# Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

# Main game loop
while True:

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # Move the enemy back and down
        if enemy.xcor() > 280:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemyspeed *= -1

        if enemy.xcor() < -280:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemyspeed *= -1

        # Check for a collision between the bullet and the enemy
        if isCollision(bullet, enemy):
            # Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            # Update the score
            score += 1
            scorestring = "Score: %s" % score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

        # Check for a collision between the player and the enemy
        if isCollision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            game_over_pen.write("Game Over", align="center", font=("Arial", 30, "normal"))
            play_again = wn.textinput("Play Again?", "Do you want to play again? (y/n)")
            if play_again.lower() == "y":
                # Reset the game
                game_over_pen.clear()
                player.setposition(0, -250)
                player.showturtle()
                for enemy in enemies:
                    enemy.hideturtle()
                enemies.clear()
                for i in range(number_of_enemies):
                    # Create the enemy
                    enemies.append(turtle.Turtle())

                for enemy in enemies:
                    enemy.color("red")
                    enemy.shape("circle")
                    enemy.penup()
                    enemy.speed(0)
                    x = random.randint(-200, 200)
                    y = random.randint(100, 250)
                    enemy.setposition(x, y)

                score = 0
                scorestring = "Score: %s" % score
                score_pen.clear()
                score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
            else:
                wn.bye()
                break

    # Move the bullet
    y = bullet.ycor()
    y += bulletspeed
    bullet.sety(y)

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

    # Check for a victory
    if score == number_of_enemies:
        game_over_pen.write("You win!", align="center", font=("Arial", 30, "normal"))
        play_again = wn.textinput("Play Again?", "Do you want to play again? (y/n)")
        if play_again.lower() == "y":
            # Reset the game
            game_over_pen.clear()
            player.setposition(0, -250)
            player.showturtle()
            for enemy in enemies:
                enemy.hideturtle()
            enemies.clear()
            for i in range(number_of_enemies):
                # Create the enemy
                enemies.append(turtle.Turtle())

            for enemy in enemies:
                enemy.color("red")
                enemy.shape("circle")
                enemy.penup()
                enemy.speed(0)
                x = random.randint(-200, 200)
                y = random.randint(100, 250)
                enemy.setposition(x, y)

            score = 0
            scorestring = "Score: %s" % score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
        else:
            wn.bye()
            break

wn.mainloop()