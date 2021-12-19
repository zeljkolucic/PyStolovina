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
        agents = state.agents
        last_agent_played_id = len(agents) - 1 if state.last_agent_played_id is None else state.last_agent_played_id
        agent = agents[(last_agent_played_id + 1) % len(agents)]
        actions = state.get_legal_actions(agent.id)

        if len(actions) == 0:
            return None, 100 if player == Player.MIN else -100

        if max_levels == 0:
            if player == Player.MAX:
                score = -math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent.id, action)
                    number_of_min_agent_actions = 8 - len(new_state.get_legal_actions(last_agent_played_id))
                    if score < number_of_min_agent_actions:
                        score = number_of_min_agent_actions
                        best_action = action
                return best_action, score
            else:
                score = math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent.id, action)
                    number_of_max_agent_actions = len(new_state.get_legal_actions(last_agent_played_id)) - 8
                    if score > number_of_max_agent_actions:
                        score = number_of_max_agent_actions
                        best_action = action
                return best_action, score

        if player == Player.MAX:
            score = -math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent.id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1, Player.MIN)
                if score < minimax_score:
                    score = minimax_score
                    best_action = action
            return best_action, score
        else:
            score = math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent.id, action)
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
        agents = state.agents
        last_agent_played_id = len(agents) - 1 if state.last_agent_played_id is None else state.last_agent_played_id
        agent = agents[(last_agent_played_id + 1) % len(agents)]
        actions = state.get_legal_actions(agent.id)

        if len(actions) == 0:
            return None, 100 if player == Player.MIN else -100

        if max_levels == 0:
            if player == Player.MAX:
                score = -math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent.id, action)
                    number_of_min_agent_actions = 8 - len(new_state.get_legal_actions(last_agent_played_id))
                    if score < number_of_min_agent_actions:
                        score = number_of_min_agent_actions
                        best_action = action
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break
                return best_action, score
            else:
                score = math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent.id, action)
                    number_of_max_agent_actions = len(new_state.get_legal_actions(last_agent_played_id)) - 8
                    if score > number_of_max_agent_actions:
                        score = number_of_max_agent_actions
                        best_action = action
                    beta = min(beta, score)
                    if alpha >= beta:
                        break
                return best_action, score

        if player == Player.MAX:
            score = -math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent.id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1, Player.MIN, alpha, beta)
                if score < minimax_score:
                    score = minimax_score
                    best_action = action
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return best_action, score
        else:
            score = math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent.id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1, Player.MAX, alpha, beta)
                if score > minimax_score:
                    score = minimax_score
                    best_action = action
                beta = min(beta, score)
                if alpha >= beta:
                    break
            return best_action, score


class ExpectAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        action, score = self.expectimax(state, max_levels)
        return action

    def expectimax(self, state, max_levels):
        agents = state.agents
        last_agent_played_id = len(agents) - 1 if state.last_agent_played_id is None else state.last_agent_played_id
        agent = agents[(last_agent_played_id + 1) % len(agents)]
        actions = state.get_legal_actions(agent.id)

        if len(actions) == 0:
            return None, -100 if agent.id == self.id else 100

        if max_levels == 0:
            if agent.id == self.id:
                score = -math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent.id, action)
                    number_of_min_agent_actions = len(new_state.get_legal_actions(last_agent_played_id))
                    if score < 8 - number_of_min_agent_actions:
                        score = number_of_min_agent_actions
                        best_action = action
                return best_action, score
            else:
                score = 0
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent.id, action)
                    number_of_max_agent_actions = len(new_state.get_legal_actions(last_agent_played_id))
                    score += number_of_max_agent_actions - 8
                score = score * 1.0 / len(actions)
                best_action = agent.last_action
                return best_action, score

        if agent.id == self.id:
            for action in actions:
                score = -math.inf
                new_state = state.apply_action(agent.id, action)
                expectimax_action, expectimax_score = self.expectimax(new_state, max_levels - 1)
                if score < expectimax_score:
                    score = expectimax_score
                    best_action = action
            print(f"Best action: {best_action}, score: {score}")
            return best_action, score
        else:
            score = 0
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent.id, action)
                expectimax_action, expectimax_score = self.expectimax(new_state, max_levels - 1)
                score += expectimax_score
            score = score * 1.0 / len(actions)
            best_action = agent.last_action
            return best_action, score


class MaxNAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        action, score = self.minimax(state, max_levels)
        return action

    def minimax(self, state, max_levels):
        agents = state.agents
        last_played_agent_id = len(agents) - 1 if state.last_agent_played_id is None else state.last_agent_played_id
        agent = agents[(last_played_agent_id + 1) % len(agents)]
        while not agent.is_active():
            agent = agents[(agent.id + 1) % len(agents)]
        actions = state.get_legal_actions(agent.id)

        if len(actions) == 0:
            return None, -100 if agent.id == self.id else 100

        if max_levels == 0:
            if agent.id == self.id:
                score = -math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent.id, action)
                    number_of_min_agents_actions = 16 - len(new_state.get_legal_actions(agents[(agent.id + 1) % len(agents)].id)) + len(new_state.get_legal_actions(agents[(agent.id + 2) % len(agents)].id))
                    if score < number_of_min_agents_actions:
                        score = number_of_min_agents_actions
                        best_action = action
                return best_action, score
            else:
                score = math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent.id, action)
                    number_of_max_agent_actions = len(new_state.get_legal_actions(agents[(agent.id + 1) % len(agents)].id)) + len(new_state.get_legal_actions(agents[(agent.id + 2) % len(agents)].id)) - 16
                    if score > number_of_max_agent_actions:
                        score = number_of_max_agent_actions
                        best_action = action
                return best_action, score

        if agent.id == self.id:
            score = -math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent.id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1)
                if score < minimax_score:
                    score = minimax_score
                    best_action = action
            return best_action, score
        else:
            score = math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent.id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1)
                if score > minimax_score:
                    score = minimax_score
                    best_action = action
            return best_action, score


