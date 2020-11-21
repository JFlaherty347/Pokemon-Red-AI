import retro
import gym
import os
import time
import retro.enums

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.policies import CnnPolicy
from stable_baselines.common.policies import MlpLnLstmPolicy
from stable_baselines.common.policies import CnnLnLstmPolicy
from stable_baselines import A2C
from stable_baselines.common.env_checker import check_env
from stable_baselines.common.cmd_util import make_vec_env
from stable_baselines.common.policies import FeedForwardPolicy, register_policy
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.vec_env import VecNormalize

#
class CustomPolicy(FeedForwardPolicy):
    def __init__(self, *args, **kwargs):
        super(CustomPolicy, self).__init__(*args, **kwargs,
                                           net_arch=[dict(pi=[128, 128, 128],
                                                          vf=[128, 128, 128])],
                                           feature_extraction="cnn")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
        retro.data.Integrations.add_custom_path(
                os.path.join(SCRIPT_DIR, "custom_integrations")
        )
        print("PokemonRed-GameBoy" in retro.data.list_games(inttype=retro.data.Integrations.ALL))
        env = retro.make("PokemonRed-GameBoy", inttype=retro.data.Integrations.ALL, obs_type=retro.Observations.RAM, use_restricted_actions=retro.Actions.DISCRETE) 
        #obs_type=retro.Observations.RAM #see https://retro.readthedocs.io/en/latest/python.html#observations
        print(env)
        
        # print(env.action_space)

        vec_env = make_vec_env(lambda: env, n_envs=32)
        vec_env = VecNormalize(vec_env, norm_obs=True, norm_reward=True, clip_obs=10)
        # time.sleep(3)    

        model = A2C(MlpPolicy, vec_env, verbose=1, tensorboard_log="./pokemon-red-tensorboard/")

        # pretrain? https://stable-baselines.readthedocs.io/en/master/guide/pretrain.html

        start_time = time.time()
        model.learn(total_timesteps=5000000, tb_log_name="a2c-MLP_5M")
        print("TRAINING COMPLETE! Time elapsed: ", str(time.time()-start_time))

        print("Saving model...")
        model.save("a2c_mlp_ram_5M")


        # print("Evaluating now...")
        start_time = time.time()
        printed_done = False
        # sampled_info = False

        # mean_reward = evaluate_policy(model, env, n_eval_episodes=4000, render=False)
        # print("done evaluating! mean reward: ", mean_reward)



        obs = env.reset()
        while True:
            action, _states = model.predict(obs)
            obs, rewards, dones, info = env.step(action)
            env.render()
            # if not sampled_info:
            #     print("Info:\n", info, "\n</info>")
            #     sampled_info = True

            if dones and not printed_done:
                print("Success! time elapsed: ", str(time.time()-start_time))
                printed_done = True

        env.close()

    
if __name__ == "__main__":
        main()