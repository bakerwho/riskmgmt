from lsh import *

class System:
	def __init__(self, numAgents=50, **kwargs):
		strategies = kwargs.pop('strategies', None)
		strategies = parse_strategies(strategies, numAgents)
		assert len(strategies) == numAgents
		self.actionspace = {0:'low', 1:'stable', 2:'high'}
		self.tracked_vars = [	't', 'state', 'lsh_result', 
								'lsh_total_reward', 'lsh_actual_reward', 
								'reward']
		self.agents = []
		for i in range(numAgents):
			self.add_Agent(strategies[i])
		self.timer = 1

	def add_Agent(self, strategy):
		i = len(self.agents)
		self.agents.append(Agent(	agentID=i, strategy_type=strategy,
									tracked_vars = self.tracked_vars, 
									actionspace = self.actionspace))
		self.numAgents += 1

	def step(self):
		choices = self.get_choices()
		rewards = self.get_rewards(choices)
		self.update_history()
		self.timer += 1

	def get_choices(self):
		choices = []
		for agent in self.agents:
			ID = agent.ID
			assert ID == len(choices)
			choices.append(agent.choose())
		return choices

	def get_rewards(self, choices):
		# Note: operations are hard-coded here. This function holds only for this payoff scheme
		choice_counts = {val : choices.count(val) for val in self.actionspace.items()}
		total_rewards = {index : rewardfunc(index, choice_counts) for index in self.actionspace.items()}
		def rewardfunc(choice, choice_counts):
			if choice == 0:
				if np.random.random() < 0.5:
					return 0
				else: return 40
			elif choice == 1:
				if np.random.random() < 0.75:
					return 0
				else: return 80
			elif choice == 1:
				return int(choice_counts[choice])
		rewards = []
		for choice in choices:
			if choice == 1:
				reward = 1
			else:
				reward = total_rewards[choice]/choice_counts[choice]
			rewards.append(reward)
		return rewards

	def update_history(self, choices, rewards):
		for agent in self.agents:
			row = {'t':self.timer}
			row[t]
		pass

	def parse_strategies(strategies, numAgents):
		if strategies is None:
			strategies = ['random' for i in range(numAgents)]
			return strategies
		elif isinstance(strategies, dict):
			if sum(list(strategies.values())) == numAgents:
				strategies = [strat for strat, num in strategies.items() 
											for i in range(num)]
				return strategies
			elif sum(list(strategies.values())) == 1.0:
				strategies = [strat for strat, num in strategies.items() 
											for i in range(int(numAgents*num))]
				while len(strategies)<numAgents:
					strategies.append(strat)
				return strategies





class Agent:
	def __init__(self, agentID, strategy_type='random', **kwargs):
		self.ID = agentID
		COLUMNS = [	't', 'state', 'lsh_result', 'lsh_total_reward', 
					'lsh_actual_reward', 'reward']
		self.tracked_vars = kwargs.pop('tracked_vars', COLUMNS)
		self.agentHistory = pd.DataFrame(columns=self.tracked_vars)
		self.actionspace = kwargs.pop(	'actionspace', 
										{'low': 0, 'stable':1, 'high':2})
		self.set_strategy(strategy_type)

	def set_strategy(self, strategy_type, **kwargs):
		func = kwargs.pop('strategy_func', None)
		desc = kwargs.pop('strategy_desc', '')
		if strategy_type is None:
			if not (callable(func) and isinstance(desc, str)):
				raise ValueError('Either strategy_type or func \
										must not be None')
		else:
			func, desc = self.parse_strategy(strategy_type)
		assert isinstance(desc, str) and callable(func)
		self.strategy_func = func
		self.strategy_desc = desc


	def parse_strategy(self, strategy):
		assert isinstance(strategy, str)
		strategy = '_'.join(strategy.split(' '))
		if strategy == 'least_popular':
			def func():
				lvs = self.get_latest_values()
				if lvs:
					return lvs.lsh_result 
				else:
					return np.random.randint(0,3)
			desc = strategy
		elif strategy == 'random':
			func = lambda : np.random.randint(0,3)
			desc = 'random'
		elif strategy in self.actionspace:
			val = int(self.actionspace[strategy])
			func = lambda : val 
			desc = 'always {}'.format(strategy)
		else:
			raise ValueError('Invalid strategy to parse_strategy()')
		#
		return func, desc


	def choose(self):
		return self.strategy_func()

	def get_latest_values(self):
		if self.agentHistory.size != 0:
			idx = self.agentHistory['t'].idxmax()
			return self.agentHistory.iloc[idx]
		else:
			return None

	def update(self, row):
		self.agentHistory = lsh.utils.add_row_to_DF(
										self.agentHistory, row)


"""
import lsh
a = lsh.Agent(1)
a.agentHistory = a.agentHistory.append({k:1 for k in a.agentHistory.columns}, ignore_index=True)
a.agentHistory = lsh.utils.add_row_to_DF(a.agentHistory, [3, 3, 3, 3, 3, 2])




"""







