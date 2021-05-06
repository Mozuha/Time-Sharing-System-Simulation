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


def print_input_info(audit_log, num_process, quantum, processes):
  audit_log += f'Number of process: {num_process}\n'
  audit_log += f'Quantum: {quantum}\n\n'
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
# subtract quantum from process time and put the process 
# back to queue if its process time exceeds quantum;
# repeat until queue get empty.
def round_robin(processes, quantum, audit_log):
  ready_queue = [Process(id, proc_time) for id, proc_time in processes]
  sys_clock = 0
  dispatch_time = 1  # overhead: run the dispatcher
  restore_time = 1  # overhead: restore the new process's context before it can begin running
  save_time = 1  # overhead: save the running process's context
  final_wait_time_list = []  # list of wait times of finished processes
  
  while len(ready_queue) != 0:
    sys_clock += dispatch_time  
    process = ready_queue.pop(0)
    sys_clock += restore_time
    process.update_wait_time(dispatch_time + restore_time)
    audit_log += f'{sys_clock:>5} |{process.id:>11} | Process start\n'
    
    if process.proc_time > quantum:
      sys_clock += quantum  # used up quantum; it's time to swap the process
      process.update_proc_time(quantum)  # resulted proc_time = remaining process time
      sys_clock += save_time
      update_ready_wait_times(ready_queue, quantum + dispatch_time + restore_time + save_time)
      ready_queue.append(process)  # put unfinished process back to queue
      audit_log += f'{sys_clock:>5} |{process.id:>11} | Process unfinished within the quantum. Still need {process.proc_time} to complete\n'
    else:
      sys_clock += process.proc_time
      update_ready_wait_times(ready_queue, process.proc_time + dispatch_time + restore_time)
      final_wait_time_list.append([process.id, process.wait_time])
      process.update_proc_time(process.proc_time)
      audit_log += f'{sys_clock:>5} |{process.id:>11} | Process complete\n'
  
  audit_log = print_stats(audit_log, sys_clock, processes, final_wait_time_list)

  return audit_log

# load input file; run round robin; write output to output file
def simulate():
  # open input file, read number of processes, quantum, and processes (id, time);
  # prepare audit log.
  with open('input_round_robin.txt', 'r') as input_file:
    num_process, quantum = map(int, input_file.readline().split())
    processes = []
    for i in range(num_process):
      id, proc_time = input_file.readline().split()
      processes.append([id, int(proc_time)])
    
    print(f'processes:\n{processes}\n')  # just to see the order of processes in console
    
    audit_log = ''
    audit_log = print_input_info(audit_log, num_process, quantum, processes)
    audit_log += f'{"Time":>5} {"Process ID":>12} {"Log":>5}\n'
    audit_log = round_robin(processes, quantum, audit_log)

  # open output file, write audit log.
  with open('audit_log_round_robin2.txt', 'w') as output_file:
    output_file.write(audit_log)

  print(audit_log)  # console output looks better than Windows txt file output.

def main():
  simulate()

if __name__ == '__main__':
  main()
  