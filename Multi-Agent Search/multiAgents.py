from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        """
        First,call the minimax function.
        minimax:If every agents have returned value the value and action,this roun should be finished and set 
                agentIndex as zero which means it is time to get into player's turn,then depth pluse 1 to 
                represent how many round we are going to do.
                Either player is win/lose or the expected number of round is finished,we sould evaluate the 
                extent of nextState whether it is a good choice.If it is ghost's turn,return min_agent.else,return max_agent.
        max_agent:This is for player.First,the value named "best" is initialized as -inf and the variable used to 
                  record the best next action named "NextAction" is none.Use for loop to travel all the possible actions 
                  which are legal and know the next state corresponds to the legal action.Also,we get the low level of value 
                  to do the following comparison to find max value and turn it to "best".
        min_agent:This is for ghosts.First,the value named "best" is initialized as inf and the variable used to record the 
                  best next action named "NextAction" is none.Use for loop to travel all the possible actions which are legal 
                  and know the next state corresponds to the legal action.Also,we get the low level of value to do the following 
                  comparison to find min value and turn it to "best".
        """
        value,action=self.minimax(gameState,0,0)
        # print(action)
        return action
        raise NotImplementedError("To be implemented")


    def minimax(self,gameState,depth,agentIndex):
        if agentIndex>=gameState.getNumAgents():
            agentIndex=0
            depth+=1
        if gameState.isWin() or gameState.isLose() or (depth>=self.depth):
            return self.evaluationFunction(gameState), None
        if agentIndex!=0:
            return self.min_agent(gameState,depth,agentIndex)
        else:
            return self.max_agent(gameState,depth,agentIndex)
    
    def max_agent(self,gameState,depth,agentIndex):
        best=float('-inf')
        NextAction = None
        for action in gameState.getLegalActions(agentIndex):
            NextState=gameState.getNextState(agentIndex,action)
            value,_=self.minimax(NextState,depth,agentIndex+1)
            if value>best:
                best=value
                NextAction=action
        return best,NextAction
    
    def min_agent(self,gameState,depth,agentIndex):
        best=float('inf')
        NextAction = None
        for action in gameState.getLegalActions(agentIndex):
            NextState=gameState.getNextState(agentIndex,action)
            value,_=self.minimax(NextState,depth,agentIndex+1)
            if value<best:
                best=value
                NextAction=action
        return best,NextAction
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        """
        First,call the minimax function.
        minimax:If every agents have returned value the value and action,this roun should be finished and set agentIndex as zero 
                which means it is time to get into player's turn,then depth pluse 1 to represent how many round we are going to do.
                Either player is win/lose or the expected number of round is finished,we sould evaluate the extent of nextState 
                whether it is a good choice.If it is ghost's turn,return min_agent.else,return max_agent.
        max_agent:This is for player.First,the value named "best" is initialized as -inf and the variable used to record the best
                  next action named "NextAction" is none.Use for loop to travel all the possible actions which are legal and know the 
                  next state corresponds to the legal action.Also,we get the low level of value to do the following comparison to find 
                  max value and turn it to "best".If "best" is greater than beta,just break.If best is larger than alpha,alpha=best.
        min_agent:This is for ghosts.First,the value named "best" is initialized as inf and the variable used to record the best
                  next action named "NextAction" is none.Use for loop to travel all the possible actions which are legal and know the 
                  next state corresponds to the legal action.Also,we get the low level of value to do the following comparison to find 
                  min value and turn it to "best".
        The difference between part 1 and part 2 is that we need to note two variables:alpha and beta.
        The initial value of alpha is -inf.
        The initial value of beta is inf.
        """
        value,action=self.minimax(gameState,0,0,float('-inf'),float('inf'))#call minimax function
        # print(action)
        return action
        raise NotImplementedError("To be implemented")


    def minimax(self,gameState,depth,agentIndex,alpha,beta):
        if agentIndex>=gameState.getNumAgents():
            agentIndex=0
            depth+=1
        if gameState.isWin() or gameState.isLose() or (depth>=self.depth):
            return self.evaluationFunction(gameState), None
        if agentIndex!=0:
            return self.min_agent(gameState,depth,agentIndex,alpha,beta)
        else:
            return self.max_agent(gameState,depth,agentIndex,alpha,beta)
    
    def max_agent(self,gameState,depth,agentIndex,alpha,beta):
        best=float('-inf')
        NextAction = None
        for action in gameState.getLegalActions(agentIndex):
            NextState=gameState.getNextState(agentIndex,action)
            value,_=self.minimax(NextState,depth,agentIndex+1,alpha,beta)
            if value>best:
                best=value
                NextAction=action

            if best>beta:
                break
            if best>alpha:
                alpha=max(alpha,best)
        return best,NextAction
    
    def min_agent(self,gameState,depth,agentIndex,alpha,beta):
        best=float('inf')
        NextAction = None
        for action in gameState.getLegalActions(agentIndex):
            NextState=gameState.getNextState(agentIndex,action)
            value,_=self.minimax(NextState,depth,agentIndex+1,alpha,beta)
            if value<best:
                best=value
                NextAction=action
            if best<alpha:
                break
            if best<beta:
                beta=min(beta,best)
        return best,NextAction
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        """
        First,call the minimax function.
        The initial value of alpha is -inf.
        The initial value of beta is inf.
        minimax:If every agents have returned value the value and action,this roun should be finished and set agentIndex as zero 
                which means it is time to get into player's turn,then depth pluse 1 to represent how many round we are going to do.
                Either player is win/lose or the expected number of round is finished,we sould evaluate the extent of nextState 
                whether it is a good choice.If it is ghost's turn,return min_agent.else,return max_agent.
        max_agent:This is for player.First,the value named "best" is initialized as -inf and the variable used to record the best
                  next action named "NextAction" is none.Use for loop to travel all the possible actions which are legal and know the 
                  next state corresponds to the legal action.Also,we get the low level of value to do the following comparison to find 
                  max value and turn it to "best".If "best" is greater than beta,just break.If best is larger than alpha,alpha=best.
        min_agent:This is for ghosts.Use total_Num/the number of action to replace worst-case into average case.
        """
        value,action=self.minimax(gameState,0,0,float('-inf'),float('inf'))
        # print(action)
        return action
        raise NotImplementedError("To be implemented")


    def minimax(self,gameState,depth,agentIndex,alpha,beta):
        if agentIndex>=gameState.getNumAgents():
            agentIndex=0
            depth+=1
        if gameState.isWin() or gameState.isLose() or (depth>=self.depth):
            return self.evaluationFunction(gameState), None
        if agentIndex!=0:
            return self.min_agent(gameState,depth,agentIndex,alpha,beta)
        else:
            return self.max_agent(gameState,depth,agentIndex,alpha,beta)
    
    def max_agent(self,gameState,depth,agentIndex,alpha,beta):
        best=float('-inf')
        NextAction = None
        for action in gameState.getLegalActions(agentIndex):
            NextState=gameState.getNextState(agentIndex,action)
            value,_=self.minimax(NextState,depth,agentIndex+1,alpha,beta)
            if value>best:
                best=value
                NextAction=action
            if best>beta:
                break
            if best>alpha:
                alpha=max(alpha,best)
        return best,NextAction
    
    def min_agent(self,gameState,depth,agentIndex,alpha,beta):
        total_value=0
        actionNum=0
        NextAction = None
        for action in gameState.getLegalActions(agentIndex):
            NextState=gameState.getNextState(agentIndex,action)
            value,_=self.minimax(NextState,depth,agentIndex+1,alpha,beta)
            total_value+=value
            actionNum+=1
        best=total_value/actionNum
        return best,NextAction
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    """
    Use currentGameState to get ghosts'states,foodand capsule as list.Travel the list of food to calculate the distance between food and 
    player and refresh the list.Travel the list of capsule to calculate the distance between capsules and player and refresh the list. 
    Use currentGameState to update the score of the game and remain food and capsules.
    """
    GhostStates = currentGameState.getGhostStates()
    Pacman_Pos = currentGameState.getPacmanPosition()
    food_list = (currentGameState.getFood()).asList()
    capsule_list = currentGameState.getCapsules()
    no_food = len(food_list)
    no_capsule = len(capsule_list)

    state_score=0
    if currentGameState.getNumAgents() > 1:
        ghost_dis = min( [manhattanDistance(Pacman_Pos, ghost.getPosition()) for ghost in GhostStates])
        if (ghost_dis <= 1):
            return -10000
        state_score -= 1.0/ghost_dis
    current_food = Pacman_Pos
    for food in food_list:
        closestFood = min(food_list, key=lambda x: manhattanDistance(x, current_food))
        state_score += 1.0/(manhattanDistance(current_food, closestFood))
        current_food = closestFood
        food_list.remove(closestFood)
    current_capsule = Pacman_Pos
    for capsule in capsule_list:
        closest_capsule = min(capsule_list, key=lambda x: manhattanDistance(x, current_capsule))
        state_score += 1.0/(manhattanDistance(current_capsule, closest_capsule))
        current_capsule = closest_capsule
        capsule_list.remove(closest_capsule)
    state_score += 10*(currentGameState.getScore())
    state_score -= 8*(no_food + no_capsule)

    return state_score
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
