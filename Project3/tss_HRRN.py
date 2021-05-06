# May 7, 2021
# Mizuki Hashimoto
#
# [Project 3]
# Change the scheduling algorithm of the simple time-sharing system to HRRN (Highest Response Ratio Next).
# Calculate turnaround time and normalized turnaround time for each of the processes.

# <input file format>
# number_of_processes
# id1 time1
# id2 time2
#  :    :  

# <output file format>
# Number of processes: num_process
# Process_ID Process_time
# id1 time1
# id2 time2
#  :    :
#
#
#---------Log---------
#
# Time Process_ID Log
# time1 id1 log1
# time2 id2 log2
#   :    :   :
#
#
#-------Stats-------
#
# All processes commpleted in system_clock
# Total wait time is: total_wait_time
# Average wait time is: avg_wait_time
# Average turnaround time is: avg_turnaround_time
# Average normalized turnaround time is: avg_norm_turnaround_time
#
# Process_ID Turnaround_time
# id1 time1
# id2 time2
#  :    :
#
# Process_ID Normalized_turnaround_time
# id1 time1
# id2 time2
#  :    :

class Process:
  def __init__(self, id, proc_time):
    self.id = id
    self.proc_time = proc_time
    self.wait_time = 0
  
  def update_proc_time(self, time):
    if time <= self.proc_time:
      self.proc_time -= time
    else:
      self.proc_time = 0

  def update_wait_time(self, time):
    self.wait_time += time


def print_input_info(audit_log, num_process, processes):
  audit_log += f'Number of process: {num_process}\n'
  audit_log += f'{"Process ID":>10} {"Process time":>15}\n'
  for id, time in processes:
    audit_log += f'{id:>10} {time:>15}\n'
  audit_log += '\n\n----------------Log--------------------\n\n'
  
  return audit_log

def print_stats(audit_log, sys_clock, processes, final_wait_time_list):
  final_wait_time_list.sort(key=lambda l:l[0])  # sort in ascending order of process name
  print(f'final wait time list:\n{final_wait_time_list}\n')  # just to see the list in console

  turnaround_time = [[w[0], w[1]+s[1]] for w, s in zip(final_wait_time_list, processes)]  # wait time + service (process) time
  print(f'turnaround time:\n{turnaround_time}\n')  # just to see the list in console

  norm_turnaround_time = [[s[0], t[1]/s[1]] for s, t in zip(processes, turnaround_time)]  # turnaround time / service (process) time
  print(f'normalized turnaround time:\n{norm_turnaround_time}\n')  # just to see the list in console

  audit_log += '\n\n----------------Stats--------------------\n\n'
  audit_log += f'All processes completed in {sys_clock}'
  audit_log += f'\nTotal wait time is: {sum([wt[1] for wt in final_wait_time_list])}'
  audit_log += f'\nAverage wait time is: {sum([wt[1] for wt in final_wait_time_list]) / len(final_wait_time_list)}'
  audit_log += f'\nAverage turnaround time is: {sum([tt[1] for tt in turnaround_time]) / len(turnaround_time)}'
  audit_log += f'\nAverage normalized turnaround time is: {sum([nt[1] for nt in norm_turnaround_time]) / len(norm_turnaround_time):.2f}\n\n'

  audit_log += f'{"Process ID":>10} {"Turnaround time":>17}\n'
  for id, time in turnaround_time:
    audit_log += f'{id:>10} {time:>17}\n'
    
  audit_log += f'\n{"Process ID":>10} {"Normalized turnaround time":>29}\n'  
  for id, time in norm_turnaround_time:
    audit_log += f'{id:>10} {time:>17.2f}\n'

  return audit_log

# update wait times of the processes waiting in the queue
def update_ready_wait_times(ready_queue, time):
  for p in ready_queue:
    p.wait_time += time

# put processes into queue; get one process; 
# increment system clock according to stated process time;
# once current process is completed, calculate response ratios
# and sort queue in response ratio descending order;
# repeat until queue get empty.
def hrrn(processes, audit_log):
  ready_queue = [Process(id, proc_time) for id, proc_time in processes]
  sys_clock = 0
  dispatch_time = 1  # overhead: run the dispatcher
  restore_time = 1  # overhead: restore the new process's context before it can begin running
  final_wait_time_list = []  # list of wait times of finished processes

  print('process flow:')
  while len(ready_queue) != 0:
    sys_clock += dispatch_time  
    process = ready_queue.pop(0)
    sys_clock += restore_time
    process.update_wait_time(dispatch_time + restore_time)
    audit_log += f'{sys_clock:>5} |{process.id:>11} | Process start\n'
    
    sys_clock += process.proc_time
    update_ready_wait_times(ready_queue, process.proc_time + dispatch_time + restore_time)
    final_wait_time_list.append([process.id, process.wait_time])
    process.update_proc_time(process.proc_time)  # ensure expected process time completed

    # HRRN selection function
    # response ratio = (waiting time + process time) / process time
    # sort in descending order so the process with the largest ratio will be processed next
    ready_queue.sort(key=lambda p:(p.wait_time + p.proc_time) / p.proc_time, reverse=True)
    print([p.id for p in ready_queue])  # check how ready_queue looks after it is sorted

    audit_log += f'{sys_clock:>5} |{process.id:>11} | Process complete\n'
  
  print('\n')
  audit_log = print_stats(audit_log, sys_clock, processes, final_wait_time_list)

  return audit_log

# load input file; run round robin; write output to output file
def simulate():
  # open input file, read number of processes and processes (id, time);
  # prepare audit log.
  with open('input_HRRN.txt', 'r') as input_file:
    num_process = int(input_file.readline())
    processes = []
    for i in range(num_process):
      id, proc_time = input_file.readline().split()
      processes.append([id, int(proc_time)])
    
    print(f'processes:\n{processes}\n')  # just to see the order of processes in console
    
    audit_log = ''
    audit_log = print_input_info(audit_log, num_process, processes)
    audit_log += f'{"Time":>5} {"Process ID":>12} {"Log":>5}\n'
    audit_log = hrrn(processes, audit_log)

  # open output file, write audit log.
  with open('audit_log_HRRN.txt', 'w') as output_file:
    output_file.write(audit_log)

  print(audit_log)  # console output looks better than Windows txt file output.

def main():
  simulate()

if __name__ == '__main__':
  main()
  