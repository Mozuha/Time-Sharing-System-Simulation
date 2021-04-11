# April 4, 2021
# Mizuki Hashimoto
#
# [Project 2]
# Introduce process "priority" into the simple time-sharing system using a round-robin selection algorithm from Project 1.
# Use the priority to ensure that processes of higher priority are selected first.
# The priority can be assigned using a new field in the input file. (smaller number, higher priority)

# <input file format>
# number_of_processes quantum
# id1 time1 priority1
# id2 time2 priority2
#  :    :       :

# <output file format>
# Time Process_ID Log
# time1 id1 log1
# time2 id2 log2
#   :    :   :
# All processes commpleted in system_clock
# Total wait time is total_wait_time
# Average wait time is avg_wait_time

# !!!!!UPDATED!!!!!
# - Changed from queue to deque
# - Changed variable names for times: Process.time->Process.proc_time, cpu_time->system_clock
# - Denominated overheads for semantical purpose: dispatch_time, restore_time, save_time
# - Moved codes for loading and writing files to simulate function
# - Added wait_time and priority attributes, and update_proc_time and update_wait_time functions to Process class
# - Added update_ready_wait_times function
# - Added final_wait_time_list to hold resulted waiting time of each process
# - Added code to sort the list of processes in priority descending order

from collections import deque

class Process:
  def __init__(self, id, proc_time, priority):
    self.id = id
    self.proc_time = proc_time
    self.wait_time = 0
    self.priority = priority
  
  def update_proc_time(self, time):
    if time <= self.proc_time:
      self.proc_time -= time
    else:
      self.proc_time = 0

  def update_wait_time(self, time):
    self.wait_time += time

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
  ready_queue = deque()
  sys_clock = 0
  dispatch_time = 1  # overhead: run the dispatcher
  restore_time = 1  # overhead: restore the new process's context before it can begin running
  save_time = 1  # overhead: save the running process's context
  final_wait_time_list = []  # list of wait times of finished processes

  for id, proc_time, priority in processes:
    ready_queue.append(Process(id, proc_time, priority))
  
  while len(ready_queue) != 0:
    sys_clock += dispatch_time  
    process = ready_queue.popleft()
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
  
  audit_log += f'\nAll processes completed in {sys_clock}'
  audit_log += f'\nTotal wait time is: {sum([wt[1] for wt in final_wait_time_list])}'
  audit_log += f'\nAverage wait time is: {sum([wt[1] for wt in final_wait_time_list]) / len(final_wait_time_list)}'
  print(final_wait_time_list, '\n')  # just to see the list in console

  return audit_log

# load input file; run round robin; write output to output file
def simulate():
  # open input file, read number of processes, quantum, and processes (id, time);
  # prepare audit log.
  with open('input.txt', 'r') as input_file:
    audit_log = f'{"Time":>5} {"Process ID":>12} {"Log":>5}\n\n'

    num_process, quantum = map(int, input_file.readline().split())
    processes = []
    for i in range(num_process):
      id, proc_time, priority = input_file.readline().split()
      processes.append([id, int(proc_time), int(priority)])
    
    processes.sort(key=lambda x:x[2])  # sort processes in priority descending order (smaller number, higher priority)
    print(processes, '\n')  # just to see the order of processes in console
    
    audit_log = round_robin(processes, quantum, audit_log)

  # open output file, write audit log.
  with open('audit_log.txt', 'w') as output_file:
    output_file.write(audit_log)

  print(audit_log)  # console output looks better than Windows txt file output.

def main():
  simulate()

if __name__ == '__main__':
  main()
  