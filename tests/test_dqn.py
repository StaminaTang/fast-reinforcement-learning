# from itertools import product
# from time import sleep
#
# import pytest
# from fastai.basic_data import DatasetType
#
# from fast_rl.agents.dqn import create_dqn_model, dqn_learner
# from fast_rl.agents.dqn_models import *
# from fast_rl.core.agent_core import ExperienceReplay, PriorityExperienceReplay, GreedyEpsilon
# from fast_rl.core.data_block import MDPDataBunch, FEED_TYPE_STATE, FEED_TYPE_IMAGE
# from fast_rl.core.metrics import RewardMetric, EpsilonMetric
# from fast_rl.core.train import GroupAgentInterpretation, AgentInterpretation
#
# p_model = [DQNModule, FixedTargetDQNModule, DoubleDuelingModule, DuelingDQNModule, DoubleDQNModule]
# p_exp = [ExperienceReplay, PriorityExperienceReplay]
# p_format = [FEED_TYPE_STATE]#, FEED_TYPE_IMAGE]
# p_envs = ['CartPole-v1']
#
# config_env_expectations = {
# 	'CartPole-v1': {'action_shape': (1, 2), 'state_shape': (1, 4)},
# 	'maze-random-5x5-v0': {'action_shape': (1, 4), 'state_shape': (1, 2)}
# }
#
#
# def trained_learner(model_cls, env, s_format, experience, bs, layers, memory_size=1000000, decay=0.00001,
# 					copy_over_frequency=300, lr: Union[float, list] = 0.001):
# 	memory = experience(memory_size=memory_size, reduce_ram=True)
# 	explore = GreedyEpsilon(epsilon_start=1, epsilon_end=0.1, decay=decay)
# 	if type(lr) == list: lr = lr[0] if model_cls == DQNModule else lr[2]
# 	model = create_dqn_model(model_cls, lr=lr, layers=layers, copy_over_frequency=copy_over_frequency)
# 	data = MDPDataBunch.from_env(env, render='human', bs=bs, add_valid=False, feed_type=s_format)
# 	learn = dqn_learner(data, model, memory=memory, exploration_method=explore,
# 						callback_fns=[RewardMetric, EpsilonMetric])
# 	learn.fit(450)
# 	return learn
#
#
# @pytest.mark.usefixtures('skip_performance_check')
# @pytest.mark.parametrize(["model_cls", "s_format", "env"], list(product(p_model, p_format, p_envs)))
# def test_dqn_create_dqn_model(model_cls, s_format, env):
# 	data = MDPDataBunch.from_env(env, render='rgb_array', bs=32, add_valid=False, feed_type=s_format)
# 	model = create_dqn_model(data, model_cls)
# 	model.eval()
# 	model(data.state.s)
#
# 	assert config_env_expectations[env]['action_shape'] == (1, data.action.n_possible_values.item())
# 	if s_format == FEED_TYPE_STATE:
# 		assert config_env_expectations[env]['state_shape'] == data.state.s.shape
#
#
# @pytest.mark.usefixtures('skip_performance_check')
# @pytest.mark.parametrize(["model_cls", "s_format", "mem", "env"], list(product(p_model, p_format, p_exp, p_envs)))
# def test_dqn_dqn_learner(model_cls, s_format, mem, env):
# 	data = MDPDataBunch.from_env(env, render='rgb_array', bs=32, add_valid=False, feed_type=s_format)
# 	model = create_dqn_model(data, model_cls)
# 	memory = mem(memory_size=1000, reduce_ram=True)
# 	exploration_method = GreedyEpsilon(epsilon_start=1, epsilon_end=0.1, decay=0.001)
# 	dqn_learner(data=data, model=model, memory=memory, exploration_method=exploration_method)
#
# 	assert config_env_expectations[env]['action_shape'] == (1, data.action.n_possible_values.item())
# 	if s_format == FEED_TYPE_STATE:
# 		assert config_env_expectations[env]['state_shape'] == data.state.s.shape
#
#
# @pytest.mark.usefixtures('skip_performance_check')
# @pytest.mark.parametrize(["model_cls", "s_format", "mem", "env"], list(product(p_model, p_format, p_exp, p_envs)))
# def test_dqn_fit(model_cls, s_format, mem, env):
# 	data = MDPDataBunch.from_env(env, render='rgb_array', bs=5, max_steps=20, add_valid=False, feed_type=s_format)
# 	model = create_dqn_model(data, model_cls, opt=torch.optim.RMSprop)
# 	memory = mem(memory_size=1000, reduce_ram=True)
# 	exploration_method = GreedyEpsilon(epsilon_start=1, epsilon_end=0.1, decay=0.001)
# 	learner = dqn_learner(data=data, model=model, memory=memory, exploration_method=exploration_method)
# 	learner.fit(2)
#
# 	assert config_env_expectations[env]['action_shape'] == (1, data.action.n_possible_values.item())
# 	if s_format == FEED_TYPE_STATE:
# 		assert config_env_expectations[env]['state_shape'] == data.state.s.shape
#
#
# @pytest.mark.usefixtures('skip_performance_check')
# @pytest.mark.parametrize(["model_cls", "s_format", "mem"], list(product(p_model, p_format, p_exp)))
# def test_dqn_fit_maze_env(model_cls, s_format, mem):
# 	success = False
# 	while not success:
# 		try:
# 			data = MDPDataBunch.from_env('maze-random-5x5-v0', render='rgb_array', bs=5, max_steps=20,
# 										 add_valid=False, feed_type=s_format)
# 			model = create_dqn_model(data, model_cls, opt=torch.optim.RMSprop)
# 			memory = ExperienceReplay(10000)
# 			exploration_method = GreedyEpsilon(epsilon_start=1, epsilon_end=0.1, decay=0.001)
# 			learner = dqn_learner(data=data, model=model, memory=memory, exploration_method=exploration_method)
# 			learner.fit(2)
#
# 			assert config_env_expectations['maze-random-5x5-v0']['action_shape'] == (
# 				1, data.action.n_possible_values.item())
# 			if s_format == FEED_TYPE_STATE:
# 				assert config_env_expectations['maze-random-5x5-v0']['state_shape'] == data.state.s.shape
# 			sleep(1)
# 			success = True
# 		except Exception as e:
# 			if not str(e).__contains__('Surface'):
# 				raise Exception
#
#
# @pytest.mark.usefixtures('skip_performance_check')
# @pytest.mark.parametrize(["model_cls", "s_format", 'experience'], list(product(p_model, p_format, p_exp)))
# def test_dqn_models_minigrids(model_cls, s_format, experience):
# 	group_interp = GroupAgentInterpretation()
# 	for i in range(5):
# 		learn = trained_learner(model_cls, 'MiniGrid-FourRooms-v0', s_format, experience, bs=32, layers=[64, 64],
# 								memory_size=1000000, decay=0.00001)
#
# 		meta = f'{experience.__name__}_{"FEED_TYPE_STATE" if s_format == FEED_TYPE_STATE else "FEED_TYPE_IMAGE"}'
# 		interp = AgentInterpretation(learn, ds_type=DatasetType.Train)
# 		interp.plot_rewards(cumulative=True, per_episode=True, group_name=meta)
# 		group_interp.add_interpretation(interp)
# 		filename = f'{learn.model.name.lower()}_{meta}'
# 		group_interp.to_pickle(f'../docs_src/data/minigrid_{learn.model.name.lower()}/', filename)
# 		del learn
#
#
# @pytest.mark.usefixtures('skip_performance_check')
# @pytest.mark.parametrize(["model_cls", "s_format", 'experience'],
# 						 list(product(p_model, p_format, p_exp)))
# def test_dqn_models_cartpole(model_cls, s_format, experience):
# 	group_interp = GroupAgentInterpretation()
# 	for i in range(5):
# 		learn = trained_learner(model_cls, 'CartPole-v1', s_format, experience, bs=32, layers=[64, 64],
# 								memory_size=1000000, decay=0.00001)
#
# 		meta = f'{experience.__name__}_{"FEED_TYPE_STATE" if s_format == FEED_TYPE_STATE else "FEED_TYPE_IMAGE"}'
# 		interp = AgentInterpretation(learn, ds_type=DatasetType.Train)
# 		interp.plot_rewards(cumulative=True, per_episode=True, group_name=meta)
# 		group_interp.add_interpretation(interp)
# 		filename = f'{learn.model.name.lower()}_{meta}'
# 		group_interp.to_pickle(f'../docs_src/data/cartpole_{learn.model.name.lower()}/', filename)
# 		del learn
#
#
# @pytest.mark.usefixtures('skip_performance_check')
# @pytest.mark.parametrize(["model_cls", "s_format", 'experience'], list(product(p_model, p_format, p_exp)))
# def test_dqn_models_lunarlander(model_cls, s_format, experience):
# 	group_interp = GroupAgentInterpretation()
# 	for i in range(5):
# 		learn = trained_learner(model_cls, 'LunarLander-v2', s_format, experience, bs=32, layers=[128, 64],
# 								memory_size=1000000, decay=0.00001, copy_over_frequency=600, lr=[0.001, 0.00025])
# 		meta = f'{experience.__name__}_{"FEED_TYPE_STATE" if s_format == FEED_TYPE_STATE else "FEED_TYPE_IMAGE"}'
# 		interp = AgentInterpretation(learn, ds_type=DatasetType.Train)
# 		interp.plot_rewards(cumulative=True, per_episode=True, group_name=meta)
# 		group_interp.add_interpretation(interp)
# 		filename = f'{learn.model.name.lower()}_{meta}'
# 		group_interp.to_pickle(f'../docs_src/data/lunarlander_{learn.model.name.lower()}/', filename)
# 		del learn
#
#
# @pytest.mark.usefixtures('skip_performance_check')
# @pytest.mark.parametrize(["model_cls", "s_format", 'experience'], list(product(p_model, p_format, p_exp)))
# def test_dqn_models_mountaincar(model_cls, s_format, experience):
# 	group_interp = GroupAgentInterpretation()
# 	for i in range(5):
# 		learn = trained_learner(model_cls, 'MountainCar-v0', s_format, experience, bs=32, layers=[24, 12],
# 								memory_size=1000000, decay=0.00001, copy_over_frequency=1000)
# 		meta = f'{experience.__name__}_{"FEED_TYPE_STATE" if s_format == FEED_TYPE_STATE else "FEED_TYPE_IMAGE"}'
# 		interp = AgentInterpretation(learn, ds_type=DatasetType.Train)
# 		interp.plot_rewards(cumulative=True, per_episode=True, group_name=meta)
# 		group_interp.add_interpretation(interp)
# 		filename = f'{learn.model.name.lower()}_{meta}'
# 		group_interp.to_pickle(f'../docs_src/data/mountaincar_{learn.model.name.lower()}/', filename)
#
# 		del learn