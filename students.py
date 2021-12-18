import math
import random

from agents import Agent
from enum import Enum


# Example agent, behaves randomly.
# ONLY StudentAgent and his descendants have a 0 id. ONLY one agent of this type must be present in a game.
# Agents from bots.py have successive ids in a range from 1 to number_of_bots.
class StudentAgent(Agent):
    def __init__(self, position, file_name):
        super().__init__(position, file_name)
        self.id = 0

    @staticmethod
    def kind():
        return '0'

    # Student shall override this method in derived classes.
    # This method should return one of the legal actions (from the Actions class) for the current state.
    # state - represents a state object.
    # max_levels - maximum depth in a tree search. If max_levels eq -1 than the tree search depth is unlimited.
    def get_next_action(self, state, max_levels):
        actions = self.get_legal_actions(state)  # equivalent of state.get_legal_actions(self.id)
        chosen_action = actions[random.randint(0, len(actions) - 1)]
        # Example of a new_state creation (for a chosen_action of a self.id agent):
        # new_state = state.apply_action(self.id, chosen_action)
        return chosen_action


class Player(Enum):
    MAX = 0
    MIN = 1


class MinimaxAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        action, score = self.minimax(state, max_levels, Player.MAX)
        return action

    def minimax(self, state, max_levels, player):
        agent_id = self.id if state.last_agent_played_id != self.id else \
            list(filter(lambda agent: agent.id != self.id, state.agents))[0].id
        actions = state.get_legal_actions(agent_id)

        if max_levels == 0:
            if player == Player.MAX:
                score = -math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent_id, action)
                    number_of_min_agent_actions = len(new_state.get_legal_actions(state.last_agent_played_id))
                    if score < number_of_min_agent_actions:
                        score = number_of_min_agent_actions
                        best_action = action
                return best_action, score
            else:
                score = math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent_id, action)
                    number_of_max_agent_actions = len(new_state.get_legal_actions(state.last_agent_played_id))
                    if score > number_of_max_agent_actions:
                        score = number_of_max_agent_actions
                        best_action = action
                return best_action, score

        if len(actions) == 0:
            return None, 1 if player == Player.MIN else -1

        if player == Player.MAX:
            score = -math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent_id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1, Player.MIN)
                if score < minimax_score:
                    score = minimax_score
                    best_action = action
            return best_action, score
        else:
            score = math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent_id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1, Player.MAX)
                if score > minimax_score:
                    score = minimax_score
                    best_action = action
            return best_action, score


class MinimaxABAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        alpha = -math.inf
        beta = math.inf
        action, score = self.minimax(state, max_levels, Player.MAX, alpha, beta)
        return action

    def minimax(self, state, max_levels, player, alpha, beta):
        agent_id = self.id if state.last_agent_played_id != self.id else \
            list(filter(lambda agent: agent.id != self.id, state.agents))[0].id
        print(f"Agent id: {agent_id}")
        actions = state.get_legal_actions(agent_id)
        print(f"Agent actions: {actions}")

        if max_levels == 0:
            if player == Player.MAX:
                print("MAX player on level 0")
                score = -math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent_id, action)
                    number_of_min_agent_actions = len(new_state.get_legal_actions(state.last_agent_played_id))
                    if score < number_of_min_agent_actions:
                        score = number_of_min_agent_actions
                        best_action = action
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break
                print(f"MAX player on level 0 with score: {score}")
                return best_action, score
            else:
                print("MIN player on level 0")
                score = math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent_id, action)
                    number_of_max_agent_actions = len(new_state.get_legal_actions(state.last_agent_played_id))
                    if score > number_of_max_agent_actions:
                        score = number_of_max_agent_actions
                        best_action = action
                    beta = min(beta, score)
                    if alpha >= beta:
                        break
                print(f"MIN player on level 0 with score: {score}")
                return best_action, score

        if len(actions) == 0:
            print(f"Player {player} has no more actions to choose")
            return None, 1 if player == Player.MIN else -1

        if player == Player.MAX:
            print(f"Player MAX on the move")
            score = -math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent_id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1, Player.MIN, alpha, beta)
                if score < minimax_score:
                    score = minimax_score
                    best_action = action
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            print(f"Player MAX with action: {best_action} and score: {score}")
            return best_action, score
        else:
            print("Player MIN on the move")
            score = math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent_id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1, Player.MAX, alpha, beta)
                if score > minimax_score:
                    score = minimax_score
                    best_action = action
                beta = min(beta, score)
                if alpha >= beta:
                    break
            print(f"Player MIN with action: {best_action} and score: {score}")
            return best_action, score


class ExpectAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        pass


class MaxNAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        pass
