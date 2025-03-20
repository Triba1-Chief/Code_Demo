//No collaborations
import java.util.*;

public class Complete_Search_Ballgame {
	static HashMap<String, int[]> previousBoards; //Tracks board setups
	static int globalBestSteps;

	public static int[] game(String[][] board) {
		//Board is 5x9 in size
		// # represents walls, o represents balls, . represents holes
		previousBoards = new HashMap<>();
		globalBestSteps = Integer.MAX_VALUE;
        return play(board, 0);
	}

	//Runs the movements keeping current steps local to each board
	public static int[] play(String[][] board, int currentSteps) {
		//Prune solutions leading to high steps than already there
		if (currentSteps >= globalBestSteps) {
			return new int[]{Integer.MAX_VALUE,Integer.MAX_VALUE};
		}

		//Check if this board set up has been achieved before
		String boardKey = Arrays.deepToString(board);
		if (previousBoards.containsKey(boardKey)) {
			return previousBoards.get(boardKey);
		}


		ArrayList<int[]> ballPositions = new ArrayList<>();
		HashMap<String, ArrayList<int[]>> ballNeighbours = new HashMap<>(); //a ball with its eatable neighbours
		boolean canEat = false; //checks if at least one eatable neighbour in the game

		//Identifying ball positions and their eatable neighbours
		for (int i = 0; i < board.length; i++) {
			for (int j = 0; j < board[i].length; j++) {
				if (board[i][j].equals("o")) {
					ballPositions.add(new int[]{i, j});
					String key = i + "," + j;
					ballNeighbours.put(key, new ArrayList<>());

					// Check vertical moves
					if (i - 2 >= 0 && board[i - 1][j].equals("o") && board[i - 2][j].equals(".")) {
						ballNeighbours.get(key).add(new int[]{i - 1, j});
						canEat = true;
					}
					if (i + 2 < board.length && board[i + 1][j].equals("o") && board[i + 2][j].equals(".")) {
						ballNeighbours.get(key).add(new int[]{i + 1, j});
						canEat = true;
					}

					// Check horizontal moves
					if (j - 2 >= 0 && board[i][j - 1].equals("o") && board[i][j - 2].equals(".")) {
						ballNeighbours.get(key).add(new int[]{i, j - 1});
						canEat = true;
					}
					if (j + 2 < board[i].length && board[i][j + 1].equals("o") && board[i][j + 2].equals(".")) {
						ballNeighbours.get(key).add(new int[]{i, j + 1});
						canEat = true;
					}
				}
			}
		}

		//Base case: Either no balls are neighbours or no valid hole to capture
		if (!canEat || ballPositions.size() == 1) {
			if (ballPositions.size() == 1) { //Early termination if only 1 ball left
				globalBestSteps = Math.min(globalBestSteps, currentSteps);
			}

			int[] result = {ballPositions.size(), currentSteps};
			previousBoards.put(boardKey, result);
			return result;
		}

		//Recursion: Complete search
		int bestSteps = Integer.MAX_VALUE;
		int numberOfBalls = Integer.MAX_VALUE;

		String[][] tempBoard = new String[board.length][board[0].length];

		for (int i = 0; i < board.length; i++) { //Creating board that tracks the movements
			tempBoard[i] = board[i].clone();
		}

		for (int[] ballPosition : ballPositions) {
			String key = ballPosition[0] + "," + ballPosition[1];

			for (int[] neighbour : ballNeighbours.get(key)) {
				int a = ballPosition[0], b = ballPosition[1], x = neighbour[0], y = neighbour[1];
				int newRow = a + (x - a) * 2, newCol = b + (y - b) * 2;
				tempBoard[newRow][newCol] = "o"; //Landing position
				tempBoard[x][y] = "."; // Empty the jumped-over space
				tempBoard[a][b] = "."; //Empty the initial ball position

				//Getting the best outcome
				int[] result = play(tempBoard, currentSteps + 1);
				if (result[0] < numberOfBalls || result[0] == numberOfBalls && result[1] < bestSteps) {
					bestSteps = result[1];
					numberOfBalls = result[0];

					if (numberOfBalls == 1) {
						globalBestSteps = bestSteps;
					}
				}

				//Backtracking
				tempBoard[newRow][newCol] = ".";
				tempBoard[x][y] = "o";
				tempBoard[a][b] = "o";
			}
		}

		//Returning best results for every unique board setup
		int[] result = {numberOfBalls, bestSteps};

		if (numberOfBalls != Integer.MAX_VALUE) {
			previousBoards.put(boardKey, result);
		}

		return result;
	}
}
