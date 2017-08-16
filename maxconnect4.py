import sys
from MaxConnect4Game import *

def oneMoveGame(currentGame):
    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'
        sys.exit(0)

    currentGame.aiPlay(4,currentGame.gameBoard) # Make a move (only random is implemented)

    print 'Game state after my move:'
    currentGame.printGameBoard()

    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()


def interactiveGame(currentGame, in_file, out_file, out_file2):

    while currentGame.pieceCount != 42:    # Is the board full already?
        
        if currentGame.currentTurn==1:
            currentGame.aiPlay(4,currentGame.gameBoard) # Make a move (only random is implemented)

            print 'Game state after move:'
            currentGame.printGameBoard()

            
            currentGame.currentTurn=2

            currentGame.gameFile=open(out_file2,"w")

            currentGame.printGameBoardToFile()
            currentGame.gameFile.close()
            currentGame.countScore()
            print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

            
        else:
            player=currentGame.currentTurn
            try:
                move=input("enter your column number between 0 and 6 :")
            except:
                sys.exit("You didnt enter a column number. Game ends")
            currentGame.playPiece(move)
            print("Game state after user move:")
            currentGame.printGameBoard()
            print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
            currentGame.currentTurn=1
            currentGame.gameFile=open(out_file,"w")
            currentGame.printGameBoardToFile()

            
    print 'BOARD FULL\n\nGame Over!\n'
    if currentGame.player1Score > currentGame.player2Score:
        print("Player1 won")
    elif currentGame.player1Score < currentGame.player2Score:
        print("Player2 won")
    else:
        print("It's a Draw")
    sys.exit(0)

def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game() # Create a game

    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nError opening input file.\nCheck file name.\n")

    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.gameFile.close()

    print '\nMaxConnect-4 game\n'
    print 'Game state before move:'
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    if game_mode == 'interactive':
        player_turn = argv[3]
        if player_turn == "computer-next":
            currentGame.currentTurn = 1
        elif player_turn == "human-next":
            currentGame.currentTurn = 2
        else:
            print("Invalid player")
        in_file=argv[2]
        try:
            currentGame.gameFile = open(in_file, 'r')
        except:
            sys.exit('Error opening input file.')
        out_file = "human.txt"
        out_file2="computer.txt"

        try:
            currentGame.gameFile = open(out_file, 'w')
        except:
            sys.exit('Error opening output file.')
        try:
            currentGame.gameFile = open(out_file2, 'w')
        except:
            sys.exit('Error opening output file.')
        interactiveGame(currentGame,in_file, out_file, out_file2) # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)


