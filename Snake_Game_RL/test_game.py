from game import SnakeGame
import time

def main():
    print("=" * 50)
    print("SNAKE GAME - Manual Control")
    print("=" * 50)
    print("\n🎮 CONTROLS:")
    print("   ⬆️  UP Arrow    - Go Straight")
    print("   ➡️  RIGHT Arrow - Turn Right")
    print("   ⬅️  LEFT Arrow  - Turn Left")
    print("   🔄  R Key       - Restart Game")
    print("   ❌  Close Window - Quit")
    print("\n🏆 The snake speeds up as you eat more food!")
    print("💡 Try to get the highest score!\n")
    print("Starting game in 2 seconds...")
    time.sleep(2)
    
    # Create game instance
    game = SnakeGame()
    
    # Game loop
    running = True
    while running:
        # Play a step - action=None means use keyboard input
        reward, done, score = game.play_step(action=None)
        
        # If game is over, wait for key press to restart
        if done:
            print(f"💀 Game Over! Score: {score}")
            # The game will restart when any key is pressed (handled in game.py)
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Game closed by user")
    except Exception as e:
        print(f"\n❌ Error: {e}") 