import pandas as pd
from sdv.single_table import CTGANSynthesizer
import warnings
warnings.filterwarnings("ignore")

actions = ['cross',
 'dribble',
 'pass',
 'rest',
 'run',
 'shot',
 'tackle',
 'walk']

dict_synthesizer = {}
for action in actions:
  dict_synthesizer[f'synth_{action}'] = CTGANSynthesizer.load(
      filepath= f'synth_{action}.pkl'
  )

#Dictionnary of [min, max] length of each action
dict_action_length = {}

dict_action_length['no action'] = [0.4, 3]
dict_action_length['rest'] = [0.4, 3]
dict_action_length['cross'] = [0.4, 3]
dict_action_length['walk'] = [0.4, 3]

dict_action_length['dribble'] = [0.1, 1.4]
dict_action_length['shot'] = [0.1, 1.4]

dict_action_length['pass'] = [0.1, 2.3]
dict_action_length['tackle'] = [0.1, 2.3]
dict_action_length['run'] = [0.1, 2.3]


def gen_match(time, style):
  """
    Generate a synthetic football match dataset based on the specified time and playing style.

    Parameters:
    - time (float): The duration of the football match in minutes.
    - style (str): The playing style of the match, which can be 'attacking', 'defending', or 'balanced'.

    Returns:
    - pd.DataFrame: A synthetic football match dataset with actions. Each row contain an gait of action and the label of this action

    This function generates a synthetic football match dataset with actions such as 'walk', 'run', 'rest', 'dribble', 'cross', 'pass', 'shot', and 'tackle'.
    The probabilities of these actions occurring are determined by the playing style specified:
    - 'attacking': Actions with higher offensive probabilities.
    - 'defending': Actions with higher defensive probabilities.
    - 'balanced': Actions with balanced probabilities.

    The 'time' parameter specifies the duration of the match in minutes, which is converted to seconds internally.

    The generated dataset includes action labels and 'norm' columns containing synthetic data for each action.
    The data is sampled and shuffled to create a realistic match sequence and is returned as a Pandas DataFrame.
    """
  dict_match = {}
  if style == 'attacking':
        action_probs = {'walk': 0.2, 'run': 0.3, 'rest': 0.04, 'dribble': 0.15, 'cross': 0.1, 'pass': 0.1, 'shot': 0.1, 'tackle': 0.01}
  elif style == 'defending':
      action_probs = {'walk': 0.2, 'run': 0.3, 'rest': 0.05, 'dribble': 0.14, 'cross': 0.05, 'pass': 0.05, 'shot':0.01, 'tackle': 0.2}
  else:
      action_probs = {'walk': 0.2, 'run': 0.3, 'rest': 0.05, 'dribble': 0.1, 'cross': 0.15, 'pass': 0.15, 'shot': 0.1, 'tackle':0.1}

  time = time*60

  action_in_game = []
  for action in actions:
    action_in_game.append(action)
    dict_match[f'match_{action}'] = dict_synthesizer[f'synth_{action}'].sample(num_rows = int(time*action_probs[action]/dict_action_length[action][1])-1)
    if dict_match[f'match_{action}'].shape[0] != 0:
        action_in_game.append(action)
        dict_match[f'match_{action}']['norm'] = dict_match[f'match_{action}'].drop(columns=['label']).apply(lambda row: row.tolist(), axis=1)

  data_match = pd.concat([dict_match[f'match_{action}'] for action in action_in_game], axis = 0)

  bool = True
  while bool:
    real_match = data_match[['label','norm']].sample(frac=1).reset_index(drop=True)
    pattern = ['shot','shot','shot']
    for i in range(len(list(real_match['label'])) - len(pattern) + 1):
        if list(real_match['label'])[i:i+len(pattern)] == pattern:
          bool = False

  return real_match