# Labyrinth Escape (https://youtu.be/LQBxvPuu38U)

<h2> Description </h2>
This is a roguelike genre with procedurally generated dungeon terrain and randomly placed monsters and treasures scattered throughout.
The player is trapped in a multi-room dungeon where he would have to navigate to each room, while avoiding traps and enemies, and defeat all the enemies within the rooms. within each room, player will be able to:
Collect power-up items like health booster to increase the player's fighting capabilities.
After defeating the enemies within that room, player can then choose to move to another room.
After completing all the rooms, the player would then be directed to a final boss room where he would have to defeat a dynamic enemy before he can escape.

<h2> How to Run </h2>
Please run main.py 

<h2> Libraries Required </h2>
No additional libraries are required to be installed.

<h2> Shortcut Commands </h2>
Press B to enter boss mode, skipping remaining rooms
Press K in the splashscreen page before pressing the start button to generate the main maze using Kruskal's algorithm, else it use Prim's algorithm by default.

<h2> Instructions </h2>

* The player first starts off in a dungeon whereby there are several rooms to be explored
* Navigate through the dungeon to get to doors, using arrow keys
* Entering a room, the player would have to attack all the enemies in the room before a wall is generated and the player can return to the main dungeon
* Press space bar for the player to shoot bullets at the enemy
* There are special items such as health booster (red potion), time freezer (hourglass) and invisibility potion (blue potion)
* Explore all rooms and kill all enemies before the boss room is generated
* The boss would shoot bullets in the player's direction. The boss would also also produce lava which would move towards the direction of the player. Both bullets and lava would cause the player to lose some health.
* Defeat the boss to win the game and escape the dungeon.
