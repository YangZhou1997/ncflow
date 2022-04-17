import os
import random
import re

folder = '/home/xuzhiying/ncflow/ext/teavar/data/b4-teavar.json'

f = open(f'{folder}/paths/EDInvCap4_backup', 'r')
raw_data = f.read()
paths = re.split(r'\n\n', raw_data.strip())
f.close()

f = open(f'{folder}/demand_backup.txt', 'r')
raw_demands = f.read().strip().split('\n')
f.close()

def all_tuples_in_str(tuples, str):
  for fail_tuple in tuples:
    if fail_tuple not in str:
      return False
  return True

def any_tuple_in_str(tuples, str):
  for fail_tuple in tuples:
    if fail_tuple in str:
      return True
  return False

def gen_failure_path():
  while True:
    sws = [f's{i}' for i in range(1, 13)]
    fail_sws = random.sample(sws, 4)
    fail_tuples = [f'({fail_sws[0]},{fail_sws[1]})', 
                   f'({fail_sws[1]},{fail_sws[0]})',
                   f'({fail_sws[2]},{fail_sws[3]})',
                   f'({fail_sws[3]},{fail_sws[2]})']
    if all_tuples_in_str(fail_tuples, raw_data):
      break
  print(fail_tuples)

  # generate and write new paths
  f_w = open(f'{folder}/paths/EDInvCap4', 'w')
  for path in paths:
    lines = path.strip().split('\n')
    new_lines = []
    cnt = 0
    for line in lines:
      if not any_tuple_in_str(fail_tuples, line):
        new_lines.append(line)
        cnt += 1
    cnt -= 1
    if cnt == 0:
      f_w.write(f'{new_lines[0]}\n\n')
    else:
      for line in new_lines:
        pattern = r'@ \d+\.\d+'
        new_line = re.sub(pattern, f'@ {1/cnt}', line)
        f_w.write(f'{new_line}\n')
      f_w.write('\n')
  f_w.close()

  return fail_tuples

def gen_normal_path():
  f_w = open(f'{folder}/paths/EDInvCap4', 'w')
  f_w.write(raw_data)
  f_w.close()

def gen_demand(demand):
  f_w = open(f'{folder}/demand.txt', 'w')
  f_w.write(f'{demand}\n')
  f_w.close()
  
if __name__ == '__main__':
  # raw_demands = raw_demands[:1]
  for i, demand in enumerate(raw_demands):
    gen_demand(demand)
    res_dir = f'failure_exp_data/{i+1}'
    os.system(f'mkdir -p {res_dir}')

    gen_normal_path()
    os.system('bash teavar_star.sh')
    os.system(f'mv teavar_star.txt {res_dir}/teavar_star_before.txt')
    
    fail_tuple = gen_failure_path()
    os.system(f'echo "{fail_tuple}" > {res_dir}/fail_tuple.txt')
    os.system('bash teavar_star.sh')
    os.system(f'mv teavar_star.txt {res_dir}/teavar_star_after.txt')